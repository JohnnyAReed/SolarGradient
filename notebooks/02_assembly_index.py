#!/usr/bin/env python3
"""
Compute Assembly Index for GNPS plant & ocean metabolites vs. solar phase.
"""
import pandas as pd, json, requests, os
from assembly_theory import assembly_index

# 1. Download GNPS plant/ocean datasets
urls = [
    "https://raw.githubusercontent.com/CCMS-UCSD/GNPSLibrary/master/GNPS-LIBRARY-PLANT.json",
    "https://raw.githubusercontent.com/CCMS-UCSD/GNPSLibrary/master/GNPS-LIBRARY-OCEAN.json"
]
dfs = []
for url in urls:
    fname = url.split("/")[-1]
    if not os.path.exists(f"../data/{fname}"):
        open(f"../data/{fname}", "wb").write(requests.get(url).content)
    dfs.append(pd.json_normalize(json.load(open(f"../data/{fname}"))))

df = pd.concat(dfs, ignore_index=True)

# 2. Compute AI for InChI strings
df["AI"] = df["Smiles"].apply(lambda smi: assembly_index(smi) if pd.notna(smi) else None)
df[["Compound_Name","AI"]].to_csv("../data/assembly_index.csv", index=False)
print("Assembly indices computed → ../data/assembly_index.csv")
