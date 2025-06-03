from functions.get_private_app_key import get_private_app_key
from functions.parse_csv import CsvProp, parse_csv
from functions.get_properties import Property, get_properties
from functions.batch_create_properties import CreatePropInput, CreatePropInputOption, batch_create_properties
import json

PRIVATE_APP_KEY: str = get_private_app_key()

record_type = "contacts"

# Parse properties from the input CSV file
props: list[CsvProp] = parse_csv("input/contacts.csv")

# Filter out default HubSpot properties
props = [prop for prop in props if prop["Hubspot defined"] == "FALSE"]

# Get existing properties
existing_props: list[Property] = get_properties(record_type, PRIVATE_APP_KEY)

# Sort into new and existing
existing_prop_names: list[str] = [prop["name"] for prop in existing_props]
props_to_create: list[CsvProp] = [prop for prop in props if prop["Internal name"] not in existing_prop_names]
props_to_update: list[CsvProp] = [prop for prop in props if prop["Internal name"] in existing_prop_names]

# Update existing properties

# Create new properties
create_inputs: list[CreatePropInput] = []
for prop in props_to_create:
    source_options: dict = json.loads(prop["Options"])
    options: list[CreatePropInputOption] = []
    for source_option in source_options:
        options.append({
            "label": source_option["label"],
            "value": source_option["value"],
            "hidden": source_option.get("hidden", False),
            "description": source_option.get("description", "")
        })
    field_type = "text"
    if prop.get("Field type"):
        field_type = prop["Field type"]
    elif prop["Type"] == "number":
        field_type = "number"
    elif prop["Type"] == "datetime":
        field_type = "date"
    elif prop["Type"] == "enumeration":
        field_type = "select"
    elif prop["Type"] == "boolean":
        field_type = "booleancheckbox"

    input: CreatePropInput = {
        "name": prop["Internal name"],
        "label": prop["Name"],
        "type": prop["Type"],
        "description": prop["Description"],
        "groupName": prop["Group name"],
        "formField": prop["Form field"] == "TRUE",
        "hasUniqueValue": prop["Unique"] == "TRUE",
        "fieldType": field_type,
        "referencedObjectType": "OWNER" if prop["External options"] == "TRUE" else None,
        "externalOptions": prop["External options"] == "TRUE",
        "options": options,
    }
    
    create_inputs.append(input)
batch_create_properties(record_type, create_inputs, PRIVATE_APP_KEY)