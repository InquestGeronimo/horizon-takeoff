import requests
from typing import Dict, Any


class Endpoint:
    """A class for invoking a URL with JSON data via a __call__ method."""

    json_data: Dict[str, Any] = {}

    def __init__(self, url: str):
        """
        Initialize an Endpoint instance.

        Args:
            url (str): The URL to send POST requests to.
        """
        self.url = url

    def __call__(self, input_text: str) -> Dict[str, Any]:
        """
        Invoke the URL with JSON data.

        Args:
            input_text (str): The input text to include in the JSON data.

        Returns:
            Dict[str, Any]: The JSON response from the URL.
        """
        self.json_data = {"text": input_text}
        response = requests.post(self.url, json=self.json_data)
        return response.json()
