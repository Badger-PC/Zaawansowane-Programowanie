import asyncio
import aiohttp
import time
import random

API_URL = "http://localhost:8000/detect-url-async"
IMAGE_URLS = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_March_2010-1.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/June_odd-eyed-cat.jpg/1200px-June_odd-eyed-cat.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Zebra_Botswana_EDITED.jpg/1200px-Zebra_Botswana_EDITED.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/e/e1/African_Elephant_Maasai_Mara.jpg"
]

TOTAL_REQUESTS = 100 
CONCURRENCY = 20 # Lower concurrency for local execution

async def send_request(session, i):
    url = random.choice(IMAGE_URLS)
    try:
        async with session.post(API_URL, params={"url": url}) as response:
            if response.status == 200:
                data = await response.json()
                return True
            else:
                print(f"Request {i} failed: {response.status}")
                return False
    except Exception as e:
        print(f"Request {i} error: {e}")
        return False

async def main():
    print(f"Starting load test with {TOTAL_REQUESTS} requests...")
    start_time = time.time()
    
    conn = aiohttp.TCPConnector(limit=CONCURRENCY)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [send_request(session, i) for i in range(TOTAL_REQUESTS)]
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    duration = end_time - start_time
    check_count = sum(results)
    
    print(f"\nFinished load test.")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Successful: {check_count}")
    print(f"Failed: {TOTAL_REQUESTS - check_count}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"RPS: {TOTAL_REQUESTS / duration:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
