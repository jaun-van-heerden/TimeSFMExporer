# pip install asyncpg httpx
# python loader.py -n 5 -g 3

import asyncio
import asyncpg
import httpx
import random
import argparse
import os
from typing import List

# Database connection parameters
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/dbname')

async def get_random_file_ids(pool: asyncpg.Pool, num: int) -> List[int]:
    async with pool.acquire() as conn:
        # Fetch all file IDs
        rows = await conn.fetch("SELECT id FROM files")
        file_ids = [row['id'] for row in rows]
        
        # Randomly select 'num' file IDs
        return random.sample(file_ids, min(num, len(file_ids)))

async def send_forecast_request(client: httpx.AsyncClient, file_id: int):
    url = "http://localhost:8000/forecast"  # Adjust this URL as needed
    data = {"fileId": file_id}
    try:
        response = await client.post(url, json=data)
        response.raise_for_status()
        print(f"Forecast request sent for file ID: {file_id}")
    except httpx.RequestError as e:
        print(f"Error sending forecast request for file ID {file_id}: {e}")

async def main(num: int, gap: int):
    async with asyncpg.create_pool(DATABASE_URL) as pool:
        file_ids = await get_random_file_ids(pool, num)
        
        async with httpx.AsyncClient() as client:
            for file_id in file_ids:
                await send_forecast_request(client, file_id)
                if file_id != file_ids[-1]:  # Don't wait after the last request
                    await asyncio.sleep(gap)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send forecast requests for random file IDs")
    parser.add_argument("-n", "--num", type=int, default=5, help="Number of requests to send")
    parser.add_argument("-g", "--gap", type=int, default=3, help="Gap between requests in seconds")
    args = parser.parse_args()

    asyncio.run(main(args.num, args.gap))