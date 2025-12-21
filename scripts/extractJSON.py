# this python script create a JSON file from exploring a directory structure
"""
{
            "id": "com_mod",
            "name": "COM_MOD",
            "description": "Communication module to connect HMI modules together and to the controller.",
            "topCategory": "hmi_module",
            "kind": "communication",
            "categoryPath": [
                "HMI Modules",
                "Communication",
                "COM_MOD"
            ],
            "priceEur": 20,
            "stock": 5,
            "image": "/images/COM_MOD_LDtop.png",
        },
"""

fields = ["id", "name", "description", "topCategory", "kind", "categoryPath", "priceEur", "stock", "image"]

import os
import json
import re
import sys


dirpath = "../KiCad/"
outputfile = "modules.json"
print("Exploring directory: " + dirpath)
# find all name.kicad_pro
modules = {"modules": []}
# don't explore hidden directories
prj_files = []
for root, dirs, files in os.walk(dirpath):
    root_rel = os.path.relpath(root, dirpath)
    if any(part.startswith('.') for part in root_rel.split(os.sep)):
        continue
    for file in files:
        if file.endswith(".kicad_pro"):
            prj_files.append(os.path.join(root, file))
            print(f"Found project file: {os.path.join(root, file)}")




for file in prj_files:
    module = {}
    module["name"] = os.path.splitext(os.path.basename(file))[0]
    module["id"] = module["name"].lower()
    # extract description from the README.md file in the same directory (just the first line after the title)
    readme_path = os.path.join(file, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as f:
            print(f"Extracting description from {readme_path}")
            lines = f.readlines()
            description = ""
            for line in lines:
                if re.match(r'^#', line):
                    description += line.strip() + "\n"
                elif line.strip() != "":
                    description += line.strip()
                    break
            module["description"] = description
    else:
        module["description"] = "No description available."
    
    # topCategory is the first directory after dirpath
    relpath = os.path.relpath(file, dirpath)
    # print(f"Relative path: {relpath}")
    path_parts = relpath.split(os.sep)
    if len(path_parts) > 0:
        module["topCategory"] = path_parts[0]
    else:
        module["topCategory"] = "Uncategorized"
    # kind is the second directory after dirpath
    if len(path_parts) > 1:
        module["kind"] = path_parts[1]
    else:
        module["kind"] = "general"
    # categoryPath is the full path from dirpath to the module
    module["categoryPath"] = path_parts[:-1] 
    # priceEur is a random value between 10 and 100
    module["priceEur"] = 10 + (hash(module["id"]) % 91)
    # stock is a random value between 0 and 50
    module["stock"] = hash(module["id"]) % 51
    # image is a placeholder path
    module["image"] = "/images/" + module["name"] + "_LDtop.png"
    modules["modules"].append(module)
    # print(module)
    # exec kicad-cli jobset run --file jobs.kicad_jobset --output LDRendering "$li"
    # os.system(f'kicad-cli jobset run --file jobs.kicad_jobset --output LDRendering "{file}"')

# os.system('mv plots images')
    
print(f"Found {len(modules)} modules.")

# write to JSON file
with open(outputfile, 'w') as f:
    json.dump(modules, f, indent=4)