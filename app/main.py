from fastapi import FastAPI
from app.schemas import TaskRequest, TaskSuggestion
from app.github_utils import clone_and_extract_code
from app.task_generator import generate_tasks

app = FastAPI()

@app.post("/generate-tasks", response_model=list[TaskSuggestion])
def generate_tasks_endpoint(data: TaskRequest):
    code = clone_and_extract_code(data.github_url)
    suggestions = generate_tasks(code, data.time_minutes)
    return suggestions