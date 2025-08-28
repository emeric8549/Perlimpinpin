import os, json, ast, re
from dotenv import load_dotenv
from google import genai

load_dotenv() # Charge la clé API depuis le fichier .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_json_from_text(text: str) -> list[dict]:
    try:
        match = re.search(r'\[\s*{.*?}\s*\]', text, re.DOTALL)
        if match:
            json_text = match.group(0)
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                return ast.literal_eval(json_text)
        else:
            raise ValueError("No valid JSON found in the text.")
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return []
    

def generate_tasks(github_context: str, time_limit: int, additional_context: str) -> list[dict]:
    prompt = f"""
You are an expert task generator. Your job is to create a list of tasks based on the provided GitHub context:
{github_context}

The user has {time_limit} minutes available today to work on this project.
Suggest exactly 3 **independent**, **useful**, and **precise** tasks that can each be completed **individually** in less than {time_limit} minutes. The tasks must last at least {time_limit // 2} minutes each. {additional_context}

For each task:
- Clearly indicate the **file involved** (relative path from the root of the repository), e.g., `"main.py"` or `"app.utils/cleaning.py"`.
- If the task involves creating a new file, specify **exactly where to create it**, including the file name.
- Describe **concretely what needs to be done**, avoiding vague or generic phrasing.
- Provide a **time estimate in minutes**.

Do not make any suggestions about requirements.txt or package.json files, as they are not relevant to the task generation.
Write **at most** one task about README.md.
Write each description in french.
Respond only with a JSON list, without any additional text or explanations. The JSON should look like this:
[
    {{
    "title": "Concise title of the task",
    "file": "relative/path/to/file.py",
    "description": "Exactly what needs to be done",
    "estimated_time": estimated duration in minutes (integer) 
    }},
]
"""
    # print(f"Prompt for Gemini:\n{prompt}\n")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    reply = response.text.strip()

    return extract_json_from_text(reply)