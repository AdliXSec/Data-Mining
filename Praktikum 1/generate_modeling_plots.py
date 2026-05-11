import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             precision_score, recall_score, f1_score, roc_curve, auc)
import os, json, warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 150

img_dir = 'images_modeling'
os.makedirs(img_dir, exist_ok=True)

# ========== LOAD & PREPROCESS (same as notebook) ==========
df = pd.read_csv('Teen_Mental_Health_Dataset.csv')
le_gender = LabelEncoder()
df['gender'] = le_gender.fit_transform(df['gender'])
social_mapping = {'low': 0, 'medium': 1, 'high': 2}
df['social_interaction_level'] = df['social_interaction_level'].map(social_mapping)
df = pd.get_dummies(df, columns=['platform_usage'], prefix='platform')
features_to_scale = ['age', 'daily_social_media_hours', 'sleep_hours', 'screen_time_before_sleep',
                     'academic_performance', 'physical_activity', 'stress_level',
                     'anxiety_level', 'addiction_level']
scaler = StandardScaler()
df[features_to_scale] = scaler.fit_transform(df[features_to_scale])

# ========== SPLIT DATA ==========
X = df.drop('depression_label', axis=1)
y = df['depression_label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

results = {}

# ===== 1. PLOT: Distribusi Target =====
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
# Full dataset
counts_full = y.value_counts()
bars = axes[0].bar(['Tidak Depresi (0)', 'Depresi (1)'], counts_full.values,
                   color=['#3498DB', '#E74C3C'], edgecolor='white', linewidth=2)
for b, v in zip(bars, counts_full.values):
    axes[0].text(b.get_x()+b.get_width()/2, b.get_height()+10, str(v), ha='center', fontweight='bold')
axes[0].set_title('Distribusi Target — Full Dataset', fontweight='bold')
axes[0].set_ylabel('Jumlah')

# Train vs Test
x_pos = np.arange(2)
w = 0.35
train_counts = y_train.value_counts().sort_index()
test_counts = y_test.value_counts().sort_index()
b1 = axes[1].bar(x_pos - w/2, train_counts.values, w, label='Training (80%)', color='#2ECC71', edgecolor='white')
b2 = axes[1].bar(x_pos + w/2, test_counts.values, w, label='Testing (20%)', color='#F39C12', edgecolor='white')
for b, v in zip(b1, train_counts.values):
    axes[1].text(b.get_x()+b.get_width()/2, b.get_height()+5, str(v), ha='center', fontweight='bold', fontsize=9)
for b, v in zip(b2, test_counts.values):
    axes[1].text(b.get_x()+b.get_width()/2, b.get_height()+5, str(v), ha='center', fontweight='bold', fontsize=9)
axes[1].set_xticks(x_pos)
axes[1].set_xticklabels(['Tidak Depresi (0)', 'Depresi (1)'])
axes[1].set_title('Distribusi Target — Train vs Test', fontweight='bold')
axes[1].set_ylabel('Jumlah')
axes[1].legend()
plt.tight_layout()
plt.savefig(f'{img_dir}/01_split_distribution.png', bbox_inches='tight')
plt.close()
print("1/8 split distribution done")

# ===== TRAIN MODELS =====
# Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10,
                                  min_samples_split=5, min_samples_leaf=2)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, y_pred_rf)
rf_train_acc = accuracy_score(y_train, rf_model.predict(X_train))

# Logistic Regression
lr_model = LogisticRegression(random_state=42, max_iter=1000, solver='lbfgs')
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
lr_acc = accuracy_score(y_test, y_pred_lr)
lr_train_acc = accuracy_score(y_train, lr_model.predict(X_train))

# SVM
svm_model = SVC(kernel='rbf', random_state=42, C=1.0, gamma='scale', probability=True)
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)
svm_acc = accuracy_score(y_test, y_pred_svm)
svm_train_acc = accuracy_score(y_train, svm_model.predict(X_train))

models_info = {
    'Random Forest': {'pred': y_pred_rf, 'acc': rf_acc, 'train_acc': rf_train_acc, 'model': rf_model},
    'Logistic Regression': {'pred': y_pred_lr, 'acc': lr_acc, 'train_acc': lr_train_acc, 'model': lr_model},
    'SVM': {'pred': y_pred_svm, 'acc': svm_acc, 'train_acc': svm_train_acc, 'model': svm_model}
}

