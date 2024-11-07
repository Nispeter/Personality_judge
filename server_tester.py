import requests
import json

BASAE_URL = "http://localhost"
BASE_PORT = "5000"

def test_init():
    url = f"{BASAE_URL}:{BASE_PORT}/init"
    data = {
        "task_num": 13,
        "simplification_str": "",
        "num_episodes": 1,
        "env_step_limit": 100,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response = response.json()
        print(response.get("prompt"))
        print(response.get("current_step"))
        print(response.get("is_completed"))
    else :
        print("Failed to initialize environment: ", response.status_code, response.text)

def test_action(action):
    url = f"{BASAE_URL}:{BASE_PORT}/action"
    data = {
        "action": action
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json())
    else :
        print("Failed to get next action: ", response.status_code, response.text)

def test_valid_actions():
    url = f"{BASAE_URL}:{BASE_PORT}/valid_actions"
    response = requests.post(url)
    if response.status_code == 200:
        print(response.json())
    else :
        print("Failed to get valid actions: ", response.status_code, response.text)

def test_step(action):
    url = f"{BASAE_URL}:{BASE_PORT}/step"
    data = {
        "action": action
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response = response.json()
        print(response.get("prompt"))
        print(response.get("current_step"))
        print(response.get("is_completed"))
    else :
        print("Failed to get next action: ", response.status_code, response.text)

if __name__ == "__main__":
    test_init()

    while True: 
        action = input("Enter action: ")
        if action == "exit":
            break
        if action == "init":
            test_init()
        test_step(action)
        