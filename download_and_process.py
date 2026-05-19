import pandas as pd
from pathlib import Path
import requests
from io import BytesIO
import logging
import sys
from typing import Dict, Any
from config import (
    DATA_DIR, JSA_DATA_URL, MERGED_OCCUPATIONS_CSV,
    STATES_TABLE_CSV, LOG_LEVEL, LOG_FORMAT
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

logger.info("Downloading latest JSA data...")

try:
    response = requests.get(JSA_DATA_URL, timeout=30)
    response.raise_for_status()
    occ_file = BytesIO(response.content)
    logger.info(f"Successfully downloaded data ({len(response.content)} bytes)")
except requests.RequestException as e:
    logger.error(f"Failed to download data: {e}")
    sys.exit(1)

try:
    occ = pd.read_excel(occ_file, sheet_name="Table_1", header=5)
    occ = occ.dropna(subset=[occ.columns[0]])
    occ.columns = ['ANZSCO Code', 'Occupation', 'Employed', 'Part-time share (%)', 'Female share (%)', 
                   'Median weekly earnings ($)', 'Median age', 'Annual employment growth', 'Col9', 'Col10']
    occ["ANZSCO Code"] = occ["ANZSCO Code"].astype(str)
    logger.info(f"Loaded {len(occ)} occupations from Table_1")
except Exception as e:
    logger.error(f"Error reading Table_1: {e}")
    sys.exit(1)

try:
    tasks_df = pd.read_excel(occ_file, sheet_name="Table_3", header=5)
    tasks = tasks_df.groupby(tasks_df.columns[0])[tasks_df.columns[2]].apply(" | ".join).reset_index(name="Task")
    tasks.columns = ['ANZSCO Code', 'Task']
    tasks["ANZSCO Code"] = tasks["ANZSCO Code"].astype(str)
    logger.info(f"Loaded {len(tasks)} task entries from Table_3")
except Exception as e:
    logger.error(f"Error reading Table_3: {e}")
    sys.exit(1)

try:
    states_df = pd.read_excel(occ_file, sheet_name="Table_6", header=6)
    states_df.columns = ['ANZSCO Code', 'Occupation', 'NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT']
    states_df["ANZSCO Code"] = states_df["ANZSCO Code"].astype(str)
    states_df.to_csv(STATES_TABLE_CSV, index=False)
    logger.info(f"Saved {len(states_df)} state records to {STATES_TABLE_CSV.name}")
except Exception as e:
    logger.error(f"Error reading Table_6: {e}")
    sys.exit(1)

try:
    merged = occ.merge(tasks, on="ANZSCO Code", how="left")
    merged.to_csv(MERGED_OCCUPATIONS_CSV, index=False)
    logger.info(f"SUCCESS! Processed {len(merged)} occupations with string ANZSCO keys")
except Exception as e:
    logger.error(f"Error merging data: {e}")
    sys.exit(1)
