#!/usr/bin/env python3
"""CLI tool for running AI security tests and model predictions using Giskard."""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import pandas as pd
import requests
import yaml

# Import the official Giskard package.
try:
    import giskard
except ImportError:
    print("Giskard package not found. Please install it using:")
    print("pip install git+https://github.com/Giskard-AI/giskard.git")
    sys.exit(1)


def setup_logging(verbose: bool):
    """Set up logging configuration with file and console handlers.

    Args:
        verbose: If True, set log level to DEBUG, otherwise INFO.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    fh = logging.FileHandler("aissert_cli.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


logger = setup_logging(verbose=False)


def load_config(config_path: str) -> dict:
    """Load configuration from JSON or YAML file.

    Args:
        config_path: Path to configuration file (.json, .yaml, or .yml).

    Returns:
        Dictionary containing configuration data.

    Raises:
        SystemExit: If file not found or unsupported format.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        logger.error("Configuration file not found: %s", config_path)
        sys.exit(1)
    with config_file.open() as f:
        if config_path.endswith(".json"):
            config = json.load(f)
        elif config_path.endswith((".yaml", ".yml")):
            config = yaml.safe_load(f)
        else:
            logger.error("Unsupported config file format. Use .json or .yaml/.yml")
            sys.exit(1)
    logger.info("Configuration loaded successfully from %s", config_path)
    return config


def load_dataset(input_path: str) -> pd.DataFrame:
    """Load dataset from CSV or JSON file.

    Args:
        input_path: Path to dataset file (.csv or .json).

    Returns:
        DataFrame containing the dataset.

    Raises:
        SystemExit: If file not found or unsupported format.
    """
    input_file = Path(input_path)
    if not input_file.exists():
        logger.error("Input file not found: %s", input_path)
        sys.exit(1)
    if input_path.endswith(".csv"):
        df = pd.read_csv(input_path)
    elif input_path.endswith(".json"):
        df = pd.read_json(input_path)
    else:
        logger.error("Unsupported input file format. Use .csv or .json")
        sys.exit(1)
    logger.info("Dataset loaded successfully from %s", input_path)
    return df


def api_call(row: pd.Series, config: dict, api_endpoint: str, max_retries: int = 3):
    """Make API call with data from a DataFrame row.

    Args:
        row: DataFrame row containing input data.
        config: Configuration dictionary with input_mapping and request params.
        api_endpoint: API endpoint URL.
        max_retries: Maximum number of retry attempts on failure.

    Returns:
        JSON response from API or None if all attempts fail.
    """
    input_mapping = config.get("input_mapping", {})
    payload = {}
    for df_col, api_param in input_mapping.items():
        if df_col in row:
            value = row[df_col]
            payload[api_param] = value.item() if hasattr(value, "item") else value
    request_params = config.get("request", {})
    headers = request_params.get("headers", {})
    headers.setdefault("Accept", "application/json")
    method = request_params.get("method", "POST").upper()
    timeout = request_params.get("timeout", 10)
    logger.info("API request payload: %s", payload)
    attempt = 0
    while attempt < max_retries:
        try:
            if method == "POST":
                response = requests.post(api_endpoint, json=payload, headers=headers, timeout=timeout)
            elif method == "GET":
                response = requests.get(api_endpoint, params=payload, headers=headers, timeout=timeout)
            else:
                logger.error("Unsupported HTTP method specified: %s", method)
                return None
            response.raise_for_status()
            logger.info("Raw API response: %s", response.text)
            json_response = response.json()
            logger.info("API response received: %s", json_response)
            return json_response
        except requests.Timeout as e:
            logger.error("Timeout occurred: %s", e)
        except requests.RequestException as e:
            logger.error("API request failed on attempt %d: %s", attempt + 1, e)
        except ValueError as e:
            logger.error("Failed to parse API response as JSON: %s", e)
            return None
        attempt += 1
        logger.info("Retrying API call (attempt %d/%d)...", attempt + 1, max_retries)
        time.sleep(1)
    logger.error("Exceeded maximum retry attempts for API call.")
    return None


def transform_response(api_response, config: dict):
    """Transform API response according to output mapping configuration.

    Args:
        api_response: Raw API response (dict or other type).
        config: Configuration dictionary with output_mapping.

    Returns:
        Transformed response based on output_mapping, or original response if no mapping.
    """
    output_mapping = config.get("output_mapping", {})
    if not api_response:
        return None
    transformed_output = {}
    for target_field, response_key in output_mapping.items():
        keys = response_key.split(".")
        value = api_response
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                logger.warning("Key '%s' not found in API response.", key)
                value = None
                break
        transformed_output[target_field] = value
    return transformed_output


def predict(df: pd.DataFrame, config: dict, api_endpoint: str):
    """Make predictions for all rows in a DataFrame using API calls.

    Args:
        df: DataFrame containing input data.
        config: Configuration dictionary.
        api_endpoint: API endpoint URL.

    Returns:
        List of transformed predictions for each row.
    """
    predictions = []
    for index, row in df.iterrows():
        logger.info("Processing row index %d", index)
        api_response = api_call(row, config, api_endpoint)
        transformed = transform_response(api_response, config)
        predictions.append(transformed)
    return predictions


def create_giskard_model(model_name: str, description: str, feature_names: list, predict_function):
    """Create a Giskard model wrapper for testing.

    Args:
        model_name: Name of the model.
        description: Description of the model.
        feature_names: List of feature column names.
        predict_function: Prediction function to wrap.

    Returns:
        Giskard PredictionFunctionModel instance.
    """
    from giskard.models.automodel import PredictionFunctionModel

    # Set scanable=True to enable scanning (if supported by the installed Giskard version)
    return PredictionFunctionModel(
        name=model_name,
        model=predict_function,
        model_type="text_generation",
        feature_names=feature_names,
        description=description,
        scanable=True,
    )


