import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 150

df = pd.read_csv('Teen_Mental_Health_Dataset.csv')
img_dir = 'images'
os.makedirs(img_dir, exist_ok=True)

# ========== 1. df.head() screenshot as table image ==========
fig, ax = plt.subplots(figsize=(14, 3))
ax.axis('off')
tbl = ax.table(cellText=df.head(10).values,
               colLabels=df.columns,
               cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(7)
tbl.scale(1, 1.4)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor('#2E86C1')
        cell.set_text_props(color='white', fontweight='bold')
    else:
        cell.set_facecolor('#F8F9FA' if row % 2 == 0 else 'white')
plt.title('10 Baris Pertama Dataset (df.head(10))', fontweight='bold', fontsize=12, pad=20)
plt.tight_layout()
plt.savefig(f'{img_dir}/01_head.png', bbox_inches='tight')
plt.close()
print("1/10 head done")

# ========== 2. df.info() as text image ==========
from io import StringIO
buf = StringIO()
df.info(buf=buf)
info_text = buf.getvalue()

fig, ax = plt.subplots(figsize=(8, 5))
ax.axis('off')
ax.text(0.05, 0.95, info_text, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='#F0F0F0', alpha=0.8))
plt.title('Informasi Dataset (df.info())', fontweight='bold', fontsize=12)
plt.tight_layout()
plt.savefig(f'{img_dir}/02_info.png', bbox_inches='tight')
plt.close()
print("2/10 info done")

