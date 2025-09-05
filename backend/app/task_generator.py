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
- Clearly indicate the **file involved** (relative path from the root of the repository), e.g., `"main.py"` or `"app.utils/cleaning.py"`. You can only propose **one file** per task.
- If the task involves creating a new file, specify **exactly where to create it**, including the file name.
- Describe **concretely what needs to be done**, avoiding vague or generic phrasing.
- If the task requires programming, only one programming language should be used per task.
- Provide a **time estimate in minutes**.

Do not make any suggestions about requirements.txt or package.json files, as they are not relevant to the task generation.
Write **at most** one task about README.md unless it is demanded by the user in the additional_context.
Write each description in english.
Respond only with a JSON list, without any additional text or explanations. The JSON should look like this:
[
    {{
    "id": id of the tasks (integer)
    "title": "Concise title of the task",
    "file": "relative/path/to/file.py",
    "description": "Exactly what needs to be done",
    "estimated_time": estimated duration in minutes (integer) 
    }},
]
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    reply = response.text.strip()

    return extract_json_from_text(reply)


def generate_code(github_context: str, task: dict) -> str:
    prompt = f"""
You are an expert code generator. Your job is to create code based on the provided GitHub context:
{github_context}

The user has provided a task with the following details:
- Title: {task["title"]}
- File: {task["file"]}
- Description: {task["description"]}
- Estimated Time: {task["estimated_time"]} minutes

Generate the code that fulfills this task. If the task implies the creation of more than one file, provide the code for each file in **the same** response.
Respond only with a JSON, without any additional text or explanations. The JSON should look like this:
{{
    "code": "Respond only with the generated code, without any additional text or explanations.",
    "language": "the programming language of the file (e.g., python, javascript, markdown, etc.) in lowercase"
}}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    reply = response.text.strip()

    return json.loads(reply[7:-3])