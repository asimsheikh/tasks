def form(*args, post):
    innerHTML = ''.join(arg for arg in args)
    return f'''<form hx-post={post}>
                 {innerHTML}
               </form>'''

def field(label, id, name, type='text', value='', autofocus=False): 
    return f'''
        <div>
            <label>{label}</label> <input type='{type}' id='{id}' name='{name}' value='{value}' {'autofocus' if autofocus else ''}/>
        </div>
    ''' 

def button(class_,text, onclick): 
    return f''' <button class='{class_}' onclick='{onclick}'>{text}</button> '''
