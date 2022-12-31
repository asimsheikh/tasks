from flask import Flask, request, render_template_string
from persist import Persist

class Repo:
    def __init__(self): 
        self.data = dict(first_name="Asim", last_name="Sheikh")
    
    def get_name(self):
        return self.data

    def update_name(self, first_name: str, last_name: str):
        self.data = dict(first_name=first_name, last_name=last_name)

db = Persist()
app = Flask(__name__)
repo = Repo()

HEAD = '''  
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="x-ua-compatible" content="ie=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <script src="{{url_for('static', filename='tailwindcss.min.js')}}"></script>
        <script src="{{url_for('static', filename='htmx.min.js')}}"></script>
    </head>
''' 

@app.post('/change/<path:subpath>')
def change(subpath: str):
    if subpath == 'legal_name':
        return render_template_string(''' <!-- html -->
        <div id="legal_name">
            <div class="m-4">
                <p class="text-lg">Legal name</p>
                <p class="text-sm">This is the name on your travel document, which could be a licence or a passport.</p>
            </div>
            <form class="m-2 flex flex-col" 
                  hx-post="/change/legal_name/add"
                   hx-target="#legal_name"
                   hx-swap="outerHTML">
                <div class="flex flex-row">
                    <div class="flex flex-col border-2 rounded-md w-4/12 mx-2 p-2">
                        <label class="text-sm" for="first_name">First name</label>
                        <input type="text" value="{{data.first_name}}" name="first_name" id="first_name" autofocus onfocus="this.select()"/>
                    </div>
                    
                    <div class="flex flex-col border-2 rounded-md w-4/12 mx-2 p-2">
                        <label class="text-sm" for="last_name">Surname</label>
                        <input type="text" value="{{data.last_name}}" name="last_name" id="last_name" />
                    </div>
                </div>
                    <div class="bg-black text-white px-4 m-2 py-2 w-1/12 rounded-md">
                        <input type="submit" value="Save" />
                    </div>
            </form>
        </div>
        <!-- !html --> ''', data=repo.get_name())

    elif subpath == 'legal_name/add':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        repo.update_name(first_name=first_name, last_name=last_name )
        page = '''
        <!-- html -->
        
            <div id="legal_name" class="flex">
                <div >
                    <p class="text-lg font-semibold">Legal name</p>
                    <p>{{data.first_name}} {{data.last_name}}</p>
                </div>

              <button class="ml-2 border-zinc-700 border-2 px-2 rounded-md"
                   id="password"
                   hx-post="/change/legal_name"
                   hx-trigger="click"
                   hx-target="#legal_name"
                   hx-swap="outerHTML">Edit</button>
            </div>

        <!-- !html -->     
        '''
        return render_template_string(HEAD + page, data=repo.get_name())
    else:
        return '<div>nothing...</div>'

@app.route('/')
def index():
    page = '''
       <!-- html -->
        <body>
            <div id="legal_name" class="flex">
                <div >
                    <p class="text-lg font-semibold">Legal name</p>
                    <p>{{data.first_name}} {{data.last_name}}</p>
                </div>

              <button class="ml-2 border-zinc-700 border-2 px-2 rounded-md"
                   id="password"
                   hx-post="/change/legal_name"
                   hx-trigger="click"
                   hx-target="#legal_name"
                   hx-swap="outerHTML">Edit</button>
            </div>
        </body>
       <!-- !html -->     
    '''
    return render_template_string(HEAD + page, data=repo.get_name())