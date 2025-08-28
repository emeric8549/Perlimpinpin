from pydantic import BaseModel, HttpUrl

class TaskRequest(BaseModel):
    github_url: HttpUrl
    time_minutes: int
    additional_context: str | None = None

class TaskSuggestion(BaseModel):
    title: str
    file: str
    description: str
    estimated_time: int # in minutes
