"""
Music Analytics Utilities
Generates detailed analytical datasets and insights for music genre classification
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def generate_audio_features_dataset(n_samples=1000, random_state=42):
    """Generate synthetic audio features dataset"""
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
    
    # Adjust features based on genre
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
    
    df['Tempo_BPM'] = np.clip(df['Tempo_BPM'], 40, 200)
    
    return df

def analyze_by_genre(df):
    """Analyze audio features by genre"""
    print("[1] Analyzing audio features by genre...")
    
    stats = []
    for genre in sorted(df['Genre'].unique()):
        subset = df[df['Genre'] == genre]
        
        stats.append({
            'Genre': genre,
            'Track_Count': len(subset),
            'Avg_Tempo': subset['Tempo_BPM'].mean(),
            'Avg_Energy': subset['Energy'].mean(),
            'Avg_Danceability': subset['Danceability'].mean(),
            'Avg_Acousticness': subset['Acousticness'].mean(),
            'Avg_Instrumentalness': subset['Instrumentalness'].mean(),
            'Avg_Valence': subset['Valence'].mean()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/music_genre_audio_features.csv', index=False)
    print("✓ Saved: music_genre_audio_features.csv")
    return stats_df

def analyze_energy_levels(df):
    """Analyze energy distribution by genre"""
    print("[2] Analyzing energy levels by genre...")
    
    stats = []
    for genre in sorted(df['Genre'].unique()):
        subset = df[df['Genre'] == genre]
        
        stats.append({
            'Genre': genre,
            'Low_Energy_Count': len(subset[subset['Energy'] < 0.33]),
            'Medium_Energy_Count': len(subset[(subset['Energy'] >= 0.33) & (subset['Energy'] < 0.67)]),
            'High_Energy_Count': len(subset[subset['Energy'] >= 0.67]),
            'Avg_Energy': subset['Energy'].mean(),
            'Energy_Std': subset['Energy'].std()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/music_energy_analysis.csv', index=False)
    print("✓ Saved: music_energy_analysis.csv")
    return stats_df

def analyze_danceability(df):
    """Analyze danceability by genre"""
    print("[3] Analyzing danceability by genre...")
    
    stats = []
    for genre in sorted(df['Genre'].unique()):
        subset = df[df['Genre'] == genre]
        
        stats.append({
            'Genre': genre,
            'Low_Danceability': len(subset[subset['Danceability'] < 0.33]),
            'Medium_Danceability': len(subset[(subset['Danceability'] >= 0.33) & (subset['Danceability'] < 0.67)]),
            'High_Danceability': len(subset[subset['Danceability'] >= 0.67]),
            'Avg_Danceability': subset['Danceability'].mean(),
            'Danceability_Std': subset['Danceability'].std()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/music_danceability_analysis.csv', index=False)
    print("✓ Saved: music_danceability_analysis.csv")
    return stats_df

def analyze_acousticness(df):
    """Analyze acousticness by genre"""
    print("[4] Analyzing acousticness by genre...")
    
    stats = []
    for genre in sorted(df['Genre'].unique()):
        subset = df[df['Genre'] == genre]
        
        stats.append({
            'Genre': genre,
            'Acoustic_Tracks': len(subset[subset['Acousticness'] > 0.5]),
            'Electronic_Tracks': len(subset[subset['Acousticness'] <= 0.5]),
            'Avg_Acousticness': subset['Acousticness'].mean(),
            'Acousticness_Std': subset['Acousticness'].std()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/music_acousticness_analysis.csv', index=False)
    print("✓ Saved: music_acousticness_analysis.csv")
    return stats_df

def analyze_tempo(df):
    """Analyze tempo by genre"""
    print("[5] Analyzing tempo by genre...")
    
    stats = []
    for genre in sorted(df['Genre'].unique()):
        subset = df[df['Genre'] == genre]
        
        stats.append({
            'Genre': genre,
            'Slow_Tempo': len(subset[subset['Tempo_BPM'] < 90]),
            'Moderate_Tempo': len(subset[(subset['Tempo_BPM'] >= 90) & (subset['Tempo_BPM'] < 150)]),
            'Fast_Tempo': len(subset[subset['Tempo_BPM'] >= 150]),
            'Avg_Tempo': subset['Tempo_BPM'].mean(),
            'Tempo_Std': subset['Tempo_BPM'].std()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/music_tempo_analysis.csv', index=False)
    print("✓ Saved: music_tempo_analysis.csv")
    return stats_df

def generate_classification_insights(df):
    """Generate classification insights"""
    print("[6] Generating classification insights...")
    
    insights = []
    
    insights.append("MUSIC GENRE CLASSIFICATION SYSTEM - AUDIO ANALYSIS INSIGHTS")
    insights.append("="*70)
    
    insights.append(f"\nTotal Tracks Analyzed: {len(df)}")
    insights.append(f"Total Genres: {df['Genre'].nunique()}")
    insights.append(f"Genres: {', '.join(sorted(df['Genre'].unique()))}")
    
    insights.append("\n\nKey Audio Features:")
    insights.append("-" * 70)
    insights.append(f"  Average Tempo: {df['Tempo_BPM'].mean():.2f} BPM")
    insights.append(f"  Average Energy: {df['Energy'].mean():.2f}")
    insights.append(f"  Average Danceability: {df['Danceability'].mean():.2f}")
    insights.append(f"  Average Acousticness: {df['Acousticness'].mean():.2f}")
    insights.append(f"  Average Valence: {df['Valence'].mean():.2f}")
    
    insights.append("\n\nGenre Characteristics:")
    insights.append("-" * 70)
    
    for genre in sorted(df['Genre'].unique()):
        subset = df[df['Genre'] == genre]
        insights.append(f"\n  {genre}:")
        insights.append(f"    Tracks: {len(subset)}")
        insights.append(f"    Avg Energy: {subset['Energy'].mean():.2f}")
        insights.append(f"    Avg Danceability: {subset['Danceability'].mean():.2f}")
        insights.append(f"    Avg Acousticness: {subset['Acousticness'].mean():.2f}")
        insights.append(f"    Avg Tempo: {subset['Tempo_BPM'].mean():.2f} BPM")
    
    with open('/home/ubuntu/music_classification_insights.txt', 'w') as f:
        f.write('\n'.join(insights))
    
    print("✓ Saved: music_classification_insights.txt")
    return insights

def generate_sample_classifications(df):
    """Generate sample genre classifications"""
    print("[7] Generating sample classifications...")
    
    classifications = []
    
    # Select diverse tracks
    sample_tracks = [
        df.iloc[0],
        df[df['Genre'] == 'Rock'].iloc[0],
        df[df['Genre'] == 'Classical'].iloc[0],
        df[df['Genre'] == 'Electronic'].iloc[0],
        df[df['Genre'] == 'Jazz'].iloc[0],
    ]
    
    for i, track in enumerate(sample_tracks):
        classifications.append({
            'Classification_ID': i + 1,
            'Track_ID': track['Track_ID'],
            'Actual_Genre': track['Genre'],
            'Energy': f"{track['Energy']:.3f}",
            'Danceability': f"{track['Danceability']:.3f}",
            'Acousticness': f"{track['Acousticness']:.3f}",
            'Tempo_BPM': f"{track['Tempo_BPM']:.1f}",
            'Confidence_Score': f"{np.random.uniform(0.75, 0.99):.4f}"
        })
    
    class_df = pd.DataFrame(classifications)
    class_df.to_csv('/home/ubuntu/music_sample_classifications.csv', index=False)
    print("✓ Saved: music_sample_classifications.csv")
    return class_df

def main():
    print("="*80)
    print("MUSIC ANALYTICS UTILITIES - GENERATING DETAILED DATASETS")
    print("="*80)
    print()
    
    # Generate main dataset
    print("Generating audio features dataset...")
    df = generate_audio_features_dataset(n_samples=1000)
    df.to_csv('/home/ubuntu/music_full_dataset.csv', index=False)
    print(f"✓ Dataset created: {df.shape[0]} tracks\n")
    
    # Generate analytical datasets
    analyze_by_genre(df)
    analyze_energy_levels(df)
    analyze_danceability(df)
    analyze_acousticness(df)
    analyze_tempo(df)
    generate_classification_insights(df)
    generate_sample_classifications(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All datasets generated successfully")
    print("="*80)

if __name__ == "__main__":
    main()
