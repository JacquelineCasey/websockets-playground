# Heroku will see setup.py and recognize the app as a python projects

import connection
import asyncio


if __name__ == '__main__':
    asyncio.run(connection.main())
