import time
from functions.get_env import get_env
from functions.parse_csv import CsvProp, parse_csv
from functions.get_properties import Option, Property, get_properties
from functions.update_property import UpdatePropData, update_property
from functions.batch_create_properties import CreatePropInput, batch_create_properties

SOURCE_PRIVATE_APP_KEY: str = get_env("SOURCE_PRIVATE_APP_KEY")
TARGET_PRIVATE_APP_KEY: str = get_env("TARGET_PRIVATE_APP_KEY")

record_type = "contacts"

# Parse properties from the input CSV file
csv_props: list[CsvProp] = parse_csv("input/contacts.csv")

# Filter out default HubSpot properties
csv_props = [prop for prop in csv_props if prop["Hubspot defined"] == "FALSE"]

# Get source properties
source_props: list[Property] = get_properties(record_type, SOURCE_PRIVATE_APP_KEY)

# Get existing properties from target portal
existing_props: list[Property] = get_properties(record_type, TARGET_PRIVATE_APP_KEY)

# Sort into new and existing
existing_prop_names: list[str] = [prop["name"] for prop in existing_props]
props_to_create: list[Property] = [prop for prop in source_props if prop["name"] not in existing_prop_names]
props_to_update: list[Property] = [prop for prop in source_props if prop["name"] in existing_prop_names]

# Update existing properties
for prop in props_to_update:
    options: list[Option] = prop.get("options", [])
    data: UpdatePropData = {
        "label": prop["label"],
        "type": prop["type"],
        "description": prop["description"],
        "groupName": prop["groupName"],
        "formField": prop["formField"],
        "hasUniqueValue": prop["hasUniqueValue"],
        "fieldType": prop["fieldType"],
        "referencedObjectType": prop.get("referencedObjectType"),
        "externalOptions": prop["externalOptions"],
        "options": options
    }
    update_property(record_type, prop["name"], data, TARGET_PRIVATE_APP_KEY)
    time.sleep(0.25)

# Create new properties
create_inputs: list[CreatePropInput] = []
for prop in props_to_create:
    options: list[Option] = prop.get("options", [])

    input: CreatePropInput = {
        "name": prop["name"],
        "label": prop["label"],
        "type": prop["type"],
        "description": prop["description"],
        "groupName": prop["groupName"],
        "formField": prop["formField"],
        "hasUniqueValue": prop["hasUniqueValue"],
        "fieldType": prop["fieldType"],
        "referencedObjectType": prop.get("referencedObjectType"),
        "externalOptions": prop["externalOptions"],
        "options": prop.get("options", [])
    }
    
    create_inputs.append(input)
batch_create_properties(record_type, create_inputs, TARGET_PRIVATE_APP_KEY)