from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import TaskRequest, TaskSuggestion
from app.github_utils import clone_and_extract_code
from app.task_generator import generate_tasks

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en dev uniquement !
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-tasks", response_model=list[TaskSuggestion])
def generate_tasks_endpoint(data: TaskRequest):
    print(f"In the backend with those data: {data}")
    code = clone_and_extract_code(data.github_url)
    suggestions = generate_tasks(code, data.time_minutes)
    return suggestions
