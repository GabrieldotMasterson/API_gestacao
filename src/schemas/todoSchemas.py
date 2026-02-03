from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.models.todoModel import TodoState



class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterTodo(FilterPage):
    title: str | None = Field(None, min_length=3, max_length=20)
    description: str | None = Field(None, min_length=3, max_length=20)
    state: TodoState | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