# ===== 2. CONFUSION MATRICES =====
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
cmaps = ['Blues', 'Oranges', 'Greens']
for idx, (name, info) in enumerate(models_info.items()):
    cm = confusion_matrix(y_test, info['pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmaps[idx], ax=axes[idx],
                xticklabels=['Tidak Depresi', 'Depresi'],
                yticklabels=['Tidak Depresi', 'Depresi'],
                annot_kws={'size': 14, 'fontweight': 'bold'})
    axes[idx].set_title(f'Confusion Matrix\n{name}', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel('Aktual')
    axes[idx].set_xlabel('Prediksi')
plt.tight_layout()
plt.savefig(f'{img_dir}/02_confusion_matrices.png', bbox_inches='tight')
plt.close()
print("2/8 confusion matrices done")

# ===== 3. CLASSIFICATION REPORT as image =====
fig, axes = plt.subplots(1, 3, figsize=(18, 4))
for idx, (name, info) in enumerate(models_info.items()):
    ax = axes[idx]
    ax.axis('off')
    report = classification_report(y_test, info['pred'], target_names=['Tidak Depresi (0)', 'Depresi (1)'])
    ax.text(0.05, 0.95, f"=== {name} ===\n\n{report}", transform=ax.transAxes,
            fontsize=9, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#F0F0F0', alpha=0.9))
plt.suptitle('Classification Report — Ketiga Model', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{img_dir}/03_classification_reports.png', bbox_inches='tight')
plt.close()
print("3/8 classification reports done")

# ===== 4. MODEL COMPARISON BAR CHART =====
names = list(models_info.keys())
accs = [models_info[n]['acc'] for n in names]
precs = [precision_score(y_test, models_info[n]['pred']) for n in names]
recs = [recall_score(y_test, models_info[n]['pred']) for n in names]
f1s = [f1_score(y_test, models_info[n]['pred']) for n in names]

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(names))
w = 0.2
colors = ['#3498DB', '#E74C3C', '#2ECC71', '#9B59B6']
metrics = [accs, precs, recs, f1s]
labels = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
for i, (vals, label, color) in enumerate(zip(metrics, labels, colors)):
    bars = ax.bar(x + i*w, vals, w, label=label, color=color, edgecolor='white', linewidth=1)
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.005, f'{v:.3f}',
                ha='center', va='bottom', fontsize=8, fontweight='bold')
ax.set_xticks(x + 1.5*w)
ax.set_xticklabels(names, fontsize=11)
ax.set_ylim(0, 1.15)
ax.set_ylabel('Skor', fontsize=12)
ax.set_title('Perbandingan Performa Model', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{img_dir}/04_model_comparison.png', bbox_inches='tight')
plt.close()
print("4/8 model comparison done")

# ===== 5. ACCURACY COMPARISON SIMPLE =====
fig, ax = plt.subplots(figsize=(10, 5))
colors_bar = ['#3498DB', '#E74C3C', '#2ECC71']
bars = ax.bar(names, accs, color=colors_bar, edgecolor='black', linewidth=0.5, width=0.5)
for b, v in zip(bars, accs):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.008, f'{v:.4f}',
            ha='center', va='bottom', fontweight='bold', fontsize=13)
ax.set_title('Perbandingan Akurasi Model', fontsize=14, fontweight='bold')
ax.set_ylabel('Akurasi', fontsize=12)
ax.set_ylim(0, 1.12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{img_dir}/05_accuracy_comparison.png', bbox_inches='tight')
plt.close()
print("5/8 accuracy comparison done")

# ===== 6. FEATURE IMPORTANCE =====
fi = pd.DataFrame({'Feature': X.columns, 'Importance': rf_model.feature_importances_})
fi = fi.sort_values('Importance', ascending=True)

fig, ax = plt.subplots(figsize=(10, 7))
bars = ax.barh(fi['Feature'], fi['Importance'], color=plt.cm.viridis(np.linspace(0.2, 0.9, len(fi))))
for b, v in zip(bars, fi['Importance']):
    ax.text(v + 0.003, b.get_y()+b.get_height()/2, f'{v:.4f}', va='center', fontsize=8)
ax.set_title('Feature Importance — Random Forest', fontsize=14, fontweight='bold')
ax.set_xlabel('Importance', fontsize=12)
plt.tight_layout()
plt.savefig(f'{img_dir}/06_feature_importance.png', bbox_inches='tight')
plt.close()
print("6/8 feature importance done")

# ===== 7. TRAIN vs TEST ACCURACY (Overfitting check) =====
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(names))
w = 0.3
train_accs = [models_info[n]['train_acc'] for n in names]
test_accs = [models_info[n]['acc'] for n in names]
b1 = ax.bar(x - w/2, train_accs, w, label='Training Accuracy', color='#2ECC71', edgecolor='white')
b2 = ax.bar(x + w/2, test_accs, w, label='Testing Accuracy', color='#E74C3C', edgecolor='white')
for b, v in zip(b1, train_accs):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.005, f'{v:.4f}', ha='center', fontweight='bold', fontsize=10)
for b, v in zip(b2, test_accs):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.005, f'{v:.4f}', ha='center', fontweight='bold', fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=11)
ax.set_ylim(0, 1.15)
ax.set_title('Training vs Testing Accuracy (Overfitting Check)', fontsize=14, fontweight='bold')
ax.set_ylabel('Akurasi')
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{img_dir}/07_overfit_check.png', bbox_inches='tight')
plt.close()
print("7/8 overfitting check done")

