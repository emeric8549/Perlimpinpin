from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import TaskRequest, TaskSuggestion, TaskChoice
from app.github_utils import clone_and_extract_code
from app.task_generator import generate_tasks, generate_code

app = FastAPI()

last_code = None
tasks = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en dev uniquement !
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-tasks", response_model=list[TaskSuggestion])
async def generate_tasks_endpoint(data: TaskRequest):
    global last_code, tasks
    print(f"In the backend with those data: {data}")
    last_code = clone_and_extract_code(data.github_url)
    if data.additional_context:
        additional_context = f"""The user wants to focus on a specific task (called additional context): **{data.additional_context}**. 
                            You have to take this into account when generating tasks **if and only if** it is **relevant** and **related to the code you've just seen**. 
                            Otherwise, ignore it and continue without taking the additional context into account."""
    else:
        additional_context = ""
    tasks = generate_tasks(last_code, data.time_minutes, additional_context)
    return tasks

@app.post("/generate-code")
async def generate_code_endpoint(choice: TaskChoice):
    global last_code, tasks
    chosen_task = next((task for task in tasks if task["id"] == choice.task_id), None)
    if not chosen_task:
        return {"error": "Task not found"}
    
    generated_code = generate_code(last_code, chosen_task)

    return generated_code
