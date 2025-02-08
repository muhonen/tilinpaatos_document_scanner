from dotenv import load_dotenv
load_dotenv()  # This will load variables from the .env file into os.environ

import os
import json
import base64
from io import BytesIO
import openai
from PIL import Image

# Get OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_text_with_openai(text, extraction_config):
    """
    Sends extracted text to the OpenAI API to extract structured data.
    The extraction_config (dict) specifies what fields to extract.
    """
    prompt = (
        f"Extract the following fields as JSON: {json.dumps(extraction_config)}\n\n"
        f"Document text:\n{text}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or another appropriate model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error processing text with OpenAI: {e}")
        return None

def process_image_with_gpt4(image, extraction_config):
    """
    Sends an image to the OpenAI API for OCR and structured extraction.
    Returns the API's response.
    
    Note: The image processing API and model identifier might change; adjust as needed.
    """
    # Convert image to JPEG base64 string
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    prompt = f"Extract the following fields as JSON: {json.dumps(extraction_config)}"
    
    # Construct the message for a multimodal (text + image) API call
    message = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}", "detail": "high"}}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-11-20",  # Example model name for image-enabled GPT-4o
            messages=[{"role": "user", "content": message}],
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error processing image with OpenAI: {e}")
        return None