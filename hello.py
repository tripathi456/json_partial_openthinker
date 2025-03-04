import os 
from openai import OpenAI
import json
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger
from json_partial_py import to_json_string

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure loguru
log_file = os.path.join(LOG_DIR, "log_{time:YYYY-MM-DD}.log")

# Remove default handler and add our custom handlers
logger.remove()
# Add console handler
logger.add(sink=lambda msg: print(msg, end=""), colorize=True, level="INFO")
# Add file handler with daily rotation
logger.add(
    sink=log_file,
    rotation="00:00",  # Rotate at midnight
    retention="30 days",  # Keep logs for 30 days
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}"
)

# Define Pydantic models for structured JSON response
class Option(BaseModel):
    label: str
    text: str

class MCQQuestion(BaseModel):
    question: str
    options: List[Option]
    answer: Optional[str] = None  # Optional field for the correct answer

class ExtractionResponse(BaseModel):
    questions: List[MCQQuestion]

# Initialize the client using the latest OpenAI library pointing to your custom Ollama endpoint
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # Required, but unused
)

# Define the prompt instructing the backend to extract MCQs in a structured JSON format
prompt = (
    "Extract multiple-choice questions from the given text. "
    "For each question, output a JSON object with the fields: 'question', 'options' "
    "(a list of objects with 'label' and 'text'), and optionally 'answer' if available. "
    "Wrap the results in a top-level 'questions' key."
)

# A more complex sample text with less neatly formatted options
sample_text = """
In an era of rapid technological evolution, digital transformation is reshaping nearly every facet of modern life.
Innovations in fields such as artificial intelligence, big data, and cloud computing have led to profound shifts in both business strategies and everyday routines.
Many experts debate the ethical and practical implications of these advances, especially concerning data privacy and decision-making automation.

One controversial discussion revolves around the challenges of ensuring accountability in AI-driven systems.
Despite extensive research, critics argue that the intricate nature of machine learning models often makes it difficult to trace responsibility when errors occur.

Consider this inquiry: "What is considered the primary ethical challenge when implementing AI for automated decision-making in sensitive domains?"
The potential answers are not clearly formatted: for instance, you might find something like a) over-reliance on automated processes; option b might mention inherent algorithmic bias; 
then c- difficulty in ensuring transparency of decision criteria; and d) perhaps even the absence of robust regulatory frameworks.
"""

# Call the custom backend synchronously using the latest OpenAI client
response = client.chat.completions.create(
    model="openthinker",  # Replace with your desired model if needed
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": sample_text}
    ]
)
logger.info(f"raw_response: {response} ")

# Retrieve the message content from the response
content = response.choices[0].message.content
logger.info(f"raw_content: {content} ")

try:
    # Parse the content as JSON and validate using Pydantic
    json_string = to_json_string(content)
    logger.info(f"to_json_string -> {json_string}")
    json_data = json.loads(json_string)
    logger.info(f"json_data -> {json_data}")
    extraction = ExtractionResponse.model_validate_json(json_data)
    # Print the validated, structured JSON output
    output = extraction.json(indent=2)
    logger.info(f"structured_output: {output}")
except Exception as e:
    print(f"Error parsing response: {e}")
