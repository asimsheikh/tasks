from uuid import uuid4
from typing import Optional

from pydantic import BaseModel
from flask import Flask, render_template, request, jsonify

class Task(BaseModel):
    id: Optional[str] = uuid4().hex
    name: str 
    completed: bool
    pomodoros: int

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        return jsonify(request.form) 
    return 'api route'