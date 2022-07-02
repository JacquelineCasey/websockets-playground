
import asyncio
import sys
import websockets

from common import *


HOST = 'jacks-macbook-pro.local' # Could be 'localhost'


async def send_and_receive_messages(websocket, keep_alive = None):
    try:
        print('=== Connected. ===')
        print(f'{BRIGHT_RED}Note:{RESET_COLOR} End the session by typing \":quit\"')
        await asyncio.gather( # Do multiple things at once. Any error is raised immediately
            print_incoming_messages(websocket), 
            send_input(websocket),
        )
    except QuitException:
        print('=== Exiting Program ===')
    except Exception as e:
        print("=== Something went wrong! ===")
        print(e.with_traceback())
        print("=== End Error Message ===")
    finally: # Quit the server after first websocket dies for any reason.
        if keep_alive:
            keep_alive.set_result(None)

def help():
    print('Unrecognized or missing command line argument: ')
    print('Use send mode with "--send" or "-s", and use receive mode with "--receive" or "-r".')
    print('Ex: python3.10 console.py s')
    exit(1)

async def main():
    if len(sys.argv) < 2:
        help()

    match sys.argv[1]:
        case '--receive' | '-r': 
            print("=== Awaiting Connection... ===")
            keep_alive = asyncio.Future()

            async with websockets.serve(lambda ws: send_and_receive_messages(ws, keep_alive), '', 8001): # On local machine, navigating to http://jacks-macbook-pro.local:8001 does something interesting.
                await keep_alive  # run until keep_alive.set_result()
        case '--send' | '-s':
            print(f'=== Attempting to Connect to {HOST}... ===')
            async with websockets.connect(f'ws://{HOST}:8001/') as websocket:
                await send_and_receive_messages(websocket)
        case _:
            help()

                
if __name__ == "__main__":
    asyncio.run(main())
