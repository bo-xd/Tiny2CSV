import os
import sys
import requests

def parse_method_descriptor(desc: str) -> int:
    inner = desc[1:desc.index(")")]
    count, i = 0, 0
    while i < len(inner):
        c = inner[i]
        if c in "ZBCSIJFD":  # primitives
            count += 1; i += 1
        elif c == 'L':       # object type
            count += 1
            i = inner.index(';', i) + 1
        elif c == '[':       # array
            i += 1
        else:
            i += 1
    return count

base_dir = os.path.dirname(os.path.abspath(__file__))

version = sys.argv[1] if len(sys.argv) > 1 else input("Enter version (example: 1.21.7): ").strip()
tiny_filename = f"{version}.tiny"
tiny_path = os.path.join(base_dir, tiny_filename)

if not os.path.exists(tiny_path):
    print(f"Downloading {version}.tiny mappings...")
    url = f"https://raw.githubusercontent.com/FabricMC/intermediary/master/mappings/{version}.tiny"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to download mappings for {version}: {resp.status_code}")
    with open(tiny_path, "w", encoding="utf8") as f:
        f.write(resp.text)
    print(f"Downloaded {tiny_filename} to {base_dir}")

methods_out, fields_out, joined_out = [], [], []

with open(tiny_path, encoding="utf8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split('\t') if '\t' in line else line.split()
        if len(parts) < 2:
            continue
            
        kind = parts[0]
        if kind == "CLASS":
            if len(parts) >= 3:
                obf, named = parts[1], parts[2]
                joined_out.append(f"CL: {obf} {named}")
                
        elif kind == "METHOD":
            if len(parts) >= 4:
                class_obf, desc, method_obf = parts[1], parts[2], parts[3]
                method_named = parts[4] if len(parts) > 4 else ""
                paramcount = parse_method_descriptor(desc)
                methods_out.append(f"{method_obf},{desc},{method_named},{paramcount}")
                
        elif kind == "FIELD":
            if len(parts) >= 4:
                class_obf, field_obf = parts[1], parts[2]
                field_named = parts[3] if len(parts) > 3 else ""
                fields_out.append(f"{field_obf},{field_named},2,")

out_methods = os.path.join(base_dir, "methods.csv")
out_fields = os.path.join(base_dir, "fields.csv") 
out_joined = os.path.join(base_dir, "joined.srg")

with open(out_methods, "w", encoding="utf8") as f:
    f.write("\n".join(methods_out))
    
with open(out_fields, "w", encoding="utf8") as f:
    f.write("\n".join(fields_out))
    
with open(out_joined, "w", encoding="utf8") as f:
    f.write("\n".join(joined_out))

print(f"{out_methods} ({len(methods_out)} methods)")
print(f"{out_fields} ({len(fields_out)} fields)")
print(f"{out_joined} ({len(joined_out)} classes)")
