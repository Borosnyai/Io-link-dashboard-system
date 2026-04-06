from iodd_parser import IODDParser
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import asdict

from iodd_parser.types import ResolvedDatatype, ResolvedRecordT, ResolvedVariable


parser = IODDParser()
load_dotenv()

iodd_path = os.getenv('IODD_PATH')

sensor1 = "Balluff-BOSR254KUUIPR10-ADSS-20210628-IODD1.1.zip"
sensor2 = "Balluff-BOS21UUIRP30-20180207-IODD1.1.zip"
sensor3 = ""

# Parse and resolve in one step
result = parser.parse_and_resolve(iodd_path + sensor2)

print(result.device_name)
print(result.device_manufacturer)
print('#' * 50)
pprint(result)


# Access user interface menus
ui = result.user_interface

Interface_printable = asdict(ui)
# pprint(Interface_printable)

# Get the specialist role menu set
specialist = ui.specialist_role_menu_set
print(f"Identification menu: {specialist.identification_menu_id}")

# Access menu details
# menu = ui.menus[specialist.identification_menu_id]
# for var_ref in menu.variable_refs:
#     print(f"  Variable: {var_ref.variable_id}")


# Access resolved variables by ID
for var_id, var in result.variables.items():
    if hasattr(var.datatype, "single_values"):
    # if var.index == 157:
        print(f'Resolved variable has ID "{var_id}" and the name: {var.name} (index={var.index}) and the class: {var.datatype.__class__}')
        for line in var.datatype.single_values:
            print(f'Option nr. {line.value} is {line.name}.')
        print('\n')

# Read Resolved IODD:
for string, variable in result.variables.items():
    print(f'The variable is --{string}-- and its index is {variable.index}:')
    if variable.datatype.__class__ == ResolvedRecordT:
        for item in variable.datatype.items:
            print(f'    The name is {item.name} and the subindex is {item.subindex}')
            if hasattr(item, "single_values"):
                pprint(item.single_values)
    

# Access resolved process data
for pd_id, pd in result.process_data.items():
    if pd.process_data_in:
        print(f'Input: {pd.process_data_in.name} represented in "{pd.process_data_in.bit_length}" bits')

# All process data:
for pd_id, pd in result.process_data.items():
    print(f'The id is: {pd_id}, whereas condition value is {pd.condition_value}')

# Access resolved errors
# for (code, additional_code), error in result.errors.items():
#     print(f"Error {code}/{additional_code}: {error.name}")

# Access resolved units
# for unit_code, unit in result.units.items():
#     print(f"Unit {unit_code}: {unit.name} ({unit.abbreviation})")

# Access texts:
# for key, value in result.texts.items():
#     print(f'The Text-key is "{key}" and the value is "{value}".')