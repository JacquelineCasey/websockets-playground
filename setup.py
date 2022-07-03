# Heroku will see setup.py and recognize the app as a python projects

import connection
import asyncio


async def periodic_messages():
    while True:
        print("Periodic Message")
        await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(connection.main())
