from nicegui import ui
import asyncio
from datetime import datetime
import httpx
import os
import re
from dotenv import load_dotenv
import json
import logging
from pathlib import Path

# Load environment variables
load_dotenv()

# Backend configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
FASTAPI_ASK_URL = f"{BACKEND_URL}/ask"
FASTAPI_FEEDBACK_URL = f"{BACKEND_URL}/feedback"

print(f"Connecting to backend at: {BACKEND_URL}")

# Add logging configuration
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_DIR / "chat_feedback.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def convert_links_to_html(text):
    """Convert markdown links and plain URLs to HTML links."""
    # First, handle markdown style links: [text](url)
    markdown_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    text = re.sub(markdown_pattern, r'<a href="\2" target="_blank" class="text-blue-500 hover:text-blue-700 underline">\1</a>', text)
    
    # Then handle plain URLs
    url_pattern = r'(https?://[^\s]+)'
    text = re.sub(url_pattern, r'<a href="\1" target="_blank" class="text-blue-500 hover:text-blue-700 underline">\1</a>', text)
    
    return text

class ChatUI:
    def __init__(self):
        self.messages = []
        self.chat_container = None
        self.chat_scroll = None
        self.notification_container = None

    def handle_message(self, msg: str):
        asyncio.create_task(self.send_message(msg))

    async def scroll_to_bottom(self):
        """Scroll to the bottom of the chat container."""
        if self.chat_scroll:
            await self.chat_scroll.scroll(percent=1)

    async def show_notification(self, message: str, type: str = 'positive'):
        """Show notification in the UI."""
        with self.notification_container:
            ui.notification(
                message,
                position='top',
                type=type,
                close_button=True,
                multi_line=True,
                timeout=3000
            )

    async def send_feedback(self, message: str, feedback: str):
        """Log feedback locally instead of sending to backend."""
        try:
            feedback_data = {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "feedback": feedback,
            }
            
            # Log to file
            logging.info(json.dumps(feedback_data))
            
            # Show success notification
            with self.notification_container:
                ui.notification('Feedback logged successfully!', type='positive')
                
        except Exception as e:
            logging.error(f"Error logging feedback: {str(e)}")
            with self.notification_container:
                ui.notification(f'Error logging feedback: {str(e)}', type='negative')

    async def send_message(self, message: str):
        if not message.strip():
            return

        # Create containers if they don't exist
        if self.chat_container is None:
            self.chat_container = ui.column().classes("w-full")

        # Add user message to chat
        with self.chat_container:
            ui.chat_message(
                text=message,
                name="You",
                stamp=datetime.now().strftime("%H:%M"),
            ).classes("w-3/4 bg-blue-100 self-end")

        self.input.value = ""
        await self.scroll_to_bottom()

        try:
            with self.chat_container:
                loading_msg = ui.chat_message(
                    text="Thinking...",
                    name="Bot",
                    stamp=datetime.now().strftime("%H:%M"),
                ).classes("w-3/4")
                await self.scroll_to_bottom()

            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(
                    FASTAPI_ASK_URL,
                    json={"question": message},
                    timeout=30.0,
                )

                loading_msg.delete()

                if response.status_code == 200:
                    bot_response = response.json().get("answer", "No response received.")
                    bot_response_html = convert_links_to_html(bot_response)
                else:
                    bot_response_html = f"Error: {response.status_code}"

            with self.chat_container:
                bot_message = ui.chat_message(
                    text=bot_response_html,
                    name="Bot",
                    stamp=datetime.now().strftime("%H:%M"),
                ).classes("w-3/4").style('word-break: break-word;')

                # Create a container for feedback buttons
                feedback_container = ui.row().classes('gap-2 mt-2')
                with feedback_container:
                    ui.button(
                        "👍 Helpful",
                        on_click=lambda fb=bot_response: asyncio.create_task(
                            self.send_feedback(fb, "helpful")
                        ),
                    ).classes("bg-green-500 text-white hover:bg-green-600")
                    ui.button(
                        "👎 Not Helpful",
                        on_click=lambda fb=bot_response: asyncio.create_task(
                            self.send_feedback(fb, "not helpful")
                        ),
                    ).classes("bg-red-500 text-white hover:bg-red-600")

            await self.scroll_to_bottom()

        except Exception as e:
            print(f"Error: {str(e)}")
            if 'loading_msg' in locals():
                loading_msg.delete()
            
            with self.chat_container:
                ui.chat_message(
                    text=f"Sorry, I encountered an error: {str(e)}",
                    name="Bot",
                    stamp=datetime.now().strftime("%H:%M"),
                ).classes("w-3/4")
                await self.scroll_to_bottom()

    def create_ui(self):
        with ui.column().classes("w-full max-w-3xl mx-auto h-screen p-4"):
            # Create notification container at the top
            self.notification_container = ui.row().classes("w-full justify-center")

            with ui.card().classes("w-full mb-4"):
                ui.label("Highrise FAQ Chatbot").classes("text-2xl font-bold")
                ui.label(f"Environment: {os.getenv('ENVIRONMENT', 'development')}").classes("text-sm text-gray-500")
                ui.label(f"Backend: {BACKEND_URL}").classes("text-sm text-gray-500")

            self.chat_scroll = ui.scroll_area().classes("w-full flex-grow")
            with self.chat_scroll:
                with ui.card().classes("w-full h-full p-4 bg-gray-100"):
                    self.chat_container = ui.column().classes("w-full gap-4")
                    with self.chat_container:
                        ui.chat_message(
                            text="Hello! I'm the Highrise FAQ chatbot. How can I help you today?",
                            name="Bot",
                            stamp=datetime.now().strftime("%H:%M"),
                        ).classes("w-3/4")

            with ui.row().classes("w-full gap-2 mt-4"):
                self.input = ui.input(placeholder="Type your message...").classes("flex-grow")
                self.input.on("keydown.enter", lambda e: self.handle_message(self.input.value))
                ui.button(
                    "Send",
                    on_click=lambda: self.handle_message(self.input.value),
                ).classes("bg-blue-500 text-white hover:bg-blue-600")

@ui.page("/")
def main():
    return ChatUI().create_ui()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=3000,
        reload=False,
        title="Highrise FAQ Chatbot",
    ) 