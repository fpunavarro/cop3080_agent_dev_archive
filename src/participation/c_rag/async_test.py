import asyncio
 
async def greet(name, delay):
    print(f"Hello {name}! (starting)")
    await asyncio.sleep(delay)
    print(f"Hello {name}! (finished after {delay} seconds)")
 
async def main():
    task1 = asyncio.create_task(greet("Alita", 2))
    task2 = asyncio.create_task(greet("Levi", 1))
    task3 = asyncio.create_task(greet("Zenitsu", 3))
 
    await task1
    await task2
    await task3
 
    print("All greetings completed!")
 
asyncio.run(main())
