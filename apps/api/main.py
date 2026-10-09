from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from database import get_connection


app = FastAPI()

class Task(BaseModel):
    title: str
    completed: bool = False
    priority: int = 3


class TaskUpdate(BaseModel):
    completed: bool


tasks = []

@app.get("/")
def root():
    return {"message": "OscarOS API is running"}

@app.get("/tasks")
def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                select id, title, completed, priority
                from tasks
                order by id;
                """)
            rows = cursor.fetchall()

    return rows


@app.post("/tasks", status_code=201)
def create_task(task: Task):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, completed, priority)
                VALUES (%s, %s, %s)
                RETURNING id, title, completed, priority
                """,
                (task.title, task.completed, task.priority)
            )

            row = cursor.fetchone()
    return row

@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """UPDATE tasks
                SET completed = %s
                WHERE id = %s
                RETURNING id, title, completed, priority;
                """,
                (task.completed, task_id)
            )

            row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return row

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """DELETE FROM tasks
                WHERE id = %s
                RETURNING id;
                """,
                (task_id, )
            )

            row = cursor.fetchone()

        if row in None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )