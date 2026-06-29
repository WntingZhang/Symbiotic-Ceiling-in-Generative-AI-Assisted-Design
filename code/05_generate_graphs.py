from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import minmax_scale, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'dataset.xlsx'
GRAPH_DIR = ROOT / 'graphs'
OUT_DIR = ROOT / 'outputs'
GRAPH_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

df = pd.read_excel(DATA_PATH)
condition_order = ['C1_HumanOnly', 'C2_AIInspiration', 'C3_FreeAICollab', 'C4_AIScaffold']
condition_order = [c for c in condition_order if c in set(df['condition'])]
label_map = {
    'C1_HumanOnly': 'C1 - Human-Only',
    'C2_AIInspiration': 'C2 - AI Inspiration',
    'C3_FreeAICollab': 'C3 - Free AI Collab',
    'C4_AIScaffold': 'C4 - AI Scaffold',
}

# Recompute SCI for plotting if absent/mostly empty.
positive = ['originality_mean', 'quality_mean', 'cultural_authenticity_mean', 'visual_diversity_score', 'felt_output_was_mine']
negative = ['fixation_mean', 'cultural_flattening_mean', 'similarity_to_ai_reference']
if 'SCI_score' not in df.columns or df['SCI_score'].notna().sum() < 10:
    cols = [c for c in positive + negative if c in df.columns]
    z = pd.DataFrame(StandardScaler().fit_transform(df[cols]), columns=cols)
    df['SCI_score'] = z[[c for c in positive if c in z]].sum(axis=1) - z[[c for c in negative if c in z]].sum(axis=1)

means = df.groupby('condition').mean(numeric_only=True).reindex(condition_order)
means.to_csv(OUT_DIR / 'descriptive_condition_means.csv')

# Figure 4: row-standardised heatmap, raw labels.
profile_cols = ['age', 'design_experience_1_7', 'genai_experience_1_7', 'cultural_familiarity_1_7']
profile_labels = ['Age', 'Design Exp.\n(1-7)', 'GenAI Exp.\n(1-7)', 'Cultural Fam.\n(1-7)']
prof = means[profile_cols]
row_std = prof.sub(prof.mean(axis=1), axis=0).div(prof.std(axis=1).replace(0, 1), axis=0)
fig, ax = plt.subplots(figsize=(8, 4.8))
im = ax.imshow(row_std.values, aspect='auto')
ax.set_xticks(range(len(condition_order)), labels=[x.split('_')[0] for x in condition_order], fontweight='bold')
ax.set_yticks(range(len(profile_labels)), labels=profile_labels)
for i in range(prof.shape[0]):
    for j in range(prof.shape[1]):
        ax.text(j, i, f'{prof.iloc[i, j]:.2f}', ha='center', va='center', fontweight='bold')
ax.set_title('Participant Profile by Condition\nrow-standardised colour; labels show raw means', fontweight='bold')
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
fig.tight_layout()
fig.savefig(GRAPH_DIR / 'figure4_participant_profile_heatmap.png', dpi=300)
plt.close(fig)

# Figure 5: radar chart.
radar_cols = ['originality_mean', 'quality_mean', 'cultural_authenticity_mean', 'cultural_specificity_mean', 'stereotype_avoidance_mean']
radar_labels = ['Originality', 'Design\nQuality', 'Cultural\nAuthenticity', 'Cultural\nSpecificity', 'Stereotype\nAvoidance']
angles = np.linspace(0, 2*np.pi, len(radar_cols), endpoint=False).tolist()
angles += angles[:1]
fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, polar=True)
for cond in condition_order:
    vals = means.loc[cond, radar_cols].tolist()
    vals += vals[:1]
    ax.plot(angles, vals, linewidth=2, label=label_map.get(cond, cond))
    ax.fill(angles, vals, alpha=0.08)
ax.set_xticks(angles[:-1], radar_labels)
ax.set_ylim(0, 7)
ax.set_yticks([2, 4, 6])
ax.set_title('Creative and Cultural Outcome Profile by Condition', fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15))
fig.tight_layout()
fig.savefig(GRAPH_DIR / 'figure5_radar_outcome_profile.png', dpi=300)
plt.close(fig)

