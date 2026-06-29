from pathlib import Path
import pandas as pd
from scipy.stats import kruskal
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'dataset.xlsx'
OUT_PATH = Path(__file__).resolve().parents[1] / 'outputs' / 'kruskal_wallis_results.csv'
OUT_PATH.parent.mkdir(exist_ok=True)

df = pd.read_excel(DATA_PATH)

# Recompute a transparent z-sum SCI if the provided SCI_score is absent or mostly empty.
positive = ['originality_mean', 'quality_mean', 'cultural_authenticity_mean', 'visual_diversity_score', 'felt_output_was_mine']
negative = ['fixation_mean', 'cultural_flattening_mean', 'similarity_to_ai_reference']
if 'SCI_score' not in df.columns or df['SCI_score'].notna().sum() < 10:
    cols = [c for c in positive + negative if c in df.columns]
    z = pd.DataFrame(StandardScaler().fit_transform(df[cols]), columns=cols)
    df['SCI_score'] = z[[c for c in positive if c in z]].sum(axis=1) - z[[c for c in negative if c in z]].sum(axis=1)

variables = {
    'Originality': 'originality_mean',
    'Design quality': 'quality_mean',
    'Cultural authenticity': 'cultural_authenticity_mean',
    'Fixation': 'fixation_mean',
    'Cultural flattening': 'cultural_flattening_mean',
    'Ownership': 'felt_output_was_mine',
    'AI reliance': 'ai_reliance',
    'AI-reference similarity': 'similarity_to_ai_reference',
    'Visual diversity': 'visual_diversity_score',
    'SCI': 'SCI_score',
}
conditions = list(df['condition'].dropna().unique())
N = len(df)
k = len(conditions)
rows = []
for label, col in variables.items():
    if col not in df.columns:
        continue
    groups = [df.loc[df['condition'] == cond, col].dropna() for cond in conditions]
    H, p = kruskal(*groups)
    eps2 = (H - k + 1) / (N - k)
    rows.append({'Outcome': label, 'Column': col, 'H': H, 'p': p, 'epsilon_squared': eps2})

res = pd.DataFrame(rows)
res.to_csv(OUT_PATH, index=False)
print(res.to_string(index=False))
print('Saved ' + str(OUT_PATH))
