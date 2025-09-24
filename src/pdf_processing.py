import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file. Uses OCR for scanned PDFs.
    Returns the extracted text as a string.
    """
    text = ""
    try:
        # Try extracting text using PyPDF2 (works for native PDFs)
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        # If no text was found, try OCR
        if not text.strip():
            images = convert_from_path(pdf_path)
            for image in images:
                text += pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
    return text

def save_text_to_file(text, pdf_path, output_folder):
    """
    Saves the extracted text to a .txt file in the specified output folder.
    The .txt file will have the same base name as the PDF.
    """
    os.makedirs(output_folder, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_path = os.path.join(output_folder, f"{base_name}.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
        print(f"Text file saved: {base_name}.txt")

def extract_texts_from_folder(folder_path, output_folder):
    """
    Extracts text from all PDF files in a folder and saves each as a .txt file in output_text.
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}...")
            text = extract_text_from_pdf(pdf_path)
            save_text_to_file(text, pdf_path, output_folder)
