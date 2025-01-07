from datetime import datetime
from fasthtml.common import *

app, rt = fast_app()

todos = []

class Todo:
    def __init__(self, title, body, due_date=None, is_completed=False):
        self.title = title
        self.body = body
        self.creation_time = datetime.now()
        self.due_date = due_date
        self.is_completed = is_completed

    def toggle_completed(self):
        self.is_completed = not self.is_completed

@rt("/")
def get():
    add_task_form = Form(
        Input(type="text", name="title", placeholder="Todo Title", required=True),
        Textarea(name="body", placeholder="Todo Description", required=True),
        Input(type="datetime-local", name="due_date"),
        Button("Add Task"),
        method="post",
        action="/add-task",
    )

    task_list = Ul(
        *[
            Li(
                f"{task.title}: {task.body} ",
                f"Created: {task.creation_time.strftime('%Y-%m-%d %H:%M:%S')} ",
                f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M:%S') if task.due_date else 'No due date'} ",
                f"Completed: {'✔️' if task.is_completed else 'Pending...'} ",
                A("Delete", href=f"/delete/{i}"),
                A("Mark Complete", href=f"/toggle/{i}"),
            )
            for i, task in enumerate(todos)
        ],
        id="task-list",
    )

    return Titled("ToDo List Tracker", H4("One step at a time."), add_task_form, task_list)


# Add a task
@rt("/add-task", methods=["post"])
def post(title: str, body: str, due_date: str):
    if title and body:
        due_date_obj = datetime.fromisoformat(due_date) if due_date else None
        task = Todo(title, body, due_date=due_date_obj)
        todos.append(task)
    return RedirectResponse(url="/", status_code=303)


# Delete a task
@rt("/delete/{index}", methods=["get"])
def delete(index: int):
    if 0 <= index < len(todos):
        todos.pop(index)
    return RedirectResponse(url="/", status_code=303)


# Marking a task as completed or pending
@rt("/toggle/{index}", methods=["get"])
def toggle(index: int):
    if 0 <= index < len(todos):
        todos[index].toggle_completed()
    return RedirectResponse(url="/", status_code=303)


serve()
