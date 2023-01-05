from pydantic import BaseModel, Field, validator

from uuid import uuid4
class Task(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    name: str 
    
    @validator('id')
    def validate_id(cls, v: str | None):
        return uuid4().hex if not v else v
    
    def render(self):
        return f'''
             <div id="{self.id}" class="flex">
                <div>
                    <p>{self.name}</p>
                </div>
              <button class="ml-2 border-zinc-700 border-2 px-2 rounded-md hover:bg-neutral-900 hover:text-neutral-200"
                   hx-post="/api"
                   hx-trigger="click"
                   hx-target="[id='{self.id}']"
                   hx-vals='{{"id": "{self.id}", "action": "edit_task" }}'
                   hx-swap="outerHTML">Edit</button>
              </div>
        '''
    
    def edit(self):
        return f'''
           <div id="{self.id}">
            <div class="m-4">
                <p class="text-lg">Task</p>
                <p class="text-sm">The tasks that you want to do</p>
            </div>
            <form class="m-2 flex flex-col" 
                  hx-post="/api"
                  hx-target="[id='{self.id}']"
                  hx-swap="outerHTML">
                <div class="flex flex-row">
                    <div class="flex flex-col border-2 rounded-md w-4/12 mx-2 p-2">
                        <label class="text-sm" for="task_name">Task Name</label>
                        <input type="text" value="{self.name}" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                        <input type="hidden" id="action" name="action" value="update_task">
                        <input type="hidden" id="id" name="id" value="{self.id}">
                    </div>
                </div>
                    <div>
                        <input class="bg-black text-white px-4 m-2 py-2 w-1/12 rounded-md" type="submit" value="Save" />
                    </div>
             </form>
        </div>
        '''