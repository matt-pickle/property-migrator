from typing import TypedDict, Literal, Required
import requests
import time

class CreatePropInputOption(TypedDict, total=False):
    hidden: Required[bool]
    description: str
    label: Required[str]
    value: Required[str]


class CreatePropInput(TypedDict, total=False):
    description: str
    label: Required[str]
    type: Required[Literal["string", "number", "date", "datetime", "enumeration", "boolean"]]
    formField: bool
    groupName: Required[str]
    referencedObjectType: Literal["OWNER"] | None
    name: Required[str]
    options: list[CreatePropInputOption] | None
    hasUniqueValue: bool
    fieldType: Required[Literal["textarea", "text", "date", "file", "number", "select", "radio", "checkbox", "booleancheckbox", "calculation_equation"]]
    externalOptions: bool


def batch_create_properties(
    record_type: str,
    inputs: list[CreatePropInput],
    PRIVATE_APP_KEY: str,
) -> None:
    url = f"https://api.hubapi.com/crm/v3/properties/{record_type}/batch/create"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json" }
    records: list[dict] = []

    for i in range(0, len(inputs), 25):
        batch = inputs[i:i+25]
        data = { "inputs": batch }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            json_response = response.json()
            print(f"Created properties: {len(json_response['results'])}")
            records.extend(json_response["results"])
        except requests.exceptions.RequestException as e:
            print(f"Error creating properties: {e}")

        time.sleep(0.25)
    
    print(f"Total properties created: {len(records)}")