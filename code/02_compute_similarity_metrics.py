"""Optional image-similarity script.

The uploaded dataset already contains these columns:
- similarity_to_ai_reference
- within_group_similarity
- visual_diversity_score

If actual image files are available, replace the placeholder section below with CLIP
embeddings and cosine-similarity computation.
"""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'dataset.xlsx'
OUT_PATH = Path(__file__).resolve().parents[1] / 'outputs' / 'similarity_metrics_preview.csv'
OUT_PATH.parent.mkdir(exist_ok=True)

df = pd.read_excel(DATA_PATH)
cols = ['participant_id', 'condition', 'similarity_to_ai_reference', 'within_group_similarity', 'visual_diversity_score']
existing = [c for c in cols if c in df.columns]
df[existing].to_csv(OUT_PATH, index=False)
print(f'Saved {OUT_PATH}')
