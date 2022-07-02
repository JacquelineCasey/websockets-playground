
import aioconsole # Async Input library
import os

class QuitException(Exception):
    pass

BRIGHT_GREEN = '\u001b[32;1m'
BRIGHT_BLUE = '\u001b[34;1m'
BRIGHT_RED = '\u001b[31;1m'
RESET_COLOR = '\u001b[0m'
SHUTDOWN_CODE = f'{BRIGHT_RED}Other User Left the Chat{RESET_COLOR}' # in red


async def print_incoming_messages(websocket):
    async for msg in websocket:
        if msg == SHUTDOWN_CODE:
            print(SHUTDOWN_CODE)
            # raise QuitException("Other ran :quit.")
            return Exception("Other ran :quit")
        print(f'{BRIGHT_GREEN}[Other]{RESET_COLOR} {msg}')
        # os.system(f'say {msg}')

async def redirect_console_input(input_handler):
    while True:
        msg = await aioconsole.ainput()
        await input_handler(msg)
