from time import sleep

import typer
from plyer import notification

import data_manager
from main import app
from data_manager import *

@app.command(name="add", help="Add task")
def add_task(task: str = typer.Argument(...), notify: str = typer.Option(False)):
    tasks: dict = data_manager.get_tasks()
    if task in tasks:
        typer.echo(f"Task {task} already exists.")
        return

    tasks[task] = False
    data_manager.update_tasks(tasks)
    typer.echo("Task added.")

    if notify:
        notification.notify(
            title="clitm",
            message="You have to" + task,
            timeout=10
        )

@app.command(name="delete", help="Delete task")
def delete_task(task: str = typer.Argument(...)):
    tasks: dict = data_manager.get_tasks()
    if task not in tasks:
        typer.echo(f"Task {task} is not exists.")
        return

    tasks.pop(task)
    data_manager.update_tasks(tasks)
    typer.echo("Task deleted.")

@app.command(name="show", help="Show all tasks")
def show_tasks():
    tasks: dict = data_manager.get_tasks()
    for task in tasks:
        typer.echo(f"Task: {task} " + ("✓" if task == True else "✗"))


@app.command(name="done", help="Done task")
def done_task(task: str = typer.Argument(...)):
    tasks: dict = data_manager.get_tasks()
    if task not in tasks:
        typer.echo(f"Task {task} is not exists.")
        return

    tasks[task] = True
    typer.echo("Task done.")


@app.command(name="undone", help="Undo task")
def undone_task(task: str = typer.Argument(...)):
    tasks: dict = data_manager.get_tasks()
    if task not in tasks:
        typer.echo(f"Task {task} is not exists.")
        return

    tasks[task] = False
    typer.echo("Task undone.")