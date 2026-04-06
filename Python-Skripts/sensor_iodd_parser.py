from iodd_parser import IODDParser
import os
from dotenv import load_dotenv
from pprint import pprint
import json



load_dotenv(dotenv_path="../.env")

iodd_path = os.getenv("IODD_PATH")

sensor1 = "Balluff-BOSR254KUUIPR10-ADSS-20210628-IODD1.1.zip"
sensor2 = "Balluff-BOS21UUIRP30-20180207-IODD1.1.zip"

if not iodd_path:
    raise ValueError("Az IODD_PATH nincs beállítva a .env fájlban")

full_path = os.path.join(iodd_path, sensor2)

print("IODD_PATH:", iodd_path)
print("Full path:", full_path)

parser = IODDParser()

result = parser.parse_and_resolve(full_path)

print(result.device_name)
print(result.device_manufacturer)

vars_by_index = {v.index: v for v in result.variables.values()}


def get_variable_info(var):
    info = {
        "name": var.name,
        "id": var.id,
        "values": []
    }

    def extract_values(datatype):
        return [
            {"val": sv.value, "text": sv.name}
            for sv in getattr(datatype, "single_values", [])
        ]

    if hasattr(var.datatype, "items"):
        for item in var.datatype.items:
            info["values"].append({
                "subindex": item.subindex,
                "name": item.name,
                "mappings": extract_values(item.datatype)
            })
    else:
        info["values"].append({
            "subindex": 0,
            "name": var.name,
            "mappings": extract_values(var.datatype)
        })

    return info


# for key, value in vars_by_index.items():
#     print(f"The details of Index {key} for {value.name}:\n")
#     pprint(get_variable_info(value))
#     print("--------------------------------------------------------")

data = []

for key, value in vars_by_index.items():
    data.append(get_variable_info(value))

with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

pprint(result.variables)