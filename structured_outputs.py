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

# Dump the JSON schema from the model and include it in the prompt
json_schema = json.dumps(MCQQuestion.model_json_schema())

# Initialize the client using the latest OpenAI library pointing to your custom Ollama endpoint
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # Required, but unused
)

# Define the prompt including the JSON schema of the expected output
prompt = (
    "Extract ONE multiple-choice question from the given text. "
    "For the question, output a JSON object that conforms to the following JSON schema:\n"
    f"{json_schema}\n"
    "your job is to extract the question and give structured output successfully. Do not attepmt to answer the question. give the valid json"
)

# A more complex sample text with less neatly formatted options
sample_text = """
12. Consider the following statements :  

**Statement-I** :  
Marsupials are not naturally found in India.  

**Statement-II** :  
Marsupials can thrive only in montane grasslands with no predators.  

Which one of the following is correct in respect of the above statements?  

(a) Both Statement-I and Statement-II are correct and Statement-II is the correct explanation for Statement-I  

(b) Both Statement-I and Statement-II are correct and Statement-II is not the correct explanation for Statement-I  

(c) Statement-I is correct but Statement-II is incorrect  

(d) Statement-I is incorrect but Statement-II is correct
"""

logger.info(f"final prompt: {prompt}")

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
    mcq_data = MCQQuestion.model_validate_json(json_string)  # Serialize dict to JSON string
    logger.info(f"mcq_data -> {mcq_data}")
    # Print the validated, structured JSON output
    output = mcq_data.model_dump_json(indent=2)
    logger.info(f"structured_output_json: {output}")
except Exception as e:
    print(f"Error parsing response: {e}")
