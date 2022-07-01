
import asyncio
import sys
import websockets

from common import print_incoming_messages, send_input


HOST = 'jacks-macbook-pro.local' # Could be 'localhost'


async def send_and_receive_messages(websocket):
    try:
        print('=== Connected. ===')
        await asyncio.gather( # Do multiple things at once.
            print_incoming_messages(websocket), 
            send_input(websocket)
        )

    except Exception as e:
        print("=== Something went wrong! ===")
        print(e.with_traceback())
        print("=== End Error Message ===")


def help():
    print('Unrecognized or missing command line argument: ')
    print('Use send mode with "--send" or "-s", and use receive mode with "--receive" or "-r".')
    print('Ex: python3.10 console.py s')
    exit(1)


async def main():
    if len(sys.argv) < 2:
        help()

    match sys.argv[1] or "none":
        case '--receive' | '-r': 
            print("=== Awaiting Connection... ===")
            async with websockets.serve(send_and_receive_messages, '', 8001): # On local machine, navigating to http://jacks-macbook-pro.local:8001 does something interesting.
                await asyncio.Future()  # run forever
        case '--send' | '-s':
            print(f'=== Attempting to Connect to {HOST}... ===')
            async with websockets.connect(f'ws://{HOST}:8001/') as websocket:
                await send_and_receive_messages(websocket)
        case _:
            help()

                
if __name__ == "__main__":
    asyncio.run(main())
