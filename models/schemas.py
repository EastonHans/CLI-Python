from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Optional


class TaskSchema(BaseModel):
    id: int
    title: str
    status: str = "open"
    assigned_to: List[int] = Field(default_factory=list)


class ProjectSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[str]
    owner_id: Optional[int]
    tasks: List[TaskSchema] = Field(default_factory=list)


class UserSchema(BaseModel):
    id: int
    name: str
    email: Optional[str]
    project_ids: List[int] = Field(default_factory=list)


class DataSchema(BaseModel):
    users: List[UserSchema]
    projects: List[ProjectSchema]
