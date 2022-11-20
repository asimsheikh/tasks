from models import Task

def to_task(form_data: dict[str,str]) -> Task:
    _id = form_data.get('id') 
    name = form_data.get('task_name')
    completed = form_data.get('task_completed')
    pomodoros = form_data.get('task_pomodoros')
    return Task(id=_id, name=name, completed=bool(completed), pomodoros=int(pomodoros))