import pandas as pd, json, os
from openrouter import OpenRouter

df = pd.read_csv("data/merged_occupations.csv")
scores = {}
client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY"))

for _, row in df.iterrows():
    prompt = f"""Australian occupation: {row.get('Occupation','Unknown')}
Tasks: {row.get('Task','N/A')}
Growth: {row.get('Growth %','N/A')}%
Pay: ${row.get('Median weekly earnings',0):,} AUD
Score AI exposure 0-10 (Aussie context: skills shortages, clean energy, high wages).
Return JSON only: {{"score": int, "rationale": "..."}}"""
    try:
        resp = client.chat.completions.create(model="google/gemini-flash-1.5", messages=[{"role":"user","content":prompt}])
        result = json.loads(resp.choices[0].message.content)
        scores[str(row[df.columns[0]])] = result   # flexible key
    except:
        scores[str(row[df.columns[0]])] = {"score": 5, "rationale": "Fallback"}

with open("data/scores.json", "w") as f:
    json.dump(scores, f)
print("✅ LLM scoring complete!")