def make_serializable(predictions):
    """Convert predictions to JSON-serializable format.

    Args:
        predictions: List of predictions (may contain dicts or objects).

    Returns:
        List of JSON-serializable dictionaries.
    """
    serializable = []
    for pred in predictions:
        if hasattr(pred, "dict"):
            serializable.append(pred.dict())
        elif isinstance(pred, dict):
            serializable.append(pred)
        else:
            serializable.append(str(pred))
    return serializable


# Define a DummyDataset class that mimics Giskard's expected Dataset interface.
class DummyDataset:
    """Dummy dataset class that mimics Giskard's Dataset interface."""

    def __init__(self, df, target=None):
        """Initialize DummyDataset.

        Args:
            df: Pandas DataFrame containing the data.
            target: Optional target column name.
        """
        self.df = df
        self.row_hashes = pd.Series([hash(tuple(row)) for row in df.values])
        self.column_dtypes = df.dtypes.to_dict()
        self.target = target

    def slice(self, func, row_level=False):
        """Apply slicing function to filter dataset rows.

        Args:
            func: Function to apply for filtering rows.
            row_level: If True, apply function at row level.

        Returns:
            Filtered DummyDataset instance.
        """
        try:
            mask = self.df.apply(func, axis=1)
            if mask.dtype != bool:
                logger.warning("Slice function did not return booleans; skipping slicing.")
                return self
            sliced_df = self.df[mask]
            return DummyDataset(sliced_df, target=self.target)
        except Exception as e:
            logger.warning("Error during slicing: %s. Returning full dataset.", e)
            return self


def main():
    """Main entry point for aissert-cli.

    Parses command-line arguments, makes API predictions, and optionally runs Giskard security tests.
    """
    parser = argparse.ArgumentParser(
        description="aissert-cli: Wrap API calls into a Giskard model, output predictions, and run tests."
    )
    parser.add_argument("--api-endpoint", required=True, help="The URL of the external API to test.")
    parser.add_argument("--config", required=True, help="Path to the configuration file (JSON or YAML).")
    parser.add_argument("--input", required=False, help="Path to the input dataset file (CSV or JSON).")
    parser.add_argument("--output", required=False, help="Path to the output file to save predictions (JSON).")
    parser.add_argument("--verbose", action="store_true", help="Increase logging verbosity to debug level.")
    parser.add_argument("--scan", action="store_true", help="Run full Giskard tests on the model predictions.")
    parser.add_argument("--report-file", required=False, help="Path to output the test report (HTML or JSON).")
    args = parser.parse_args()

    global logger
    logger = setup_logging(args.verbose)

    config = load_config(args.config)

    if args.input:
        df = load_dataset(args.input)
    else:
        logger.info("No input file provided; using a sample dataset.")
        df = pd.DataFrame(
            [
                {
                    "world_context": "A mysterious enchanted forest",
                    "genre": "Fantasy",
                    "difficulty": "Medium",
                    "narrative_tone": "Dramatic",
                    "campaign_name": "The Lost Kingdom",
                    "user_question": "What do I do next?",
                },
                {
                    "world_context": "A futuristic cityscape",
                    "genre": "Sci-Fi",
                    "difficulty": "Hard",
                    "narrative_tone": "Grim",
                    "campaign_name": "Cyber Odyssey",
                    "user_question": "How can I infiltrate the enemy headquarters?",
                },
            ]
        )

    dataset = DummyDataset(df)

    def model_predict(input_dataset):
        df_inner = input_dataset.df if hasattr(input_dataset, "df") else input_dataset
        return predict(df_inner, config, args.api_endpoint)

    feature_names = list(df.columns)
    model = create_giskard_model(
        model_name="aissert_model",
        description="A model wrapping API calls for predictions.",
        feature_names=feature_names,
        predict_function=model_predict,
    )

    predictions = model.predict(dataset)
    logger.info("Predictions: %s", predictions)
    print("Predictions:")
    print(predictions)
    serializable_predictions = make_serializable(predictions)
    if args.output:
        try:
            output_file = Path(args.output)
            with output_file.open("w") as fout:
                json.dump(serializable_predictions, fout, indent=2)
            logger.info("Predictions successfully written to %s", args.output)
        except Exception as e:
            logger.error("Failed to write predictions to file: %s", e)

    # Run Giskard tests (scan) on the model.
    if args.scan:
        logger.info("Initiating full Giskard tests...")
        try:
            # run_scan returns an HTML string with the report.
            scan_report = giskard.scan(model=model)
            logger.info("Model tests completed successfully.")
        except Exception as e:
            logger.error("Error during model tests: %s", e)
            scan_report = f"<html><body><h1>Test Error</h1><p>{e}</p></body></html>"

    if args.report_file:
        try:
            # Convert the scan report to a string. If there's a to_html() method, use that.
            report_str = scan_report.to_html() if hasattr(scan_report, "to_html") else str(scan_report)
            report_file = Path(args.report_file)
            with report_file.open("w") as f:
                f.write(report_str)
            logger.info("Test report written to %s", args.report_file)
        except Exception as e:
            logger.error("Failed to write test report to file: %s", e)
    else:
        print("Test Report:")
        print(scan_report.to_html() if hasattr(scan_report, "to_html") else str(scan_report))


if __name__ == "__main__":
    main()
