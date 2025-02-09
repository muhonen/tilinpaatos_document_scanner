import base64
import json
import os
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

from .extraction_structures import extraction_schema
from .prompts import get_prompt

load_dotenv()
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def prepare_image(image, target_width=1200, quality=300, grayscale=True):
    """
    Resize the image if its width exceeds target_width, convert to grayscale if requested,
    and return the processed image.
    """
    width, height = image.size
    if width > target_width:
        new_height = int((target_width / width) * height)
        image = image.resize(
            (target_width, new_height), resample=Image.Resampling.LANCZOS
        )
    if grayscale:
        image = image.convert("L")
    return image


def process_text_with_openai(text, extraction_schema_name):
    """
    Process text using GPT-4o-mini and return the API response.
    """
    prompt = get_prompt()
    json_schema = extraction_schema(extraction_schema_name)
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "yrityksen_taloustiedot", "schema": json_schema},
        },
        max_tokens=1500,
    )
    return response.choices[0].message.content


def process_image_with_gpt4(image, extraction_schema_name):
    """
    Process a single image using GPT-4o-mini.
    The image is resized, converted to grayscale, compressed, and encoded to base64.
    """
    prepared_image = prepare_image(image, target_width=1200, quality=30, grayscale=True)
    buffered = BytesIO()
    prepared_image.save(buffered, format="JPEG", quality=300)
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    prompt = get_prompt()
    messages = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": f"data:image/jpeg;base64,{img_str}",
            "image_url": {"detail": "low"},
        },
    ]
    json_schema = extraction_schema(extraction_schema_name)
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "yrityksen_taloustiedot", "schema": json_schema},
        },
        max_tokens=1500,
    )
    return response.choices[0].message.content


def process_images_with_gpt4(images, extraction_schema_name):
    """
    Process multiple images in a single API call.
    The images are processed as a single user message whose content is an array of a text prompt
    followed by multiple image objects.
    """
    prompt = get_prompt()
    messages = [{"role": "system", "content": prompt}]
    # Build a single user message with an array of objects
    user_content = [{"type": "text", "text": prompt}]
    for image in images:
        prepared_image = prepare_image(
            image, target_width=1200, quality=300, grayscale=True
        )
        buffered = BytesIO()
        prepared_image.save(buffered, format="JPEG", quality=300)
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        user_content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_str}",
                    "detail": "low",
                },
            }
        )
    messages.append({"role": "user", "content": user_content})
    json_schema = extraction_schema(extraction_schema_name)
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "yrityksen_taloustiedot", "schema": json_schema},
        },
        max_tokens=2000,
    )
    return response.choices[0].message.content
