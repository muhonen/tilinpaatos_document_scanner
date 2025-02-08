import os
from PIL import Image
from .pdf_utils import extract_text_from_pdf, convert_pdf_to_images
from .openai_utils import process_text_with_openai, process_image_with_gpt4

class DocumentScanner:
    def __init__(self, extraction_config):
        """
        Initialize with a configuration dict that specifies what fields to extract.
        """
        self.extraction_config = extraction_config

    def scan_document(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = extract_text_from_pdf(file_path)
            if text:
                print("Text layer found in PDF. Processing text...")
                return process_text_with_openai(text, self.extraction_config)
            else:
                print("No text found; assuming scanned PDF. Converting to images...")
                images = convert_pdf_to_images(file_path)
                results = []
                for idx, img in enumerate(images):
                    print(f"Processing page {idx + 1} as image...")
                    res = process_image_with_gpt4(img, self.extraction_config)
                    if res:
                        results.append(res)
                return "\n".join(results)
        elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
            try:
                image = Image.open(file_path)
            except Exception as e:
                print(f"Error opening image: {e}")
                return None
            print("Processing image file...")
            return process_image_with_gpt4(image, self.extraction_config)
        else:
            print("Unsupported file format.")
            return None