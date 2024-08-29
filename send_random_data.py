import requests
import numpy as np
import pandas as pd
import random
import json
from concurrent.futures import ThreadPoolExecutor
from pprint import pprint

host = input("Enter the host: ")

if host == "":
    host = "localhost"

# URL of the endpoint
url = f'http://{host}:8000/forecast'

def generate_random_data():
    # Generate a random numpy array or pandas DataFrame
    #if random.choice([True, False]):
    data = np.random.rand(1, 100)
    #else:
        #data = pd.DataFrame(np.random.rand(1, 50), columns=[f'col_{i}' for i in range(5)])
    
    return data

def generate_random_config():
    # Generate a random config dictionary
    config = {
        "context_len": random.choice([64, 128]),
        "horizon_len": random.choice([16, 32]),
        "input_patch_len": random.choice([32]),
        "output_patch_len": random.choice([128]),
        "num_layers": random.choice([20]),
        "model_dims": random.choice([1280]),
        "backend": random.choice(["cpu"]),
    }
    return config

def send_request():
    # Generate random data and config
    print("Sending request")
    data = generate_random_data()
    config = generate_random_config()

    # Convert data to a list of lists if it's a numpy array
    if isinstance(data, np.ndarray):
        data = data.tolist()

    # Convert data to JSON serializable format if it's a pandas DataFrame
    if isinstance(data, pd.DataFrame):
        data = data.to_dict(orient='records')
    
    # Create the payload
    payload = {
        #"config": config,
        "data": data
    }

    # Send the POST request
    response = requests.post(url, json=payload)

    # Print the response from the server
    print(f'Status Code: {response.status_code}')
    pprint(response.json())
    #print(f'Response: {response.json()}')

if __name__ == "__main__":
    # Use ThreadPoolExecutor to send 3 POST requests concurrently
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(send_request) for _ in range(3)]
        
        # Optionally, wait for all futures to complete
        for future in futures:
            future.result()