# Figure 6: agency distributions using violin + jittered points + median line.
agency_cols = ['felt_output_was_mine', 'felt_ai_controlled_direction', 'perceived_control', 'ai_reliance']
agency_titles = ['Felt Output\nOwnership', 'Felt AI\nControlled', 'Perceived\nControl', 'AI Reliance']
fig, axes = plt.subplots(1, 4, figsize=(14, 4.5), sharey=True)
rng = np.random.default_rng(7)
for ax, col, title in zip(axes, agency_cols, agency_titles):
    data = [df.loc[df['condition'] == cond, col].dropna().values for cond in condition_order]
    ax.violinplot(data, positions=np.arange(1, len(data)+1), showmeans=False, showmedians=True, widths=0.75)
    for i, arr in enumerate(data, start=1):
        jitter = rng.normal(i, 0.035, size=len(arr))
        ax.scatter(jitter, arr, s=14, alpha=0.55)
    ax.set_xticks(np.arange(1, len(data)+1), [c.split('_')[0] for c in condition_order])
    ax.set_title(title, fontsize=10, fontweight='bold')
    ax.set_ylim(0.5, 7.5)
    ax.grid(axis='y', alpha=0.25)
axes[0].set_ylabel('Score (1-7)')
fig.suptitle('Agency and Reliance Distributions by Condition', fontweight='bold')
fig.tight_layout()
fig.savefig(GRAPH_DIR / 'figure6_agency_raincloud_plot.png', dpi=300)
plt.close(fig)

# Figure 7: bubble scatter plot.
fig, ax = plt.subplots(figsize=(8, 6))
for cond in condition_order:
    sub = df[df['condition'] == cond]
    size = 25 + sub['ai_reliance'].fillna(0) * 22
    ax.scatter(sub['similarity_to_ai_reference'], sub['visual_diversity_score'], s=size, alpha=0.68, label=label_map.get(cond, cond), edgecolors='white', linewidths=0.5)
ax.axvline(df['similarity_to_ai_reference'].mean(), linestyle='--', linewidth=1, alpha=0.5)
ax.axhline(df['visual_diversity_score'].mean(), linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('Cosine Similarity to AI Reference')
ax.set_ylabel('Visual Diversity Score')
ax.set_title('AI Similarity vs. Visual Diversity\n(bubble size = AI reliance)', fontweight='bold')
ax.text(0.02, df['visual_diversity_score'].max(), 'Low similarity\nHigh diversity\n(ideal)', va='top', fontsize=9)
ax.text(df['similarity_to_ai_reference'].max(), df['visual_diversity_score'].min(), 'High similarity\nLow diversity\n(ceiling risk)', ha='right', va='bottom', fontsize=9)
ax.legend(loc='best')
fig.tight_layout()
fig.savefig(GRAPH_DIR / 'figure7_similarity_diversity_bubble_plot.png', dpi=300)
plt.close(fig)

# Figure 8: parallel coordinates.
parallel_cols = ['originality_mean', 'quality_mean', 'cultural_authenticity_mean', 'visual_diversity_score', 'felt_output_was_mine', 'fixation_mean', 'cultural_flattening_mean', 'similarity_to_ai_reference', 'SCI_score']
parallel_labels = ['Originality', 'Quality', 'Cultural\nAuthenticity', 'Visual\nDiversity', 'Ownership', 'Fixation', 'Cultural\nFlattening', 'AI\nSimilarity', 'SCI']
pm = means[parallel_cols].copy()
norm = pd.DataFrame(minmax_scale(pm), index=pm.index, columns=pm.columns)
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(parallel_cols))
for cond in condition_order:
    ax.plot(x, norm.loc[cond].values, marker='o', linewidth=2, label=label_map.get(cond, cond))
ax.set_xticks(x, parallel_labels)
ax.set_ylabel('Normalised value')
ax.set_title('Outcome Profile Across All Dimensions by Condition', fontweight='bold')
ax.grid(axis='y', alpha=0.25)
ax.legend(loc='lower left')
fig.tight_layout()
fig.savefig(GRAPH_DIR / 'figure8_parallel_coordinates_sci.png', dpi=300)
plt.close(fig)

print('Saved graphs to ' + str(GRAPH_DIR))
