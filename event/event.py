import asyncio
from datetime import datetime

print('testtttttt', flush=True)

async def event():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Event triggered at: " + timestamp, flush=True)

# Create and run the event loop
async def main():
    # Run the event loop
    while True:
        await event()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())