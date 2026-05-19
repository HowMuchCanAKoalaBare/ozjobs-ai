# OzJobsAI

AI Exposure Analysis for Australian Jobs using official JSA (Jobs and Skills Australia) data.

## Overview

OzJobsAI analyzes AI exposure risk across Australian occupations using official government data from Jobs and Skills Australia. The system uses LLM-powered scoring to assess how susceptible different jobs are to AI automation, with a focus on Australian context including skills shortages, clean energy transition, and wage considerations.

## Features

- **Official Data Source**: Uses JSA Occupation Profiles data
- **LLM-Powered Scoring**: AI exposure scores (0-10) with detailed rationales
- **Interactive Visualization**: Treemap visualization with state filtering
- **Australian Context**: Scoring considers local factors like skills shortages
- **Hierarchical Grouping**: Occupations organized by ANZSCO Major Groups

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## Usage

### 1. Download and Process Data

Fetch the latest JSA data and process it:

```bash
python download_and_process.py
```

This downloads the official JSA Excel file and extracts:
- Occupation profiles (Table_1)
- Task descriptions (Table_3)
- State distribution data (Table_6)

### 2. Score Occupations with LLM

Generate AI exposure scores using the LLM:

```bash
python score_llm.py
```

This processes each occupation through the LLM to generate:
- AI exposure score (0-10)
- Detailed rationale for the score

**Note**: This step requires an OpenRouter API key and may take time due to rate limiting.

### 3. Build Site Data

Combine all data into the final data.json:

```bash
python build_site_data.py
```

This merges:
- Occupation data
- LLM scores
- State averages
- Major group classifications

### 4. View the Visualization

Open `index.html` in a web browser to view the interactive treemap visualization.

## Project Structure

```
ozjobs-ai-main/
├── config.py                 # Configuration settings
├── download_and_process.py   # Download and process JSA data
├── score_llm.py             # Generate AI exposure scores
├── build_site_data.py       # Build final data.json
├── requirements.txt         # Python dependencies
├── index.html               # Frontend visualization
├── script.js                # Frontend logic
├── style.css                # Frontend styling
├── data/                    # Data directory
│   ├── merged_occupations.csv
│   ├── states_table6.csv
│   └── scores.json
└── data.json                # Final output for frontend
```

## Configuration

Edit `config.py` to customize:
- API model selection
- Rate limiting settings
- File paths
- Score thresholds
- Logging configuration

## AI Score Interpretation

- **0-3.5 (Green)**: Safe as a koala - Low AI exposure
- **3.5-6.0 (Amber)**: She'll be right - Moderate AI exposure
- **6.0-10.0 (Red)**: Shark-bait exposed - High AI exposure

## Data Sources

- **Jobs and Skills Australia**: Official occupation profiles data
- **ANZSCO Classification**: Australian and New Zealand Standard Classification of Occupations

## Improvements Made

Recent improvements to the codebase include:

1. **Critical Bug Fix**: Removed random scoring override that was replacing LLM-generated scores
2. **Error Handling**: Added comprehensive error handling and logging to all Python scripts
3. **Type Hints**: Added type annotations for better code clarity
4. **Configuration Management**: Centralized configuration in config.py
5. **Frontend Error Handling**: Added error handling for data loading and visualization
6. **Dependency Management**: Created requirements.txt for reproducible installations
7. **Rate Limiting**: Added API rate limiting to prevent rate limit errors
8. **Security**: Added API key validation and timeout settings

## License

This project uses official Australian government data. Please refer to the JSA data license for usage terms.
