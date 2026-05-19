"""
Configuration settings for OzJobsAI
"""
import os
from pathlib import Path
from typing import Dict, Any

# Directory paths
BASE_DIR: Path = Path(__file__).parent
DATA_DIR: Path = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# API Configuration
OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL: str = "google/gemini-flash-1.5"
API_RATE_LIMIT_DELAY: float = 0.5  # seconds between API calls

# Data URLs
JSA_DATA_URL: str = "https://www.jobsandskills.gov.au/sites/default/files/2026-03/Occupation%20profiles%20data%20-%20November%202025%20%28Revised%29.xlsx"

# File paths
MERGED_OCCUPATIONS_CSV: Path = DATA_DIR / "merged_occupations.csv"
STATES_TABLE_CSV: Path = DATA_DIR / "states_table6.csv"
SCORES_JSON: Path = DATA_DIR / "scores.json"
DATA_JSON: Path = BASE_DIR / "data.json"

# ANZSCO Major Group Mapping
MAJOR_GROUP_MAP: Dict[str, str] = {
    '1': 'Managers',
    '2': 'Professionals',
    '3': 'Technicians and Trades Workers',
    '4': 'Community and Personal Service Workers',
    '5': 'Clerical and Administrative Workers',
    '6': 'Sales Workers',
    '7': 'Machinery Operators and Drivers',
    '8': 'Labourers'
}

# State Mapping
STATE_MAP: Dict[str, str] = {
    'NSW': 'New South Wales',
    'VIC': 'Victoria',
    'QLD': 'Queensland',
    'SA': 'South Australia',
    'WA': 'Western Australia',
    'TAS': 'Tasmania',
    'NT': 'Northern Territory',
    'ACT': 'Australian Capital Territory'
}

# AI Score thresholds
SAFE_THRESHOLD: float = 3.5
RISK_THRESHOLD: float = 6.0
DEFAULT_SCORE: int = 5

# Logging configuration
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
