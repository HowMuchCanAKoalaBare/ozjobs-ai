import pandas as pd
import json
import numpy as np
import logging
import sys
from typing import Dict, Any
from config import (
    DATA_DIR, MERGED_OCCUPATIONS_CSV, STATES_TABLE_CSV,
    SCORES_JSON, DATA_JSON, MAJOR_GROUP_MAP, STATE_MAP,
    DEFAULT_SCORE, LOG_LEVEL, LOG_FORMAT
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

logger.info("Building clean OzJobs AI data.json with hierarchy...")

try:
    df = pd.read_csv(MERGED_OCCUPATIONS_CSV)
    logger.info(f"Loaded {len(df)} occupations from {MERGED_OCCUPATIONS_CSV.name}")
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error loading CSV: {e}")
    sys.exit(1)
try:
    with open(SCORES_JSON, "r") as f:
        scores = json.load(f)
    logger.info(f"Loaded scores for {len(scores)} occupations")
except FileNotFoundError as e:
    logger.error(f"Scores file not found: {e}")
    logger.warning("Proceeding without LLM scores - using default score of 5")
    scores = {}
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON in scores file: {e}")
    scores = {}
key_col = df.columns[0]

df["ai_score"] = df[key_col].map(lambda c: scores.get(str(c), {}).get("score", DEFAULT_SCORE))
df["rationale"] = df[key_col].map(lambda c: scores.get(str(c), {}).get("rationale", ""))

# Hierarchical grouping (Major Groups like original JoshKale)
df["Major Group"] = df["ANZSCO Code"].astype(str).str[0].map(MAJOR_GROUP_MAP)

# Clean NaNs
for col in df.columns:
    if df[col].dtype == float:
        df[col] = df[col].fillna(0)

# State averages
try:
    state_df = pd.read_csv(STATES_TABLE_CSV)
except FileNotFoundError as e:
    logger.error(f"States file not found: {e}")
    sys.exit(1)
state_map = STATE_MAP
state_averages = {}
for short, full in state_map.items():
    if short in state_df.columns:
        state_df[short] = pd.to_numeric(state_df[short], errors='coerce')
        weighted = (state_df[short] * df["ai_score"]).sum() / state_df[short].sum()
        state_averages[full] = round(weighted, 1)

data = {"occupations": df.to_dict("records"), "state_averages": state_averages}

try:
    with open(DATA_JSON, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Successfully wrote {DATA_JSON.name} with {len(data['occupations'])} occupations")
except Exception as e:
    logger.error(f"Error writing {DATA_JSON.name}: {e}")
    sys.exit(1)

logger.info("✅ Data build complete!")