from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'dataset.xlsx'
OUT_PATH = Path(__file__).resolve().parents[1] / 'outputs' / 'sci_scores_recomputed.csv'
OUT_PATH.parent.mkdir(exist_ok=True)

df = pd.read_excel(DATA_PATH)
positive = ['originality_mean', 'quality_mean', 'cultural_authenticity_mean', 'visual_diversity_score', 'felt_output_was_mine']
negative = ['fixation_mean', 'cultural_flattening_mean', 'similarity_to_ai_reference']
needed = [c for c in positive + negative if c in df.columns]

z = pd.DataFrame(StandardScaler().fit_transform(df[needed]), columns=needed)
score = z[[c for c in positive if c in z]].sum(axis=1) - z[[c for c in negative if c in z]].sum(axis=1)
df['SCI_recomputed_zsum'] = score

cols = ['participant_id', 'condition', 'SCI_score', 'SCI_recomputed_zsum']
df[[c for c in cols if c in df.columns]].to_csv(OUT_PATH, index=False)
print(f'Saved {OUT_PATH}')
