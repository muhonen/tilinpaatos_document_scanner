import sys
import json
import os
from document_scanner.scanner import DocumentScanner

def load_extraction_config(config_path):
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_to_scan>")
        sys.exit(1)

    file_path = sys.argv[1]
    config_path = os.path.join("config", "extraction_config.json")
    extraction_config = load_extraction_config(config_path)
    
    scanner = DocumentScanner(extraction_config)
    result = scanner.scan_document(file_path)
    
    if result:
        print("Extraction Result:")
        print(result)
    else:
        print("No extraction result obtained.")