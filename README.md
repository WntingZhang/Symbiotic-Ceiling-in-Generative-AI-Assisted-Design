# Symbiotic Ceiling Study

Reproducible analysis folder for the Symbiotic Ceiling Study.

## Folder structure

```text
symbiotic-ceiling-study/
│
├── README.md
├── requirements.txt
│
├── data/                     # intentionally empty in this ZIP
│   └── .gitkeep
│
├── code/
│   ├── 01_load_dataset.py
│   ├── 02_compute_similarity_metrics.py
│   ├── 03_compute_sci_score.py
│   ├── 04_statistical_tests.py
│   └── 05_generate_graphs.py
│
├── graphs/
│   ├── figure4_participant_profile_heatmap.png
│   ├── figure5_radar_outcome_profile.png
│   ├── figure6_agency_raincloud_plot.png
│   ├── figure7_similarity_diversity_bubble_plot.png
│   └── figure8_parallel_coordinates_sci.png
│
└── outputs/
    ├── descriptive_condition_means.csv
    └── kruskal_wallis_results.csv
```

## How to rerun

1. Put your Excel dataset inside `data/` and name it `dataset.xlsx`.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
python code/01_load_dataset.py
python code/03_compute_sci_score.py
python code/04_statistical_tests.py
python code/05_generate_graphs.py
```

The `data/` folder is intentionally empty in this ZIP as requested.
