from models import Task, Notes

def to_task(form_data: dict[str,str]) -> Task:
    _id = form_data.get('id') 
    name = form_data.get('task_name')
    completed = form_data.get('task_completed')
    pomodoros = form_data.get('task_pomodoros')
    return Task(id=_id, name=name, completed=bool(completed), pomodoros=int(pomodoros))

def to_note(form_data: dict[str, str]) -> Notes:
    _id = form_data.get('id')
    date = form_data.get('notes_date')
    text = form_data.get('notes_text')
    task_id = form_data.get('notes_task_id')
    if _id:
        return Notes(id=_id, date=date, text=text, task_id=task_id)
    else:
        return Notes(date=date, text=text, task_id=task_id)

    