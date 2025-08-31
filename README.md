# Tiny2CSV

Tiny2CSV is a simple Python utility that converts [FabricMC Tiny mappings](https://github.com/FabricMC/intermediary) (`.tiny` files) into more accessible CSV and SRG-like formats.  
It extracts **classes, methods, and fields** from the mappings and outputs them as separate files for easier analysis and tooling.

---

- Downloads FabricMC `.tiny` mappings for any given Minecraft version
- Parses mappings into:
  - `methods.csv` → Method name, descriptor, deobfuscated name, parameter count
  - `fields.csv` → Field name, deobfuscated name
  - `joined.srg` → Class name mappings in SRG-like format
