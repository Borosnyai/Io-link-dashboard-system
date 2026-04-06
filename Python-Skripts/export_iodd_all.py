import os
import json
from dotenv import load_dotenv
from iodd_parser import IODDParser

load_dotenv(dotenv_path="../.env")

iodd_path = os.getenv("IODD_PATH")
sensor_file = "Balluff-BOS21UUIRP30-20180207-IODD1.1.zip"

if not iodd_path:
    raise ValueError("IODD_PATH is not set in the .env file")

full_path = os.path.join(iodd_path, sensor_file)

parser = IODDParser()
result = parser.parse_and_resolve(full_path)


def extract_single_values(datatype):
    return [
        {
            "value": getattr(sv, "value", None),
            "name": getattr(sv, "name", None)
        }
        for sv in getattr(datatype, "single_values", [])
    ]


def extract_record_items(datatype):
    items = []

    if hasattr(datatype, "items"):
        for item in datatype.items:
            item_datatype = getattr(item, "datatype", None)

            items.append({
                "subindex": getattr(item, "subindex", None),
                "name": getattr(item, "name", None),
                "bit_offset": getattr(item, "bit_offset", None),
                "datatype": {
                    "type": type(item_datatype).__name__ if item_datatype else None,
                    "single_values": extract_single_values(item_datatype)
                }
            })

    return items


def extract_datatype(datatype):
    if datatype is None:
        return None

    return {
        "type": type(datatype).__name__,
        "single_values": extract_single_values(datatype),
        "items": extract_record_items(datatype)
    }


def extract_variable(var):
    return {
        "id": getattr(var, "id", None),
        "name": getattr(var, "name", None),
        "index": getattr(var, "index", None),
        "subindex": getattr(var, "subindex", None),
        "datatype": extract_datatype(getattr(var, "datatype", None))
    }


def extract_process_data(process_data):
    if not process_data:
        return None

    extracted = {}

    for pd_id, pd in process_data.items():
        process_data_in = getattr(pd, "process_data_in", None)
        process_data_out = getattr(pd, "process_data_out", None)

        extracted[pd_id] = {
            "condition_variable_id": getattr(pd, "condition_variable_id", None),
            "condition_subindex": getattr(pd, "condition_subindex", None),
            "condition_value": getattr(pd, "condition_value", None),
            "process_data_in": {
                "id": getattr(process_data_in, "id", None),
                "name": getattr(process_data_in, "name", None),
                "bit_length": getattr(process_data_in, "bit_length", None),
                "datatype": extract_datatype(getattr(process_data_in, "datatype", None))
            } if process_data_in else None,
            "process_data_out": {
                "id": getattr(process_data_out, "id", None),
                "name": getattr(process_data_out, "name", None),
                "bit_length": getattr(process_data_out, "bit_length", None),
                "datatype": extract_datatype(getattr(process_data_out, "datatype", None))
            } if process_data_out else None
        }

    return extracted


variables = [extract_variable(v) for v in result.variables.values()]
variables_by_id = {v["id"]: v for v in variables}

export_data = {
    "device": {
        "name": getattr(result, "device_name", None),
        "manufacturer": getattr(result, "device_manufacturer", None)
    },
    "vendor_text": variables_by_id.get("V_VendorText"),
    "process_data": extract_process_data(getattr(result, "process_data", None)),
    "process_data_in": variables_by_id.get("V_ProcessDataInput"),
    "process_data_out": variables_by_id.get("V_ProcessDataOutput"),
    "variables": variables
}

with open("iodd_complete.json", "w", encoding="utf-8") as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

print("Done: iodd_complete.json")