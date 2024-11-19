from nicegui import ui
import asyncio
from datetime import datetime
import httpx

FASTAPI_ASK_URL = "https://highrise-backend.onrender.com/ask"
FASTAPI_FEEDBACK_URL = "https://highrise-backend.onrender.com/feedback"

class ChatUI:
    def __init__(self):
        self.messages = []
        self.messages_container = None
        self.chat_container = None
    
    def handle_message(self, msg):
        asyncio.create_task(self.send_message(msg))
    
    async def send_message(self, message: str):
        if not message.strip():
            return
        
        # Create containers if they don't exist
        if self.chat_container is None:
            self.chat_container = ui.column().classes('w-full')
            
        # Add user message
        with self.chat_container:
            ui.chat_message(
                text=message,
                name='You',
                stamp=datetime.now().strftime('%H:%M'),
            ).classes('w-3/4 bg-blue-100 self-end')
        
        # Make API call
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    FASTAPI_ASK_URL,
                    json={'question': message},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    bot_response = response.json()['answer']
                else:
                    bot_response = f"Error: {response.status_code}"
                
                # Add bot response
                with self.chat_container:
                    ui.chat_message(
                        text=bot_response,
                        name='Bot',
                        stamp=datetime.now().strftime('%H:%M'),
                    ).classes('w-3/4')
                
        except Exception as e:
            # Add error message
            with self.chat_container:
                ui.chat_message(
                    text=f"Sorry, I encountered an error: {str(e)}",
                    name='Bot',
                    stamp=datetime.now().strftime('%H:%M'),
                ).classes('w-3/4')
        
        # Clear input
        self.input.value = ''
    
    def create_ui(self):
        # Main container
        with ui.column().classes('w-full max-w-3xl mx-auto h-screen p-4'):
            # Header
            ui.label('Highrise FAQ Chatbot').classes('text-2xl font-bold mb-4')
            
            # Chat container
            with ui.card().classes('w-full flex-grow overflow-auto p-4'):
                self.chat_container = ui.column().classes('w-full gap-4')
            
            # Input area
            with ui.row().classes('w-full gap-2 mt-4'):
                self.input = ui.input(placeholder='Type your message...').classes('flex-grow')
                self.input.on('keydown.enter', lambda e: self.handle_message(self.input.value))
                ui.button('Send', on_click=lambda: self.handle_message(self.input.value)) \
                    .classes('bg-blue-500 text-white')

@ui.page('/')
def main():
    return ChatUI().create_ui()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=3000,
        reload=False,
        title="Highrise FAQ Chatbot"
    ) 