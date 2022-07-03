# Heroku will see setup.py and recognize the app as a python projects

import connection
import asyncio
import sys


async def periodic_messages():
    while True:
        print("Periodic Message")
        await asyncio.sleep(10)

async def main():
    await asyncio.gather(periodic_messages())

if __name__ == '__main__':
    asyncio.run(main())
