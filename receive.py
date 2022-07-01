
import asyncio
import websockets
from common import print_incoming_messages, respond_to_input


async def handler(websocket):
    print("=== Connected. ===")
    try:
        await asyncio.gather(print_incoming_messages(websocket), respond_to_input(websocket)) # Do multiple things at once.
    except Exception as e:
        print("=== Something went wrong! ===")
        print(e.with_traceback())
        print("=== End Error Message ===")


async def main():
    print("=== Awaiting Connection... ===")
    async with websockets.serve(handler, '', 8001): # On local machine, navigating to http://jacks-macbook-pro.local:8001 does something interesting.
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
