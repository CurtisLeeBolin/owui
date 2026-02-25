from nicegui import ui
from ollama import Client

client = Client(host='http://ollama:11434')

def main():
    ui.label('Ollama WebUI').classes('text-h4')

    # Get models
    try:
        response = client.list()
        models = [m['name'] for m in response['models']]
    except:
        models = []

    # UI Elements
    model_select = ui.select(models, label='Select Model').classes('w-64')
    log = ui.log().classes('w-full h-96 border')
    input_field = ui.input(placeholder='Message...')

    async def send():
        prompt = input_field.value
        input_field.value = ''
        log.push(f'You: {prompt}')

        # Stream response
        response_text = ''
        for chunk in client.chat(
            model=model_select.value,
            messages=[{'role': 'user', 'content': prompt}],
            stream=True
        ):
            content = chunk['message']['content']
            response_text += content

        log.push(f'AI: {response_text}')

    ui.button('Send', on_click=send)

    ui.run(host='0.0.0.0', port=80, title='owui', reload=False)

if __name__ in {'__main__', '__mp_main__'}:
    main()
