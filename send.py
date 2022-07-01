
import asyncio
import websockets
from common import print_incoming_messages, respond_to_input


HOST = 'jacks-macbook-pro.local' # Could be 'localhost'


async def main():
    print("=== Attempting to Connect to {HOST}... ===")
    async with websockets.connect(f'ws://{HOST}:8001/') as websocket:
        print("=== Connected. ===")
        await asyncio.gather(print_incoming_messages(websocket), respond_to_input(websocket))
        

if __name__ == "__main__":
    asyncio.run(main())
