import requests

class APIClient:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url

    def get_users(self):
        response = requests.get(f"{self.base_url}/users")
        return response

    def get_user(self, user_id):
        response = requests.get(f"{self.base_url}/users/{user_id}")
        return response

    def create_user(self, name, job):
        response = requests.post(f"{self.base_url}/users", json={"name": name, "job": job})
        return response

    def update_user(self, user_id, name, job):
        response = requests.put(f"{self.base_url}/users/{user_id}", json={"name": name, "job": job})
        return response

    def delete_user(self, user_id):
        response = requests.delete(f"{self.base_url}/users/{user_id}")
        return response
