def form(*args):
    return 'form' 

def field(label, id, name, type): 
    return f'''
        <div>
            <label>{label}</label> <input type='{type}' id='{id}' name='{name}'/>
        </div>
    ''' 

def button(text, onclick): 
    return f'''
        <button onclick='{onclick}'>{text}</button>
    '''

template = form(
              field(label='First Name', id='first_name', name='first_name', type='text'), 
              field(label='Last Name', id='last_name', name='last_name', type='text'),
              button(text='submit', onclick='submit')
)

assert template == 'form'
