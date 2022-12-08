from models import Task, Notes, Contact

def to_task(form_data: dict[str,str]) -> Task:
    _id = form_data.get('id') or '' 
    name = form_data.get('task_name') or ''
    completed = form_data.get('task_completed') or False
    pomodoros = form_data.get('task_pomodoros') or 0
    return Task(id=_id, name=name, completed=completed == 'True', pomodoros=int(pomodoros))

def to_note(form_data: dict[str, str]) -> Notes:
    _id = form_data.get('id')
    date = form_data.get('notes_date')
    text = form_data.get('notes_text')
    task_id = form_data.get('notes_task_id')
    if _id:
        return Notes(id=_id, date=date, text=text, task_id=task_id)
    else:
        return Notes(date=date, text=text, task_id=task_id)

def to_contact(form_data: dict[str, str]) -> Contact:
    _id = form_data.get('contact_id')
    first_name = form_data.get('contact_first_name') or ''
    last_name = form_data.get('contact_last_name') or ''
    email = form_data.get('contact_email') or ''
    if _id:
        return Contact(id=_id, first_name=first_name, last_name=last_name, email=email)
    else:

        return Contact(first_name=first_name, last_name=last_name, email=email)