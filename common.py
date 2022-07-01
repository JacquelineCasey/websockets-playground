
import aioconsole # Async Input library


async def print_incoming_messages(websocket):
    # while True:
    #     message = await websocket.recv()
    #     print(message)
    async for message in websocket:
        print(f'[Other] {message}')


async def send_input(websocket):
    while True:
        msg = await aioconsole.ainput()
        print (f'\033[1A[You] {msg}\033[K') # Control Sequence. Replaces the printed input line.
        await websocket.send(msg)
