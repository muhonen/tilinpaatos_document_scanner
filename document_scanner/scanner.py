import asyncio
import json
import os

from PIL import Image

from .openai_utils import (process_image_with_gpt4, process_images_with_gpt4,
                           process_text_with_openai)
from .pdf_utils import convert_pdf_to_images, extract_text_from_pdf


class DocumentScanner:
    def __init__(self, extraction_schema_name):
        self.extraction_schema_name = extraction_schema_name

    def scan_document(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
            if text:
                print("Text layer found in PDF. Processing text...")
                result = process_text_with_openai(text, self.extraction_schema_name)
                return (
                    json.dumps(json.loads(result), indent=2)
                    if result is not None
                    else None
                )
            else:
                print("No text found; assuming scanned PDF. Converting to images...")
                images = convert_pdf_to_images(file_path)
                print(f"Converted PDF to {len(images)} images.")
                return asyncio.run(self.async_process_images(images))
        elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
            try:
                image = Image.open(file_path)
            except Exception as e:
                print(f"Error opening image: {e}")
                return None
            print("Processing image file...")
            result = process_image_with_gpt4(image, self.extraction_schema_name)
            return (
                json.dumps(json.loads(result), indent=2) if result is not None else None
            )
        else:
            print("Unsupported file format.")
            return None

    async def async_process_images(self, images):
        print("Starting async image processing...")
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, process_images_with_gpt4, images, self.extraction_schema_name
        )
        print("Finished async image processing.")
        return json.dumps(json.loads(result), indent=2) if result is not None else None
