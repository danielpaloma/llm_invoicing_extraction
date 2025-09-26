import os
from dotenv import load_dotenv
from openai import OpenAI
import yaml
from pathlib import Path
from src.pdf_processing import extract_text_from_pdf, save_text_to_file, extract_texts_from_folder
from src.llm_extraction import load_prompts, llm_data_extraction
from src.excel_helpers import save_json_to_excel

def main():
    #INITIALIZATION:

    # Load YAML config
    print("Initializing...")
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)


    # Assign paths and constants
    INPUT_PATH = Path(config["paths"]["input"]) #input folder with pdf files
    OUTPUT_PATH = Path(config["paths"]["output"]) #output folder for text files
    SYSTEM_PROMPT_PATH = Path(config["paths"]["system_prompt"])
    USER_PROMPT_PATH = Path(config["paths"]["user_prompt"])

    EXCEL_PATH = Path(config["paths"]["excel_output"])
    INVOICES_SHEET = config["sheets"]["invoices_sheet"]
    LINE_ITEMS_SHEET = config["sheets"]["line_items_sheet"]



    # Load variables from .env file
    load_dotenv()

    # Get the API key
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    system_prompt, user_prompt = load_prompts(SYSTEM_PROMPT_PATH, USER_PROMPT_PATH)

    # PROCESSING - CONVERT PDF TO TEXT:
    print("Processing PDFs to extract text...")
    extract_texts_from_folder(INPUT_PATH, OUTPUT_PATH)

    # DATA EXTRACTION:
    
    print("Calling LLM for data extraction...")
    for filename in os.listdir(OUTPUT_PATH):
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(OUTPUT_PATH, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                print(f"Reading text file: {filename}")

                #calling LLM for data extraction
                print("Extracting data using LLM...")
                response = llm_data_extraction(client, system_prompt, user_prompt, text)
                
                # Data validation: only save if response is not None and not empty
                if response:
                    print("Saving extracted data to Excel...")
                    save_json_to_excel(response, filename, EXCEL_PATH, INVOICES_SHEET, LINE_ITEMS_SHEET)
                    #print(f"Response for {filename}: {response}")
                else:
                    print(f"No valid response for {filename}, skipping save.")


if __name__ == "__main__":
    main()
