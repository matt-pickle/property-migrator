import csv
import os
from typing import TypedDict, Literal, Any

CsvProp = TypedDict('CsvProp', {
    "Name": str,
    "Internal name": str,
    "Type": Literal["string", "number", "date", "datetime", "enumeration", "boolean"],
    "Description": str,
    "Group name": str,
    "Form field": Literal["TRUE", "FALSE"],
    "Options": str,
    "Read only value": Literal["TRUE", "FALSE"],
    "Read only definition": Literal["TRUE", "FALSE"],
    "Calculated": Literal["TRUE", "FALSE"],
    "External options": Literal["TRUE", "FALSE"],
    "Deleted": Literal["TRUE", "FALSE"],
    "Hubspot defined": Literal["TRUE", "FALSE"],
    "Created user": str,
    "Usages": str,
    "Unique": Literal["TRUE", "FALSE"],
    "Field type": Literal["textarea", "text", "date", "file", "number", "select", "radio", "checkbox", "booleancheckbox", "calculation_equation"],
})

def parse_csv(csv_file_path: str) -> list[CsvProp]:
    # Get absolute path if relative path is provided
    if not os.path.isabs(csv_file_path):
        csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), csv_file_path)
    
    # Check if file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: File not found at {csv_file_path}")
        return []
    
    # Parse CSV to list of dictionaries
    data: Any = []
    try:
        with open(csv_file_path, 'r', encoding='ISO-8859-1') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                data.append(row)
        
        print(f"Successfully parsed {len(data)} rows from {csv_file_path}")
        return data
    except Exception as e:
        print(f"Error parsing CSV file: {str(e)}")
        return []