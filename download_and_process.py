import pandas as pd
from pathlib import Path
import requests
from io import BytesIO

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

OCC_URL = "https://www.jobsandskills.gov.au/sites/default/files/2026-03/Occupation%20profiles%20data%20-%20November%202025%20%28Revised%29.xlsx"

print("Downloading latest JSA data...")

occ_file = BytesIO(requests.get(OCC_URL).content)

# Table_1 – main occupations (header=5)
occ = pd.read_excel(occ_file, sheet_name="Table_1", header=5)
occ = occ.dropna(subset=[occ.columns[0]])
occ.columns = ['ANZSCO Code', 'Occupation', 'Employed', 'Part-time share (%)', 'Female share (%)', 
               'Median weekly earnings ($)', 'Median age', 'Annual employment growth', 'Col9', 'Col10']
occ["ANZSCO Code"] = occ["ANZSCO Code"].astype(str)   # ← permanent string fix

# Table_3 – tasks (header=5)
tasks_df = pd.read_excel(occ_file, sheet_name="Table_3", header=5)
tasks = tasks_df.groupby(tasks_df.columns[0])[tasks_df.columns[2]].apply(" | ".join).reset_index(name="Task")
tasks.columns = ['ANZSCO Code', 'Task']
tasks["ANZSCO Code"] = tasks["ANZSCO Code"].astype(str)

# Table_6 – states (header=6)
states_df = pd.read_excel(occ_file, sheet_name="Table_6", header=6)
states_df.columns = ['ANZSCO Code', 'Occupation', 'NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT']
states_df["ANZSCO Code"] = states_df["ANZSCO Code"].astype(str)
states_df.to_csv(DATA_DIR / "states_table6.csv", index=False)

merged = occ.merge(tasks, on="ANZSCO Code", how="left")
merged.to_csv(DATA_DIR / "merged_occupations.csv", index=False)

print(f"✅ SUCCESS! Processed {len(merged)} occupations with string ANZSCO keys")
