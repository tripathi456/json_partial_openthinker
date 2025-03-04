# OpenThinker JSON Partial Python

A Python library for extracting structured data from text using the OpenAI API with a local Ollama model. This project specifically focuses on extracting multiple-choice questions (MCQs) from unstructured text and validating them against a defined schema.

## Features

- Extract MCQs from unstructured text
- Validate extracted data against Pydantic models
- Parse partial JSON responses using json-partial-python
- Comprehensive logging with loguru

## Requirements

- Python 3.13+
- Ollama running locally with the "openthinker" model

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd openthinker-json-partial-py

# Install dependencies
pip install -e .
```

## Usage

The project includes two example scripts:

### 1. Extract a Single MCQ

```python
# Run the structured_outputs.py script
python structured_outputs.py
```

This script extracts a single MCQ from a sample text and validates it against a defined schema.

### 2. Extract Multiple MCQs

```python
# Run the hello.py script
python hello.py
```

This script extracts multiple MCQs from a sample text and validates them against a defined schema.

## Project Structure

- `structured_outputs.py`: Example script for extracting a single MCQ
- `hello.py`: Example script for extracting multiple MCQs
- `logs/`: Directory for log files
- `pyproject.toml`: Project configuration and dependencies

## Dependencies

- json-partial-python: For parsing partial JSON responses
- loguru: For logging
- openai: For interacting with the OpenAI API
- pydantic: For data validation
- requests: For HTTP requests

## License

[Add license information here]

## Contributing

[Add contribution guidelines here]