import pandas as pd
import json
import os
import logging
import sys
import time
from typing import Dict, Any
from openrouter import OpenRouter
from config import (
    MERGED_OCCUPATIONS_CSV, SCORES_JSON, OPENROUTER_API_KEY,
    LLM_MODEL, API_RATE_LIMIT_DELAY, DEFAULT_SCORE,
    LOG_LEVEL, LOG_FORMAT
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

if not OPENROUTER_API_KEY:
    logger.error("OPENROUTER_API_KEY environment variable not set")
    sys.exit(1)

try:
    df = pd.read_csv(MERGED_OCCUPATIONS_CSV)
    logger.info(f"Loaded {len(df)} occupations for scoring")
except FileNotFoundError as e:
    logger.error(f"{MERGED_OCCUPATIONS_CSV.name} not found: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error loading CSV: {e}")
    sys.exit(1)

scores: Dict[str, Dict[str, Any]] = {}
client = OpenRouter(api_key=OPENROUTER_API_KEY)

logger.info(f"Starting LLM scoring for {len(df)} occupations...")
for idx, row in df.iterrows():
    prompt = f"""Australian occupation: {row.get('Occupation','Unknown')}
Tasks: {row.get('Task','N/A')}
Growth: {row.get('Growth %','N/A')}%
Pay: ${row.get('Median weekly earnings',0):,} AUD
Score AI exposure 0-10 (Aussie context: skills shortages, clean energy, high wages).
Return JSON only: {{"score": int, "rationale": "..."}}"""
    try:
        resp = client.chat.completions.create(model=LLM_MODEL, messages=[{"role":"user","content":prompt}])
        result = json.loads(resp.choices[0].message.content)
        scores[str(row[df.columns[0]])] = result
        logger.info(f"Scored {idx+1}/{len(df)}: {row.get('Occupation', 'Unknown')} - Score: {result.get('score', 5)}")
        time.sleep(API_RATE_LIMIT_DELAY)  # Rate limiting
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON response for {row.get('Occupation', 'Unknown')}: {e}")
        scores[str(row[df.columns[0]])] = {"score": DEFAULT_SCORE, "rationale": "Parse error"}
    except Exception as e:
        logger.warning(f"Error scoring {row.get('Occupation', 'Unknown')}: {e}")
        scores[str(row[df.columns[0]])] = {"score": DEFAULT_SCORE, "rationale": "API error"}

try:
    with open(SCORES_JSON, "w") as f:
        json.dump(scores, f, indent=2)
    logger.info(f"✅ LLM scoring complete! Saved {len(scores)} scores")
except Exception as e:
    logger.error(f"Error writing {SCORES_JSON.name}: {e}")
    sys.exit(1)