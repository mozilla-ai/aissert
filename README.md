# AIssert

A lightweight testing suite for AI applications to ensure your generative outputs behave as expected.

## Monorepo Structure

This repository contains multiple related packages:

| Package                             | Description                                 |
|-------------------------------------|---------------------------------------------|
| [aissert](./aissert/)               | Core library for AI metrics and assertions  |
| [aissert-cli](./aissert-cli/)       | CLI tool for running AI security tests      |
| [example-pkg](./example-pkg/)       | Example package demonstrating aissert usage |
| [pytest-aissert](./pytest-aissert/) | Pytest plugin for AI testing                |
| [qa_bot](./qa_bot/)                 | Example QA chatbot with AI testing          |

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all workspace dependencies
uv sync --dev
# or via Makefile
make install
```

## Development

Common development tasks are available via the Makefile:

```bash
# Install dependencies
make install

# Run linting and formatting
make lint

# Run all tests
make test

# Run tests for specific package
make test-pytest-aissert
make test-qa-bot
make test-example-pkg

# Clean build artifacts
make clean
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

## Security

For information on reporting security vulnerabilities, please see our [Security Policy](SECURITY.md).

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0). See the [LICENSE](LICENSE) file for details.
