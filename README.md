# AIssert

A lightweight testing suite for AI applications to ensure your generative outputs behave as expected.


## Installation

1. Create the virtual environment

Note: giskard currently only supports python versions '<3.13,>=3.9'

```
python3.12 -m venv .venv source .venv/bin/activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Create a test config.json

```
 {
	"input_mapping": {
  	"world_context": "world_context",
  	"genre": "genre",
  	"difficulty": "difficulty",
  	"narrative_tone": "narrative_tone",
  	"campaign_name": "campaign_name",
  	"user_question": "user_question"
	},
	"output_mapping": {
  	"predictions": "narrative"
	},
	"request": {
  	"headers": {
    	"Content-Type": "application/json",
    	"Authorization": "Bearer YOUR_TOKEN"
  	},
  	"method": "POST"
	}
  }
  ```

  4. Test
   
```
cd aissert-cli
python aissert_cli.py --api-endpoint http://localhost:8000/api/dungeon/ --config ./config.json --input ./input.json --output predictions.json --scan --report-file scan_report.html --verbose
```


