
import aioconsole # Async Input library


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
            raise QuitException("Other ran :quit.")
        print(f'{BRIGHT_GREEN}[Other]{RESET_COLOR} {msg}')

async def send_input(websocket):
    while True:
        msg = await aioconsole.ainput()
        if (msg == ':quit'):
            await websocket.send(SHUTDOWN_CODE)
            raise QuitException("User ran :quit.")
        print (f'\033[1A{BRIGHT_BLUE}[You]{RESET_COLOR} {msg}\033[K') # Control Sequence replaces the printed input line.
        await websocket.send(msg)