# ===== 8. COMPARISON TABLE as image =====
comp_data = []
for name in names:
    pred = models_info[name]['pred']
    comp_data.append([
        name,
        f"{models_info[name]['train_acc']:.4f}",
        f"{models_info[name]['acc']:.4f}",
        f"{precision_score(y_test, pred):.4f}",
        f"{recall_score(y_test, pred):.4f}",
        f"{f1_score(y_test, pred):.4f}"
    ])

fig, ax = plt.subplots(figsize=(14, 2.5))
ax.axis('off')
col_labels = ['Model', 'Train Acc', 'Test Acc', 'Precision', 'Recall', 'F1-Score']
tbl = ax.table(cellText=comp_data, colLabels=col_labels, cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 1.8)
for (row, col), cell in tbl.get_celld().items():
    if row == 0:
        cell.set_facecolor('#2C3E50')
        cell.set_text_props(color='white', fontweight='bold')
    else:
        cell.set_facecolor('#ECF0F1' if row % 2 == 0 else 'white')
plt.title('Tabel Perbandingan Performa Model', fontweight='bold', fontsize=13, pad=20)
plt.tight_layout()
plt.savefig(f'{img_dir}/08_comparison_table.png', bbox_inches='tight')
plt.close()
print("8/8 comparison table done")

# ===== SAVE METRICS TO JSON for report =====
report_data = {}
for name in names:
    pred = models_info[name]['pred']
    cm = confusion_matrix(y_test, pred)
    report_data[name] = {
        'train_acc': round(models_info[name]['train_acc'], 4),
        'test_acc': round(models_info[name]['acc'], 4),
        'precision': round(precision_score(y_test, pred), 4),
        'recall': round(recall_score(y_test, pred), 4),
        'f1': round(f1_score(y_test, pred), 4),
        'cm': cm.tolist()
    }
report_data['split'] = {
    'total': len(y),
    'train': len(y_train),
    'test': len(y_test),
    'train_0': int((y_train==0).sum()),
    'train_1': int((y_train==1).sum()),
    'test_0': int((y_test==0).sum()),
    'test_1': int((y_test==1).sum()),
    'features': list(X.columns),
    'n_features': X.shape[1]
}
fi_sorted = fi.sort_values('Importance', ascending=False)
report_data['feature_importance'] = {r['Feature']: round(r['Importance'],4) for _,r in fi_sorted.iterrows()}

with open('modeling_results.json', 'w') as f:
    json.dump(report_data, f, indent=2)

print("\n=== Semua 8 gambar + metrics JSON berhasil di-generate ===")
