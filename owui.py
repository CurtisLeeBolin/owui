from nicegui import app, ui
from ollama import Client

# 1. Ollama Connection
client = Client(host='http://ollama:11434')

# 2. Force the subpath for ALL assets and routes
# This ensures NiceGUI looks for assets at /owui/_nicegui instead of /_nicegui
app.root_path = '/owui'

@ui.page('/')
def owui_page():
    '''
    Because app.root_path is set to /owui, this handler
    automatically serves at http://domain.org
    '''
    ui.label('Ollama WebUI').classes('text-h4 mb-4')

    try:
        response = client.list()
        models = [m['name'] for m in response.get('models', [])]
    except Exception as e:
        ui.notify(f'Ollama connection failed: {e}', color='negative')
        models = []

    with ui.column().classes('w-full max-w-2xl mx-auto'):
        model_select = ui.select(models, label='Select Model').classes('w-full')
        log = ui.log().classes('w-full h-96 border p-4 bg-gray-50')
        input_field = ui.input(placeholder='Type a message...').classes('w-full')

        async def send():
            prompt = input_field.value
            if not prompt or not model_select.value:
                return

            input_field.value = ''
            log.push(f'You: {prompt}')

            full_response = ""
            try:
                for chunk in client.chat(
                    model=model_select.value,
                    messages=[{'role': 'user', 'content': prompt}],
                    stream=True
                ):
                    content = chunk['message']['content']
                    full_response += content

                log.push(f'AI: {full_response}')
            except Exception as e:
                ui.notify(f'Error: {e}', color='negative')

        ui.button('Send', on_click=send).classes('w-full mt-2')

def main():
    ui.run(
        host='0.0.0.0',
        port=80,
        title='owui',
        reload=False,
        storage_secret='owui_secret_key'
    )

if __name__ in {'__main__', '__mp_main__'}:
    main()
