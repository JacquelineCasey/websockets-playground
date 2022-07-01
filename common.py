
import aioconsole # Async Input library


async def print_incoming_messages(websocket):
    async for msg in websocket:
        print(f'[Other] {msg}')


async def send_input(websocket):
    while True:
        msg = await aioconsole.ainput()
        # if (msg == ':quit'):
        #     print('=== Exiting Program ===')
        #     exit(0)
        print (f'\033[1A[You] {msg}\033[K') # Control Sequence. Replaces the printed input line.
        await websocket.send(msg)