# ========== 3. describe() as table image ==========
desc = df.describe().round(2)
fig, ax = plt.subplots(figsize=(14, 4))
ax.axis('off')
tbl = ax.table(cellText=desc.values,
               colLabels=desc.columns,
               rowLabels=desc.index,
               cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(7.5)
tbl.scale(1, 1.5)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor('#2E86C1')
        cell.set_text_props(color='white', fontweight='bold')
    if col == -1:
        cell.set_facecolor('#D6EAF8')
        cell.set_text_props(fontweight='bold')
plt.title('Statistik Deskriptif (df.describe())', fontweight='bold', fontsize=12, pad=20)
plt.tight_layout()
plt.savefig(f'{img_dir}/03_describe.png', bbox_inches='tight')
plt.close()
print("3/10 describe done")

# ========== 4. Distribution plots for numerical ==========
num_cols = ['age', 'daily_social_media_hours', 'sleep_hours', 'screen_time_before_sleep',
            'academic_performance', 'physical_activity', 'stress_level', 'anxiety_level', 
            'addiction_level', 'depression_label']
fig, axes = plt.subplots(2, 5, figsize=(18, 7))
axes = axes.flatten()
colors = ['#3498DB', '#E74C3C', '#2ECC71', '#9B59B6', '#F39C12',
          '#1ABC9C', '#E67E22', '#2980B9', '#C0392B', '#8E44AD']
for idx, col in enumerate(num_cols):
    ax = axes[idx]
    ax.hist(df[col], bins=15, color=colors[idx], edgecolor='white', alpha=0.85)
    ax.set_title(col, fontsize=9, fontweight='bold')
    ax.set_xlabel('')
    ax.set_ylabel('Frekuensi', fontsize=8)
    ax.tick_params(labelsize=7)
plt.suptitle('Distribusi Variabel Numerik', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{img_dir}/04_dist_numerical.png', bbox_inches='tight')
plt.close()
print("4/10 dist numerical done")

# ========== 5. Bar plots for categorical ==========
cat_cols = ['gender', 'platform_usage', 'social_interaction_level']
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
palette = [['#3498DB', '#E74C3C'], ['#9B59B6', '#F39C12', '#1ABC9C'], ['#E67E22', '#2ECC71', '#3498DB']]
for idx, col in enumerate(cat_cols):
    ax = axes[idx]
    counts = df[col].value_counts()
    bars = ax.bar(counts.index, counts.values, color=palette[idx], edgecolor='white', linewidth=1.5)
    ax.set_title(col, fontsize=11, fontweight='bold')
    ax.set_ylabel('Frekuensi', fontsize=9)
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 8,
                str(val), ha='center', va='bottom', fontweight='bold', fontsize=9)
    ax.tick_params(labelsize=9)
plt.suptitle('Distribusi Variabel Kategorikal (Bar Plot)', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{img_dir}/05_barplot_categorical.png', bbox_inches='tight')
plt.close()
print("5/10 barplot done")

# ========== 6. Pie charts for categorical ==========
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
for idx, col in enumerate(cat_cols):
    ax = axes[idx]
    counts = df[col].value_counts()
    wedges, texts, autotexts = ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%',
                                       colors=palette[idx], startangle=90, 
                                       textprops={'fontsize': 9})
    for at in autotexts:
        at.set_fontweight('bold')
    ax.set_title(col, fontsize=11, fontweight='bold')
plt.suptitle('Distribusi Variabel Kategorikal (Pie Chart)', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{img_dir}/06_piechart_categorical.png', bbox_inches='tight')
plt.close()
print("6/10 pie done")

# ========== 7. Boxplot for outlier detection ==========
fig, axes = plt.subplots(2, 5, figsize=(18, 7))
axes = axes.flatten()
for idx, col in enumerate(num_cols):
    ax = axes[idx]
    bp = ax.boxplot(df[col], patch_artist=True, boxprops=dict(facecolor=colors[idx], alpha=0.7),
                    medianprops=dict(color='black', linewidth=2),
                    whiskerprops=dict(linewidth=1.5),
                    flierprops=dict(marker='o', markerfacecolor='red', markersize=5))
    ax.set_title(col, fontsize=9, fontweight='bold')
    ax.tick_params(labelsize=7)
plt.suptitle('Boxplot untuk Deteksi Outlier', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{img_dir}/07_boxplot.png', bbox_inches='tight')
plt.close()
print("7/10 boxplot done")

# ========== 8. Missing values heatmap ==========
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(df.isnull().astype(int), cbar=True, cmap='YlOrRd', yticklabels=False, ax=ax)
ax.set_title('Heatmap Missing Values', fontsize=13, fontweight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=9)
plt.tight_layout()
plt.savefig(f'{img_dir}/08_missing_heatmap.png', bbox_inches='tight')
plt.close()
print("8/10 missing heatmap done")

# ========== 9. After encoding - head ==========
from sklearn.preprocessing import LabelEncoder, StandardScaler
df_transformed = df.copy()
le = LabelEncoder()
df_transformed['gender'] = le.fit_transform(df_transformed['gender'])
social_map = {'low': 0, 'medium': 1, 'high': 2}
df_transformed['social_interaction_level'] = df_transformed['social_interaction_level'].map(social_map)
df_transformed = pd.get_dummies(df_transformed, columns=['platform_usage'], prefix='platform')

features_to_scale = ['age', 'daily_social_media_hours', 'sleep_hours', 'screen_time_before_sleep',
                     'academic_performance', 'physical_activity', 'stress_level',
                     'anxiety_level', 'addiction_level']
scaler = StandardScaler()
df_transformed[features_to_scale] = scaler.fit_transform(df_transformed[features_to_scale])

fig, ax = plt.subplots(figsize=(16, 3.5))
ax.axis('off')
display_df = df_transformed.head(5).round(2)
tbl = ax.table(cellText=display_df.values,
               colLabels=display_df.columns,
               cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(6.5)
tbl.scale(1, 1.5)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor('#27AE60')
        cell.set_text_props(color='white', fontweight='bold')
    else:
        cell.set_facecolor('#F8F9FA' if row % 2 == 0 else 'white')
plt.title('Data Setelah Encoding & Standardisasi (5 Baris Pertama)', fontweight='bold', fontsize=12, pad=20)
plt.tight_layout()
plt.savefig(f'{img_dir}/09_after_transform.png', bbox_inches='tight')
plt.close()
print("9/10 after transform done")

# ========== 10. Correlation heatmap ==========
fig, ax = plt.subplots(figsize=(13, 10))
corr = df_transformed.corr()
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax,
            linewidths=0.5, vmin=-1, vmax=1, annot_kws={'size': 7},
            square=True)
ax.set_title('Correlation Matrix Setelah Preprocessing', fontsize=14, fontweight='bold', pad=15)
ax.tick_params(labelsize=8)
plt.tight_layout()
plt.savefig(f'{img_dir}/10_correlation_heatmap.png', bbox_inches='tight')
plt.close()
print("10/10 correlation done")

print("\n=== Semua 10 gambar berhasil di-generate di folder images/ ===")
