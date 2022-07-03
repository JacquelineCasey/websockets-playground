
import asyncio
from traceback import print_exc
import websockets

class Connection():
    _next_id = 1

    def __init__(self, websocket, on_receive=None, on_closed=None) -> None:
        self._websocket = websocket
        self._send_queue = asyncio.Queue()
        self._on_receive = on_receive
        self._on_closed = on_closed
        self._ended = False
        self.id = Connection._next_id
        Connection._next_id += 1

    async def activate(self):
        self._gathered_tasks = asyncio.gather(self._send_messages(), self._receive_messages(), self._wait_closed())
        try:
            await self._gathered_tasks # May be cancelled by end_connection()
        except Exception as e:
            print(f'Connection with id {self.id} encountered an exception.')
            print_exc(e)
        except asyncio.CancelledError: # Strangly not itself an Exception
            pass # We are fine with this actually. This is how the Connection shuts down.
        finally:
            self.end_connection()
            await self._websocket.close()
            if self._on_closed:
                self._on_closed(self)

    async def _receive_messages(self):
        async for msg in self._websocket:
            if self._on_receive:
                self._on_receive(msg, self)

    async def _send_messages(self):
        while True:
            msg = await self._send_queue.get()
            await self._websocket.send(msg)
            self._send_queue.task_done()

    async def _wait_closed(self):
        await self._websocket.wait_closed()
        self.end_connection()

    def send_message(self, msg):
        self._send_queue.put_nowait(msg)

    def end_connection(self):
        if not self._ended:
            self._ended = True
            self._gathered_tasks.cancel()
            # Cancelling the gather will cause activate() to progress. It also cancels all gathered tasks.


# Test / Example of Usage

# A simple server (later we will make a full server class). Prints 'Connection Opened'
# and 'Connection Closed' appropriately. Prints received messages, and echos them.
# Connections are closed gracefully, and multiple parallel connections are supported.
# Receiving the string 'exit' also triggers closing. 
# Test with `python3 -m websockets 127.0.0.1:8001` in another shell.

async def main():
    def on_receive_msg(msg, connection: Connection):
        print(f'[{connection.id}] received {msg}')
        connection.send_message(f'echo {msg}')
        if msg == 'exit':
            connection.end_connection()

    def on_closed(connection: Connection):
        print(f'[{connection.id}] Connection Closed')

    async def handle_ws(websocket): 
        connection = Connection(websocket, on_receive_msg, on_closed)
        print(f'[{connection.id}] Connection Opened') 
        await connection.activate()

    async with websockets.serve(handle_ws, '', 8001):
        await asyncio.Future() # suspend indefinitely

if __name__ == '__main__':
    asyncio.run(main())
