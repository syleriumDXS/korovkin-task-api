
import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from psycopg.rows import dict_row


DATABASE_URL = os.environ["DATABASE_URL"]


def connect():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)
    yield


app = FastAPI(title="Task API", lifespan=lifespan)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    completed: bool | None = None


@app.get("/tasks")
def get_tasks():
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with connect() as conn:
        task = conn.execute(
            "SELECT * FROM tasks WHERE id = %s", (task_id,)
        ).fetchone()

    if task is None:
        raise HTTPException(404, "Task not found")

    return task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    with connect() as conn:
        return conn.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING *",
            (task.title,)
        ).fetchone()


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if task.title is None and task.completed is None:
        raise HTTPException(400, "No fields to update")

    with connect() as conn:
        result = conn.execute(
            """
            UPDATE tasks
            SET title = COALESCE(%s, title),
                completed = COALESCE(%s, completed)
            WHERE id = %s
            RETURNING *
            """,
            (task.title, task.completed, task_id)
        ).fetchone()

    if result is None:
        raise HTTPException(404, "Task not found")

    return result


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with connect() as conn:
        result = conn.execute(
            "DELETE FROM tasks WHERE id = %s RETURNING id",
            (task_id,)
        ).fetchone()

    if result is None:
        raise HTTPException(404, "Task not found")

    return {"message": "Task deleted"}
