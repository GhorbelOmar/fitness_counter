import asyncio
import time
import httpx
import pytest
from app.main import app

# Mark the test as asynchronous
@pytest.mark.asyncio
async def test_stress_count_reps():
    """
    Sends 100 concurrent requests to the /count-reps endpoint and
    calculates the average response time.
    """
    num_requests = 100
    request_body = {"data": [{"x": 1, "y": 2, "z": 3}, {"x": 4, "y": 5, "z": 6}]}
    successful_requests = 0

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        tasks = []
        
        start_time = time.time()

        for _ in range(num_requests):
            task = client.post("/count-reps", json=request_body)
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        end_time = time.time()

        for response in responses:
            if response.status_code == 200:
                successful_requests += 1

    assert successful_requests == num_requests, f"Only {successful_requests}/{num_requests} requests were successful."

    total_time = end_time - start_time
    average_response_time = total_time / successful_requests if successful_requests > 0 else 0
    print(f"\nTotal time for {num_requests} requests: {total_time:.4f} seconds")
    print(f"Average response time for {successful_requests} successful requests: {average_response_time:.4f} seconds")


