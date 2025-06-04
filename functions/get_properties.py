from typing import TypedDict
import requests

class Property(TypedDict):
    name: str
    hubspotDefined: bool

class Response(TypedDict):
    results: list[Property]

def get_properties(
    recordType: str,
    PRIVATE_APP_KEY: str,
) -> list[Property]:
    properties = []
    url = f"https://api.hubapi.com/crm/v3/properties/{recordType}"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json"}
        
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_response: Response = response.json()
        results = json_response["results"]
        print(f"Retrieved properties: {len(results)}")
        properties = [result for result in results if result["hubspotDefined"] == False]
    except requests.exceptions.RequestException as e:
        print(f"Error getting properties: {e}")

    return properties