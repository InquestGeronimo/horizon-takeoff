import requests
from typing import Any, Dict

class EC2Endpoint:
    """A class for invoking a API endpoint on EC2Instance with JSON data via a __call__ method."""

    BASE_URLS = {
        (False, False): "8000/generate",
        (False, True): "8000/generate_stream",
        (True, False): "3000/generate",
        (True, True): "3000/generate_stream",
    }

    def __init__(self, address: str, pro: bool = False, stream: bool = False):
        """
        Initialize an Endpoint instance.

        Args:
            address (str): The ipv4 address for the EC2 instance.
            stream (bool): Whether to use a streaming endpoint. Defaults to False.
            pro (bool): Whether to use a pro or community endpoint. Defaults to False.
        """
        base_url = "http://" + address + ":"
        self.url = base_url + self.BASE_URLS[(pro, stream)]

    def __call__(self, input_text: str) -> Dict[str, Any]:
        """
        Invoke the URL with JSON data.

        Args:
            input_text (str): The input text to include in the JSON data.

        Returns:
            Dict[str, Any]: The JSON response from the URL.
        """
        json_data = {"text": input_text}
        response = requests.post(self.url, json=json_data)
        return response.json()
