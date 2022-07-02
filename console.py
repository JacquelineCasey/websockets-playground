
import asyncio
import sys
from traceback import print_exc
import websockets

from common import *


HOST = 'jacks-macbook-pro.local' # Could be 'localhost'


class InputHandler():
    websocket = None
    task = None
    quit_handler = None

    async def handle_input(self, msg):
        if (msg == ':quit'):
            if self.websocket.open:
                await self.websocket.send(SHUTDOWN_CODE)
            self.quit_handler()
            return
        print (f'\033[1A{BRIGHT_BLUE}[You]{RESET_COLOR} {msg}\033[K') # Control Sequence replaces the printed input line.
        if self.websocket.open:
            await self.websocket.send(msg)
    
    
input_handler = None

async def send_and_receive_messages(websocket, keep_alive = None): 
    print('=== Connected. ===')
    print(f'{BRIGHT_RED}Note:{RESET_COLOR} End the session by typing \":quit\"')

    receive_task = asyncio.gather(print_incoming_messages(websocket))

    def kill_server():
        if keep_alive:
            keep_alive.set_result(None)
            receive_task.cancel()

    # Ensure that the input is printed on the screen and sent to partner
    global input_handler
    if not input_handler:
        input_handler = InputHandler()
        asyncio.create_task(redirect_console_input(input_handler.handle_input))
        input_handler.quit_handler = kill_server

    input_handler.websocket = websocket

    try:
        await receive_task # side effect: releases exception immediately
    except QuitException:
        print('=== Exiting Program ===')
        kill_server()
    except Exception as e:
        print("=== Something went wrong! ===")
        print_exc(e)
        print("=== End Error Message ===")


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
