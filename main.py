import sys

from document_scanner.scanner import DocumentScanner

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_to_scan>")
        sys.exit(1)

    file_path = sys.argv[1]
    scanner = DocumentScanner(extraction_schema_name="yrityksen_taloustiedot")
    result = scanner.scan_document(file_path)

    if result:
        print("Extraction Result:")
        print(result)
    else:
        print("No extraction result obtained.")
