from nicegui import ui
from ollama import Client

# 1. Ollama Connection
client = Client(host='http://ollama:11434')

# 2. Define your application at the local root
# (The 'root_path' in ui.run will shift this to /owui/ automatically)
@ui.page('/')
def owui_page():
    #ui.dark_mode().auto()
    ui.dark_mode().enable()  # Force dark theme

    with ui.row().classes('w-full items-center mb-4'):
        ui.label('Ollama WebUI').classes('text-h4')

    try:
        response = client.list()
        models = [m['name'] for m in response.get('models', [])]
    except Exception as e:
        ui.notify(f'Ollama connection failed: {e}', color='negative')
        models = []

    with ui.column().classes('w-full max-w-2xl mx-auto'):
        model_select = ui.select(models, label='Select Model').classes('w-full')
        log = ui.log().classes('w-full h-96 border p-4 bg-gray-900 text-white')
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
    # SETTING ROOT_PATH HERE FIXES THE 404 ON ASSETS
    ui.run(
        host='0.0.0.0',
        port=80,
        title='owui',
        reload=False,
        storage_secret='owui_secret_key_123',
        root_path='/owui'  # This prefixes ALL internal assets with /owui
    )

if __name__ in {'__main__', '__mp_main__'}:
    main()
