from fastapi import FastAPI, HTTPException
from iodd_parser import IODDParser
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

app = FastAPI()

# env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

IODD_PATH = os.getenv("IODD_PATH")

if not IODD_PATH:
    raise ValueError("IODD_PATH is not set in .env")

IODD_FILE = "Balluff-BOS21UUIRP30-20180207-IODD1.1.zip"
iodd_file_path = os.path.join(IODD_PATH, IODD_FILE)

if not os.path.exists(iodd_file_path):
    raise FileNotFoundError(f"IODD file not found: {iodd_file_path}")

# --- parser init ---
parser = IODDParser()
result = parser.parse_and_resolve(iodd_file_path)

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/light-barrier/data"

mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION1,
    client_id="python-iodd-publisher"
)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)


def clean_value(value):
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)

def find_process_data_item(subindex: int):
    raw_process_data = getattr(result, "process_data", {})

    for process_id, pd in raw_process_data.items():
        process_data_in = getattr(pd, "process_data_in", None)

        if process_data_in is None:
            continue

        datatype = getattr(process_data_in, "datatype", None)
        items = getattr(datatype, "items", [])

        for item in items:
            if getattr(item, "subindex", None) == subindex:
                return {
                    "process_id": process_id,
                    "process_name": clean_value(getattr(process_data_in, "name", None)),
                    "subindex": clean_value(getattr(item, "subindex", None)),
                    "name": clean_value(getattr(item, "name", None)),
                    "description": clean_value(getattr(item, "description", None)),
                    "datatype": clean_value(getattr(item, "datatype", None)),
                    "bit_offset": clean_value(getattr(item, "bit_offset", None)),
                }

    return None


@app.get("/")
def root():
    return {"message": "IODD API running"}


@app.get("/iodd")
def get_iodd_info():
    return {
        "device_name": clean_value(getattr(result, "device_name", None)),
        "manufacturer": clean_value(getattr(result, "device_manufacturer", None)),
    }


@app.get("/debug-result")
def debug_result():
    return {
        "result_type": str(type(result)),
        "result_dir": [x for x in dir(result) if not x.startswith("_")]
    }


@app.get("/debug-variables")
def debug_variables():
    raw_variables = getattr(result, "variables", None)

    return {
        "variables_type": str(type(raw_variables)),
        "is_none": raw_variables is None,
        "string_preview": str(raw_variables)[:1000],
        "dir": [x for x in dir(raw_variables) if not x.startswith("_")]
    }


@app.get("/debug-variables-items")
def debug_variables_items():
    raw_variables = getattr(result, "variables", None)

    items = []

    try:
        if isinstance(raw_variables, dict):
            for key, value in list(raw_variables.items())[:10]:
                items.append({
                    "key": str(key),
                    "value": str(value),
                    "value_type": str(type(value))
                })
        else:
            for i, item in enumerate(list(raw_variables)[:10]):
                items.append({
                    "position": i,
                    "value": str(item),
                    "type": str(type(item))
                })
    except Exception as e:
        return {
            "error": str(e),
            "variables_type": str(type(raw_variables))
        }

    return {
        "variables_type": str(type(raw_variables)),
        "items": items
    }


@app.get("/debug-all-top-level")
def debug_all_top_level():
    return {
        "device_name": clean_value(getattr(result, "device_name", None)),
        "device_manufacturer": clean_value(getattr(result, "device_manufacturer", None)),
        "variables_type": str(type(getattr(result, "variables", None))),
        "process_data_type": str(type(getattr(result, "process_data", None))),
        "user_interface_type": str(type(getattr(result, "user_interface", None))),
        "variables_preview": str(getattr(result, "variables", None))[:500],
        "process_data_preview": str(getattr(result, "process_data", None))[:500],
        "user_interface_preview": str(getattr(result, "user_interface", None))[:500],
    }


@app.get("/variables")
def get_variables():
    raw_variables = getattr(result, "variables", {})

    variables = []

    for variable_id, var in raw_variables.items():
        variables.append({
            "id": variable_id,
            "name": clean_value(getattr(var, "name", None)),
            "index": clean_value(getattr(var, "index", None)),
            "description": clean_value(getattr(var, "description", None)),
            "datatype": clean_value(getattr(var, "datatype", None)),
            "access_rights": clean_value(getattr(var, "access_rights", None)),
        })

    return {
        "count": len(variables),
        "variables": variables
    }


