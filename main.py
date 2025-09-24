import os
from dotenv import load_dotenv
from openai import OpenAI
import yaml
from pathlib import Path
from src.pdf_processing import extract_text_from_pdf, save_text_to_file, extract_texts_from_folder
from src.llm_extraction import load_prompts, llm_data_extraction

def main():
    #INITIALIZATION:

    # Load YAML config
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)


    # Assign paths
    INPUT_PATH = Path(config["paths"]["input"])
    OUTPUT_PATH = Path(config["paths"]["output"])
    SYSTEM_PROMPT_PATH = Path(config["paths"]["system_prompt"])
    USER_PROMPT_PATH = Path(config["paths"]["user_prompt"])

    # Load variables from .env file
    load_dotenv()

    # Get the API key
    api_key = os.getenv("OPENAI_API_KEY")

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # PROCESSING - CONVERT PDF TO TEXT:
    #extract_texts_from_folder(INPUT_PATH, OUTPUT_PATH)

    # DATA EXTRACTION:
    system_prompt, user_prompt = load_prompts(SYSTEM_PROMPT_PATH, USER_PROMPT_PATH)

    for filename in os.listdir(OUTPUT_PATH):
        if filename.lower().endswith('.txt'):
            file_path = os.path.join(OUTPUT_PATH, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                print(f"Reading text file: {filename}")

                yield filename, text
                response = llm_data_extraction(client, system_prompt, user_prompt, text)
                print(f"Response for {filename}: {response}")

    # Example: list available models
    #models = client.models.list()
    #for m in models.data[:5]:
    #    print(m.id)

if __name__ == "__main__":
    main()
