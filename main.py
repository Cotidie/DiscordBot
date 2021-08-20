import asyncio

async def main():
    print(1)
    task = asyncio.create_task(test())
    print("HELLO")
    await task

async def test():
    await asyncio.sleep(1)
    print("WOW")

async def foo():
    print("FOO")

asyncio.run(main())