@app.get("/variables/index/{index}")
def get_variable_by_index(index: int):
    raw_variables = getattr(result, "variables", {})

    for variable_id, var in raw_variables.items():
        if getattr(var, "index", None) == index:
            return {
                "id": variable_id,
                "name": clean_value(getattr(var, "name", None)),
                "index": clean_value(getattr(var, "index", None)),
                "description": clean_value(getattr(var, "description", None)),
                "datatype": clean_value(getattr(var, "datatype", None)),
                "access_rights": clean_value(getattr(var, "access_rights", None)),
            }

    raise HTTPException(status_code=404, detail=f"Variable not found for index={index}")


@app.get("/variables/index/{index}/items")
def get_variable_items_by_index(index: int):
    raw_variables = getattr(result, "variables", {})

    for variable_id, var in raw_variables.items():
        if getattr(var, "index", None) == index:
            datatype = getattr(var, "datatype", None)
            items = getattr(datatype, "items", None)

            if not items:
                return {
                    "id": variable_id,
                    "name": clean_value(getattr(var, "name", None)),
                    "index": clean_value(getattr(var, "index", None)),
                    "items": []
                }

            result_items = []
            for item in items:
                result_items.append({
                    "subindex": clean_value(getattr(item, "subindex", None)),
                    "name": clean_value(getattr(item, "name", None)),
                    "description": clean_value(getattr(item, "description", None)),
                    "datatype": clean_value(getattr(item, "datatype", None)),
                })

            return {
                "id": variable_id,
                "name": clean_value(getattr(var, "name", None)),
                "index": clean_value(getattr(var, "index", None)),
                "items": result_items
            }

    raise HTTPException(status_code=404, detail=f"Variable not found for index={index}")


@app.get("/variables/{index}/{subindex}")
def get_variable_by_index_and_subindex(index: int, subindex: int):
    raw_variables = getattr(result, "variables", {})

    for variable_id, var in raw_variables.items():
        if getattr(var, "index", None) == index:
            datatype = getattr(var, "datatype", None)
            items = getattr(datatype, "items", None)

            if not items:
                raise HTTPException(
                    status_code=404,
                    detail=f"No subitems found for index={index}"
                )

            for item in items:
                if getattr(item, "subindex", None) == subindex:
                    return {
                        "variable_id": variable_id,
                        "variable_name": clean_value(getattr(var, "name", None)),
                        "index": clean_value(getattr(var, "index", None)),
                        "subindex": clean_value(getattr(item, "subindex", None)),
                        "name": clean_value(getattr(item, "name", None)),
                        "description": clean_value(getattr(item, "description", None)),
                        "datatype": clean_value(getattr(item, "datatype", None)),
                    }

            raise HTTPException(
                status_code=404,
                detail=f"Subindex {subindex} not found for index={index}"
            )

    raise HTTPException(
        status_code=404,
        detail=f"Variable not found for index={index}"
    )


@app.get("/process-data")
def get_process_data():
    raw_process_data = getattr(result, "process_data", {})

    process_entries = []

    for process_id, pd in raw_process_data.items():
        process_data_in = getattr(pd, "process_data_in", None)

        if process_data_in is None:
            continue

        datatype = getattr(process_data_in, "datatype", None)
        items = getattr(datatype, "items", [])

        parsed_items = []
        for item in items:
            parsed_items.append({
                "subindex": clean_value(getattr(item, "subindex", None)),
                "name": clean_value(getattr(item, "name", None)),
                "description": clean_value(getattr(item, "description", None)),
                "datatype": clean_value(getattr(item, "datatype", None)),
                "bit_offset": clean_value(getattr(item, "bit_offset", None)),
            })

        process_entries.append({
            "id": process_id,
            "name": clean_value(getattr(process_data_in, "name", None)),
            "bit_length": clean_value(getattr(process_data_in, "bit_length", None)),
            "items": parsed_items
        })

    return {
        "count": len(process_entries),
        "process_data": process_entries
    }

@app.post("/publish/process-data/{subindex}")
def publish_process_data(subindex: int):
    item = find_process_data_item(subindex)

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Process data item not found for subindex={subindex}"
        )

    # most még tesztérték
    if item["name"] in ["BDC1", "Stability", "Teach-In", "ok", "too low", "too high"]:
        current_value = True
    else:
        current_value = 123

    payload = {
        "sensorId": "light-barrier-1",
        "category": "process-data",
        "subindex": item["subindex"],
        "name": item["name"],
        "description": item["description"],
        "datatype": item["datatype"],
        "bit_offset": item["bit_offset"],
        "value": current_value,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))

    return {
        "message": "MQTT message published",
        "topic": MQTT_TOPIC,
        "payload": payload
    }

