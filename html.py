def div(
        *args,
        id: str | None = None, 
        class_: str | None = None,
        hx_post:str | None = None, 
        hx_target: str | None = None, 
        __: list[str] | None = None) -> str:
    items: str = ''.join([x for x in args or []])
    return f'<div id="{id}" class="{class_}" hx-post="{hx_post}" hx-target="{hx_target}">{items}</div>' 

def p(text: str, class_: str | None = None) -> str:
    return f'<p class="{class_}">{text}</p>'

# print(
#     div(id='pebbles', class_='flex grow m-2', hx_post='/pebbles', hx_target='#pebbles', __=
#        [p(f'Hello world {x}') for x in range(10)] 
# ))

# div(
#     p('hello world'),
#     p('nothing here'),
#     p('adding items'),
#     div(
#         p('Here we are'),
#         form(
#             input(id=1, name='hello', value=''),
#             input(id=2, name='lastname', value='Sheikh')
#             button(text='Enter name')
#         )
#     ),
# )