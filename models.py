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
                    <p class="text-lg font-semibold">Task</p>
                    <p>{self.name}</p>
                </div>
              <button class="ml-2 border-zinc-700 border-2 px-2 rounded-md"
                   hx-post="/api"
                   hx-trigger="click"
                   hx-target="#{self.id}"
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
                  hx-target="#{self.id}"
                  hx-swap="outerHTML">
                <div class="flex flex-row">
                    <div class="flex flex-col border-2 rounded-md w-4/12 mx-2 p-2">
                        <label class="text-sm" for="task_name">Task Name</label>
                        <input type="text" value="{self.name}" name="task_name" id="task_name" autofocus onfocus="this.select()"/>
                    </div>
                </div>
                    <div class="bg-black text-white px-4 m-2 py-2 w-1/12 rounded-md">
                        <input type="submit" value="Save" />
                    </div>
             </form>
        </div>
        '''