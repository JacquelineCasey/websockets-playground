
import asyncio
import websockets


async def main():
    async with websockets.connect('ws://localhost:8001/') as websocket:
        while True:
            msg = input()
            print(msg)
            await websocket.send(msg)
        

if __name__ == "__main__":
    asyncio.run(main())