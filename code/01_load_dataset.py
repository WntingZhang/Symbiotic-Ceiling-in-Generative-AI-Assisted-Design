from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'dataset.xlsx'

if not DATA_PATH.exists():
    raise FileNotFoundError('Place your Excel dataset at data/dataset.xlsx')

df = pd.read_excel(DATA_PATH)
print('Dataset shape:', df.shape)
print('
Columns:')
for col in df.columns:
    print('-', col)
print('
Condition counts:')
print(df['condition'].value_counts())
