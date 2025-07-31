from typing import TypedDict, NotRequired, Literal
import requests

class Option(TypedDict):
    label: str
    value: str
    hidden: bool
    description: str

class Property(TypedDict):
    name: str
    label: str
    type: Literal['string', 'number', 'date', 'datetime', 'enumeration', 'bool']
    formField: bool
    groupName: str
    description: str
    hasUniqueValue: bool
    fieldType: Literal['textarea', 'text', 'date', 'file', 'number', 'select', 'radio', 'checkbox', 'booleancheckbox', 'calculation_equation']
    externalOptions: bool
    hidden: bool
    hubspotDefined: NotRequired[bool]
    referencedObjectType: NotRequired[Literal['OWNER']]
    calculationFormula: NotRequired[str]
    options: NotRequired[list[Option]]

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
        properties = [result for result in results if not result.get('hubspotDefined')]
    except requests.exceptions.RequestException as e:
        print(f"Error getting properties: {e}")

    return properties