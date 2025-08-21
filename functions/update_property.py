from typing import TypedDict, Literal, Required
import requests
import time

class PropOption(TypedDict):
    label: str
    value: str
    hidden: bool
    description: str


class UpdatePropData(TypedDict, total=False):
    description: str
    label: Required[str]
    type: Required[Literal["string", "number", "date", "datetime", "enumeration", "bool"]]
    formField: bool
    groupName: Required[str]
    referencedObjectType: Literal["OWNER"] | None
    options: list[PropOption] | None
    hasUniqueValue: bool
    fieldType: Required[Literal["textarea", "text", "date", "file", "number", "select", "radio", "checkbox", "booleancheckbox", "calculation_equation"]]
    externalOptions: bool


def update_property(
    record_type: str,
    prop_name: str,
    data: UpdatePropData,
    PRIVATE_APP_KEY: str,
) -> None:
    url = f"https://api.hubapi.com/crm/v3/properties/{record_type}/{prop_name}"
    headers = { "Authorization": f"Bearer {PRIVATE_APP_KEY}", "Content-Type": "application/json" }

    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Updated {prop_name} property")
    except requests.exceptions.RequestException as e:
        print(f"Error updating {prop_name} property: {e.response.text}")