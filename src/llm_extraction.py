import os
import json

def load_prompts(system_prompt_path, user_prompt_path):
    """
    Reads the system and user prompt .txt files and returns their contents as strings.
    """
    with open(system_prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    with open(user_prompt_path, 'r', encoding='utf-8') as f:
        user_prompt = f.read()
    return system_prompt, user_prompt


def llm_data_extraction(client, system_prompt, user_prompt, text):
    """
    Calls GPT-4o-mini with the given system prompt, user prompt, and text.
    Returns the response as a JSON object.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{user_prompt}\n\n{text}"}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print(f"LLM extraction error: {e}")
        return None





