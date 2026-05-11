"""
Script to add data modeling cells to code.ipynb
This script reads the existing notebook, adds new cells for:
1. Train/Test Split
2. Model Training (Random Forest, Logistic Regression, SVM)
3. Model Evaluation (accuracy, classification report, confusion matrix)
4. Feature Importance Analysis
"""

import json
import uuid

def make_cell_id():
    return str(uuid.uuid4())[:8]

def make_markdown_cell(source, cell_id=None):
    return {
        "cell_type": "markdown",
        "id": cell_id or make_cell_id(),
        "metadata": {},
        "source": source if isinstance(source, list) else [source]
    }

def make_code_cell(source, cell_id=None):
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id or make_cell_id(),
        "metadata": {},
        "outputs": [],
        "source": source if isinstance(source, list) else [source]
    }

def main():
    notebook_path = r"r:\Data Mining\Praktikum 1\code.ipynb"
    
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
    
    new_cells = []
    
    # --- Section: Data Modeling ---
    new_cells.append(make_markdown_cell(
        "# Data Modeling\n",
        "data-modeling-header"
    ))
    
    # --- Cell: Train/Test Split ---
    new_cells.append(make_markdown_cell(
        "## Train/Test Split",
        "train-test-split-header"
    ))
    
    new_cells.append(make_code_cell([
        "from sklearn.model_selection import train_test_split\n",
        "\n",
        "# Memisahkan fitur (X) dan target (y)\n",
        "X = df.drop('depression_label', axis=1)\n",
        "y = df['depression_label']\n",
        "\n",
        "print(f'Jumlah fitur: {X.shape[1]}')\n",
        "print(f'Fitur: {list(X.columns)}')\n",
        "print(f'\\nDistribusi target:')\n",
        "print(y.value_counts())\n",
        "\n",
        "# Split data: 80% training, 20% testing\n",
        "X_train, X_test, y_train, y_test = train_test_split(\n",
        "    X, y, test_size=0.2, random_state=42, stratify=y\n",
        ")\n",
        "\n",
        "print(f'\\nUkuran data training: {X_train.shape[0]}')\n",
        "print(f'Ukuran data testing: {X_test.shape[0]}')\n",
        "print(f'\\nDistribusi target (training):')\n",
        "print(y_train.value_counts())\n",
        "print(f'\\nDistribusi target (testing):')\n",
        "print(y_test.value_counts())"
    ], "train-test-split-code"))
    
    # --- Section: Model 1 - Random Forest ---
    new_cells.append(make_markdown_cell(
        "## Model 1: Random Forest Classifier",
        "rf-header"
    ))
    
    new_cells.append(make_code_cell([
        "from sklearn.ensemble import RandomForestClassifier\n",
        "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix\n",
        "import seaborn as sns\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "# Inisialisasi dan training model Random Forest\n",
        "rf_model = RandomForestClassifier(\n",
        "    n_estimators=100,\n",
        "    random_state=42,\n",
        "    max_depth=10,\n",
        "    min_samples_split=5,\n",
        "    min_samples_leaf=2\n",
        ")\n",
        "\n",
        "rf_model.fit(X_train, y_train)\n",
        "\n",
        "# Prediksi pada data testing\n",
        "y_pred_rf = rf_model.predict(X_test)\n",
        "\n",
        "# Evaluasi model\n",
        "rf_accuracy = accuracy_score(y_test, y_pred_rf)\n",
        "print('=== Random Forest Classifier ===')\n",
        "print(f'Accuracy: {rf_accuracy:.4f}')\n",
        "print(f'\\nClassification Report:')\n",
        "print(classification_report(y_test, y_pred_rf, target_names=['Tidak Depresi (0)', 'Depresi (1)']))\n",
        "\n",
        "# Confusion Matrix\n",
        "cm_rf = confusion_matrix(y_test, y_pred_rf)\n",
        "plt.figure(figsize=(8, 6))\n",
        "sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues',\n",
        "            xticklabels=['Tidak Depresi', 'Depresi'],\n",
        "            yticklabels=['Tidak Depresi', 'Depresi'])\n",
        "plt.title('Confusion Matrix - Random Forest')\n",
        "plt.ylabel('Aktual')\n",
        "plt.xlabel('Prediksi')\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ], "rf-train-eval"))
    
    # --- Section: Model 2 - Logistic Regression ---
    new_cells.append(make_markdown_cell(
        "## Model 2: Logistic Regression",
        "lr-header"
    ))
    
    new_cells.append(make_code_cell([
        "from sklearn.linear_model import LogisticRegression\n",
        "\n",
        "# Inisialisasi dan training model Logistic Regression\n",
        "lr_model = LogisticRegression(\n",
        "    random_state=42,\n",
        "    max_iter=1000,\n",
        "    solver='lbfgs'\n",
        ")\n",
        "\n",
        "lr_model.fit(X_train, y_train)\n",
        "\n",
        "# Prediksi pada data testing\n",
        "y_pred_lr = lr_model.predict(X_test)\n",
        "\n",
        "# Evaluasi model\n",
        "lr_accuracy = accuracy_score(y_test, y_pred_lr)\n",
        "print('=== Logistic Regression ===')\n",
        "print(f'Accuracy: {lr_accuracy:.4f}')\n",
        "print(f'\\nClassification Report:')\n",
        "print(classification_report(y_test, y_pred_lr, target_names=['Tidak Depresi (0)', 'Depresi (1)']))\n",
        "\n",
        "# Confusion Matrix\n",
        "cm_lr = confusion_matrix(y_test, y_pred_lr)\n",
        "plt.figure(figsize=(8, 6))\n",
        "sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Oranges',\n",
        "            xticklabels=['Tidak Depresi', 'Depresi'],\n",
        "            yticklabels=['Tidak Depresi', 'Depresi'])\n",
        "plt.title('Confusion Matrix - Logistic Regression')\n",
        "plt.ylabel('Aktual')\n",
        "plt.xlabel('Prediksi')\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ], "lr-train-eval"))
    
    # --- Section: Model 3 - SVM ---
    new_cells.append(make_markdown_cell(
        "## Model 3: Support Vector Machine (SVM)",
        "svm-header"
    ))
    
    new_cells.append(make_code_cell([
        "from sklearn.svm import SVC\n",
        "\n",
        "# Inisialisasi dan training model SVM\n",
        "svm_model = SVC(\n",
        "    kernel='rbf',\n",
        "    random_state=42,\n",
        "    C=1.0,\n",
        "    gamma='scale'\n",
        ")\n",
        "\n",
        "svm_model.fit(X_train, y_train)\n",
        "\n",
        "# Prediksi pada data testing\n",
        "y_pred_svm = svm_model.predict(X_test)\n",
        "\n",
        "# Evaluasi model\n",
        "svm_accuracy = accuracy_score(y_test, y_pred_svm)\n",
        "print('=== Support Vector Machine (SVM) ===')\n",
        "print(f'Accuracy: {svm_accuracy:.4f}')\n",
        "print(f'\\nClassification Report:')\n",
        "print(classification_report(y_test, y_pred_svm, target_names=['Tidak Depresi (0)', 'Depresi (1)']))\n",
        "\n",
        "# Confusion Matrix\n",
        "cm_svm = confusion_matrix(y_test, y_pred_svm)\n",
        "plt.figure(figsize=(8, 6))\n",
        "sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Greens',\n",
        "            xticklabels=['Tidak Depresi', 'Depresi'],\n",
        "            yticklabels=['Tidak Depresi', 'Depresi'])\n",
        "plt.title('Confusion Matrix - SVM')\n",
        "plt.ylabel('Aktual')\n",
        "plt.xlabel('Prediksi')\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ], "svm-train-eval"))
    
    # --- Section: Model Comparison ---
    new_cells.append(make_markdown_cell(
        "## Perbandingan Model",
        "comparison-header"
    ))
    
    new_cells.append(make_code_cell([
        "import pandas as pd\n",
        "from sklearn.metrics import precision_score, recall_score, f1_score\n",
        "\n",
        "# Membuat tabel perbandingan model\n",
        "model_names = ['Random Forest', 'Logistic Regression', 'SVM']\n",
        "predictions = [y_pred_rf, y_pred_lr, y_pred_svm]\n",
        "accuracies = [rf_accuracy, lr_accuracy, svm_accuracy]\n",
        "\n",
        "comparison_data = []\n",
        "for name, y_pred, acc in zip(model_names, predictions, accuracies):\n",
        "    comparison_data.append({\n",
        "        'Model': name,\n",
        "        'Accuracy': f'{acc:.4f}',\n",
        "        'Precision': f'{precision_score(y_test, y_pred):.4f}',\n",
        "        'Recall': f'{recall_score(y_test, y_pred):.4f}',\n",
        "        'F1-Score': f'{f1_score(y_test, y_pred):.4f}'\n",
        "    })\n",
        "\n",
        "comparison_df = pd.DataFrame(comparison_data)\n",
        "print('=== Perbandingan Performa Model ===')\n",
        "comparison_df"
    ], "model-comparison-code"))
    
    new_cells.append(make_code_cell([
        "# Visualisasi perbandingan akurasi model\n",
        "fig, ax = plt.subplots(figsize=(10, 6))\n",
        "\n",
        "colors = ['#3498db', '#e74c3c', '#2ecc71']\n",
        "bars = ax.bar(model_names, accuracies, color=colors, edgecolor='black', linewidth=0.5)\n",
        "\n",
        "# Menambahkan label nilai di atas setiap bar\n",
        "for bar, acc in zip(bars, accuracies):\n",
        "    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,\n",
        "            f'{acc:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=12)\n",
        "\n",
        "ax.set_title('Perbandingan Akurasi Model', fontsize=14, fontweight='bold')\n",
        "ax.set_ylabel('Akurasi', fontsize=12)\n",
        "ax.set_xlabel('Model', fontsize=12)\n",
        "ax.set_ylim(0, 1.1)\n",
        "ax.grid(axis='y', alpha=0.3)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ], "accuracy-comparison-chart"))
    
    # --- Section: Feature Importance ---
    new_cells.append(make_markdown_cell(
        "## Feature Importance (Random Forest)",
        "feature-importance-header"
    ))
    
    new_cells.append(make_code_cell([
        "# Analisis Feature Importance dari model Random Forest\n",
        "feature_importance = pd.DataFrame({\n",
        "    'Feature': X.columns,\n",
        "    'Importance': rf_model.feature_importances_\n",
        "}).sort_values('Importance', ascending=False)\n",
        "\n",
        "print('=== Feature Importance (Random Forest) ===')\n",
        "print(feature_importance.to_string(index=False))\n",
        "\n",
        "# Visualisasi Feature Importance\n",
        "plt.figure(figsize=(12, 6))\n",
        "sns.barplot(data=feature_importance, x='Importance', y='Feature',\n",
        "            palette='viridis')\n",
        "plt.title('Feature Importance - Random Forest', fontsize=14, fontweight='bold')\n",
        "plt.xlabel('Importance', fontsize=12)\n",
        "plt.ylabel('Feature', fontsize=12)\n",
        "plt.tight_layout()\n",
        "plt.show()"
    ], "feature-importance-code"))
    
    # --- Section: Conclusion ---
    new_cells.append(make_markdown_cell([
        "## Kesimpulan\n",
        "\n",
        "Dari hasil modeling di atas, dapat disimpulkan:\n",
        "\n",
        "1. **Train/Test Split**: Dataset dibagi menjadi 80% data training dan 20% data testing dengan stratified sampling untuk menjaga distribusi kelas yang seimbang.\n",
        "\n",
        "2. **Model yang Digunakan**: Tiga model klasifikasi telah dilatih dan dievaluasi:\n",
        "   - Random Forest Classifier\n",
        "   - Logistic Regression\n",
        "   - Support Vector Machine (SVM)\n",
        "\n",
        "3. **Evaluasi**: Setiap model dievaluasi menggunakan metrik accuracy, precision, recall, dan F1-score.\n",
        "\n",
        "4. **Feature Importance**: Analisis feature importance dari Random Forest menunjukkan fitur-fitur yang paling berpengaruh dalam prediksi label depresi pada remaja."
    ], "conclusion-header"))
    
    # Append new cells to notebook
    notebook["cells"].extend(new_cells)
    
    # Write back
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    
    print(f"Successfully added {len(new_cells)} cells to the notebook.")
    print("New cells added:")
    for cell in new_cells:
        cell_type = cell["cell_type"]
        cell_id = cell["id"]
        preview = cell["source"][0][:60] if cell["source"] else "(empty)"
        print(f"  [{cell_type}] id={cell_id}: {preview}...")

if __name__ == "__main__":
    main()
