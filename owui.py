from nicegui import ui
from ollama import Client

# Connect to your separate Ollama container
client = Client(host='http://ollama:11434')

# Use this decorator to define the home page route
@ui.page('/owui/')
def home_page():
    ui.label('Ollama WebUI').classes('text-h4 mb-4')

    # 1. Fetch models
    try:
        response = client.list()
        models = [m['name'] for m in response.get('models', [])]
    except Exception as e:
        ui.notify(f'Ollama connection failed: {e}', color='negative')
        models = []

    # 2. UI Layout
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

            full_response = ''
            try:
                # The ollama client.chat is a blocking generator,
                # wrapping it in a thread or running it simply:
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
    # Start the server - it will now correctly find the @ui.page('/') route
    ui.run(host='0.0.0.0', port=80, title='owui', reload=False)

if __name__ in {'__main__', '__mp_main__'}:
    main()
