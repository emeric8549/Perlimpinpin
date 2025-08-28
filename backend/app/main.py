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
async def generate_tasks_endpoint(data: TaskRequest):
    print(f"In the backend with those data: {data}")
    code = clone_and_extract_code(data.github_url)
    if data.additional_context:
        additional_context = f"""The user wants to focus on a specific task (called additional context): **{data.additional_context}**. 
                            You have to take this into account when generating tasks **if and only if** it is **relevant** and **related to the code you've just seen**. 
                            Otherwise, ignore it and continue without taking the additional context into account."""
    else:
        additional_context = ""
    suggestions = generate_tasks(code, data.time_minutes, additional_context)
    return suggestions