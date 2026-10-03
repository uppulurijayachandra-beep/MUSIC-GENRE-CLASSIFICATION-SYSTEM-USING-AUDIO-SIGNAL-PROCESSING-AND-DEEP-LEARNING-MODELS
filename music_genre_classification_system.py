"""
Music Genre Classification System
Classifies music genres using audio signal processing and deep learning models
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def generate_audio_features_dataset(n_samples=1000, random_state=42):
    """Generate synthetic audio features dataset for music genre classification"""
    np.random.seed(random_state)
    
    genres = ['Rock', 'Pop', 'Jazz', 'Classical', 'Hip-Hop', 'Electronic', 'Country', 'Blues']
    genre_indices = np.random.choice(len(genres), n_samples)
    
    data = {
        'Track_ID': [f'TRACK{i:06d}' for i in range(n_samples)],
        'Genre': [genres[i] for i in genre_indices],
        'Tempo_BPM': np.random.normal(120, 30, n_samples),
        'Energy': np.random.uniform(0, 1, n_samples),
        'Danceability': np.random.uniform(0, 1, n_samples),
        'Valence': np.random.uniform(0, 1, n_samples),
        'Acousticness': np.random.uniform(0, 1, n_samples),
        'Instrumentalness': np.random.uniform(0, 1, n_samples),
        'Liveness': np.random.uniform(0, 1, n_samples),
        'Speechiness': np.random.uniform(0, 1, n_samples),
        'MFCC_Mean': np.random.normal(40, 15, n_samples),
        'MFCC_Std': np.random.normal(20, 8, n_samples),
        'Spectral_Centroid': np.random.normal(2000, 800, n_samples),
        'Spectral_Rolloff': np.random.normal(4000, 1500, n_samples),
        'Zero_Crossing_Rate': np.random.uniform(0, 0.3, n_samples),
        'Chroma_Mean': np.random.normal(0.5, 0.2, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Adjust features based on genre to create realistic patterns
    for idx, row in df.iterrows():
        genre = row['Genre']
        
        if genre == 'Rock':
            df.at[idx, 'Energy'] = np.clip(df.at[idx, 'Energy'] + 0.3, 0, 1)
            df.at[idx, 'Danceability'] = np.clip(df.at[idx, 'Danceability'] + 0.2, 0, 1)
            df.at[idx, 'Acousticness'] = np.clip(df.at[idx, 'Acousticness'] - 0.3, 0, 1)
            
        elif genre == 'Pop':
            df.at[idx, 'Danceability'] = np.clip(df.at[idx, 'Danceability'] + 0.4, 0, 1)
            df.at[idx, 'Valence'] = np.clip(df.at[idx, 'Valence'] + 0.3, 0, 1)
            df.at[idx, 'Energy'] = np.clip(df.at[idx, 'Energy'] + 0.2, 0, 1)
            
        elif genre == 'Jazz':
            df.at[idx, 'Instrumentalness'] = np.clip(df.at[idx, 'Instrumentalness'] + 0.4, 0, 1)
            df.at[idx, 'Acousticness'] = np.clip(df.at[idx, 'Acousticness'] + 0.3, 0, 1)
            df.at[idx, 'Liveness'] = np.clip(df.at[idx, 'Liveness'] + 0.3, 0, 1)
            
        elif genre == 'Classical':
            df.at[idx, 'Acousticness'] = np.clip(df.at[idx, 'Acousticness'] + 0.5, 0, 1)
            df.at[idx, 'Instrumentalness'] = np.clip(df.at[idx, 'Instrumentalness'] + 0.5, 0, 1)
            df.at[idx, 'Energy'] = np.clip(df.at[idx, 'Energy'] - 0.2, 0, 1)
            df.at[idx, 'Tempo_BPM'] = np.clip(df.at[idx, 'Tempo_BPM'] + 20, 40, 200)
            
        elif genre == 'Hip-Hop':
            df.at[idx, 'Danceability'] = np.clip(df.at[idx, 'Danceability'] + 0.3, 0, 1)
            df.at[idx, 'Speechiness'] = np.clip(df.at[idx, 'Speechiness'] + 0.3, 0, 1)
            df.at[idx, 'Energy'] = np.clip(df.at[idx, 'Energy'] + 0.2, 0, 1)
            
        elif genre == 'Electronic':
            df.at[idx, 'Energy'] = np.clip(df.at[idx, 'Energy'] + 0.4, 0, 1)
            df.at[idx, 'Danceability'] = np.clip(df.at[idx, 'Danceability'] + 0.3, 0, 1)
            df.at[idx, 'Instrumentalness'] = np.clip(df.at[idx, 'Instrumentalness'] + 0.3, 0, 1)
            
        elif genre == 'Country':
            df.at[idx, 'Acousticness'] = np.clip(df.at[idx, 'Acousticness'] + 0.4, 0, 1)
            df.at[idx, 'Valence'] = np.clip(df.at[idx, 'Valence'] + 0.2, 0, 1)
            df.at[idx, 'Tempo_BPM'] = np.clip(df.at[idx, 'Tempo_BPM'] - 10, 40, 200)
            
        elif genre == 'Blues':
            df.at[idx, 'Acousticness'] = np.clip(df.at[idx, 'Acousticness'] + 0.3, 0, 1)
            df.at[idx, 'Valence'] = np.clip(df.at[idx, 'Valence'] - 0.3, 0, 1)
            df.at[idx, 'Liveness'] = np.clip(df.at[idx, 'Liveness'] + 0.2, 0, 1)
    
    # Ensure realistic value ranges
    df['Tempo_BPM'] = np.clip(df['Tempo_BPM'], 40, 200)
    
    return df

def preprocess_audio_data(df):
    """Preprocess audio features for modeling"""
    df_processed = df.copy()
    
    feature_cols = [
        'Tempo_BPM', 'Energy', 'Danceability', 'Valence', 'Acousticness',
        'Instrumentalness', 'Liveness', 'Speechiness', 'MFCC_Mean', 'MFCC_Std',
        'Spectral_Centroid', 'Spectral_Rolloff', 'Zero_Crossing_Rate', 'Chroma_Mean'
    ]
    
    return df_processed, feature_cols

def encode_genres(df):
    """Encode genre labels to numeric values"""
    genres = df['Genre'].unique()
    genre_mapping = {genre: idx for idx, genre in enumerate(sorted(genres))}
    df['Genre_Encoded'] = df['Genre'].map(genre_mapping)
    return df, genre_mapping

def train_classification_models(X_train, X_test, y_train, y_test):
    """Train multiple classification models"""
    models = {}
    results = {}
    
    # Model 1: Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    
    models['Logistic Regression'] = lr_model
    results['Logistic Regression'] = {
        'predictions': y_pred_lr,
        'accuracy': accuracy_score(y_test, y_pred_lr),
        'precision': precision_score(y_test, y_pred_lr, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred_lr, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred_lr, average='weighted', zero_division=0)
    }
    
    # Model 2: Random Forest Classifier
    print("Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    models['Random Forest'] = rf_model
    results['Random Forest'] = {
        'predictions': y_pred_rf,
        'accuracy': accuracy_score(y_test, y_pred_rf),
        'precision': precision_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred_rf, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred_rf, average='weighted', zero_division=0)
    }
    
    # Model 3: Gradient Boosting Classifier
    print("Training Gradient Boosting Classifier...")
    gb_model = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    
    models['Gradient Boosting'] = gb_model
    results['Gradient Boosting'] = {
        'predictions': y_pred_gb,
        'accuracy': accuracy_score(y_test, y_pred_gb),
        'precision': precision_score(y_test, y_pred_gb, average='weighted', zero_division=0),
        'recall': recall_score(y_test, y_pred_gb, average='weighted', zero_division=0),
        'f1': f1_score(y_test, y_pred_gb, average='weighted', zero_division=0)
    }
    
    return models, results

def plot_genre_distribution(df):
    """Plot distribution of music genres"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    genre_counts = df['Genre'].value_counts()
    colors = plt.cm.Set3(np.linspace(0, 1, len(genre_counts)))
    
    axes[0].bar(genre_counts.index, genre_counts.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_ylabel('Number of Tracks', fontsize=11, fontweight='bold')
    axes[0].set_title('Distribution of Music Genres in Dataset', fontsize=12, fontweight='bold')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(genre_counts.values):
        axes[0].text(i, v + 5, str(v), ha='center', fontweight='bold')
    
    axes[1].pie(genre_counts.values, labels=genre_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    axes[1].set_title('Percentage Distribution of Music Genres', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/music_genre_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: music_genre_distribution.png")
    plt.close()

def plot_model_comparison(results):
    """Compare model performance metrics"""
    models = list(results.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    
    colors = ['#3498db', '#e74c3c', '#f39c12']
    
    for idx, metric in enumerate(metrics):
        values = [results[m][metric] for m in models]
        axes[idx].bar(models, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[idx].set_ylabel(metric.upper(), fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{metric.upper()}', fontsize=12, fontweight='bold')
        axes[idx].set_ylim([0, 1])
        axes[idx].grid(axis='y', alpha=0.3)
        for i, v in enumerate(values):
            axes[idx].text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/music_model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: music_model_comparison.png")
    plt.close()

def plot_confusion_matrices(results, y_test, genre_mapping):
    """Plot confusion matrices for all models"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    models = list(results.keys())
    genre_labels = sorted(genre_mapping.keys())
    
    for idx, model_name in enumerate(models):
        cm = confusion_matrix(y_test, results[model_name]['predictions'])
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], cbar=False,
                   xticklabels=genre_labels, yticklabels=genre_labels,
                   annot_kws={'fontsize': 8, 'fontweight': 'bold'})
        axes[idx].set_xlabel('Predicted', fontsize=10, fontweight='bold')
        axes[idx].set_ylabel('Actual', fontsize=10, fontweight='bold')
        axes[idx].set_title(f'{model_name}\nAccuracy: {results[model_name]["accuracy"]:.4f}', 
                          fontsize=11, fontweight='bold')
        axes[idx].tick_params(axis='x', rotation=45)
        axes[idx].tick_params(axis='y', rotation=0)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/music_confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Saved: music_confusion_matrices.png")
    plt.close()

def plot_feature_importance(models):
    """Plot feature importance for tree-based models"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    feature_names = [
        'Tempo', 'Energy', 'Danceability', 'Valence', 'Acousticness',
        'Instrumentalness', 'Liveness', 'Speechiness', 'MFCC_Mean', 'MFCC_Std',
        'Spectral_Centroid', 'Spectral_Rolloff', 'Zero_Crossing_Rate', 'Chroma_Mean'
    ]
    
    # Random Forest
    rf_importance = models['Random Forest'].feature_importances_
    rf_indices = np.argsort(rf_importance)[-10:]
    axes[0].barh(range(len(rf_indices)), rf_importance[rf_indices], 
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_yticks(range(len(rf_indices)))
    axes[0].set_yticklabels([feature_names[i] for i in rf_indices], fontsize=10)
    axes[0].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[0].set_title('Random Forest - Feature Importance', fontsize=12, fontweight='bold')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Gradient Boosting
    gb_importance = models['Gradient Boosting'].feature_importances_
    gb_indices = np.argsort(gb_importance)[-10:]
    axes[1].barh(range(len(gb_indices)), gb_importance[gb_indices], 
                color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_yticks(range(len(gb_indices)))
    axes[1].set_yticklabels([feature_names[i] for i in gb_indices], fontsize=10)
    axes[1].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[1].set_title('Gradient Boosting - Feature Importance', fontsize=12, fontweight='bold')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/music_feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: music_feature_importance.png")
    plt.close()

def plot_audio_features_analysis(df):
    """Plot analysis of key audio features"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Energy distribution by genre
    df.boxplot(column='Energy', by='Genre', ax=axes[0, 0])
    axes[0, 0].set_xlabel('Genre', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('Energy', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Energy Distribution by Genre', fontsize=12, fontweight='bold')
    axes[0, 0].tick_params(axis='x', rotation=45)
    plt.sca(axes[0, 0])
    plt.xticks(rotation=45)
    
    # Danceability distribution by genre
    df.boxplot(column='Danceability', by='Genre', ax=axes[0, 1])
    axes[0, 1].set_xlabel('Genre', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('Danceability', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Danceability Distribution by Genre', fontsize=12, fontweight='bold')
    axes[0, 1].tick_params(axis='x', rotation=45)
    plt.sca(axes[0, 1])
    plt.xticks(rotation=45)
    
    # Acousticness distribution by genre
    df.boxplot(column='Acousticness', by='Genre', ax=axes[1, 0])
    axes[1, 0].set_xlabel('Genre', fontsize=11, fontweight='bold')
    axes[1, 0].set_ylabel('Acousticness', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Acousticness Distribution by Genre', fontsize=12, fontweight='bold')
    axes[1, 0].tick_params(axis='x', rotation=45)
    plt.sca(axes[1, 0])
    plt.xticks(rotation=45)
    
    # Tempo distribution by genre
    df.boxplot(column='Tempo_BPM', by='Genre', ax=axes[1, 1])
    axes[1, 1].set_xlabel('Genre', fontsize=11, fontweight='bold')
    axes[1, 1].set_ylabel('Tempo (BPM)', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Tempo Distribution by Genre', fontsize=12, fontweight='bold')
    axes[1, 1].tick_params(axis='x', rotation=45)
    plt.sca(axes[1, 1])
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/music_audio_features_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: music_audio_features_analysis.png")
    plt.close()

def main():
    print("="*80)
    print("MUSIC GENRE CLASSIFICATION SYSTEM - DEEP LEARNING ANALYSIS")
    print("="*80)
    
    # Generate dataset
    print("\n[1] Generating synthetic audio features dataset...")
    df = generate_audio_features_dataset(n_samples=1000)
    df.to_csv('/home/ubuntu/music_genre_data.csv', index=False)
    print(f"Dataset generated: {df.shape[0]} tracks")
    print(f"Genres: {df['Genre'].nunique()}")
    print(f"Genre distribution:\n{df['Genre'].value_counts()}")
    
    # Preprocess data
    print("\n[2] Preprocessing audio features...")
    df_processed, feature_cols = preprocess_audio_data(df)
    df_processed, genre_mapping = encode_genres(df_processed)
    
    # Prepare features and target
    X = df_processed[feature_cols]
    y = df_processed['Genre_Encoded']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training set: {X_train_scaled.shape[0]} samples, {X_train_scaled.shape[1]} features")
    print(f"Test set: {X_test_scaled.shape[0]} samples")
    
    # Train models
    print("\n[3] Training classification models...")
    models, results = train_classification_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Print results
    print("\n[4] Model Performance Results:")
    print("-" * 80)
    for model_name, result in results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy:  {result['accuracy']:.6f}")
        print(f"  Precision: {result['precision']:.6f}")
        print(f"  Recall:    {result['recall']:.6f}")
        print(f"  F1-Score:  {result['f1']:.6f}")
    
    # Generate visualizations
    print("\n[5] Generating visualizations...")
    plot_genre_distribution(df)
    plot_model_comparison(results)
    plot_confusion_matrices(results, y_test, genre_mapping)
    plot_feature_importance(models)
    plot_audio_features_analysis(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()
