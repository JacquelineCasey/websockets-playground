
import aioconsole # Async Input library


async def print_incoming_messages(websocket):
    # while True:
    #     message = await websocket.recv()
    #     print(message)
    async for message in websocket:
        print(f'[Other] {message}')


async def respond_to_input(websocket):
    while True:
        msg = await aioconsole.ainput()
        print(f'[You] {msg}')
        await websocket.send(msg)
