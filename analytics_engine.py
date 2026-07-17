
"""
Created on Mon Jul 13 19:03:33 2026

@author: hsc
"""
# -*- coding: utf-8 -*-
"""
Unsupervised Language Analytics Engine
Created on Mon July 13 2026
@author: hsc
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text

# Local preprocessed dataset pointer
script_directory = os.path.dirname(os.path.abspath(__file__))
input_filename = os.path.join(script_directory, "fomc_cleaned_data.json")

with open(input_filename, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Order meetings chronologically
dataset = sorted(dataset, key=lambda x: x['date'])

print("\n==========================================================================")
print(f"🤖 RUNNING VECTOR TIME-SERIES DISPLACEMENT ({len(dataset)} DOCUMENTS)")
print("==========================================================================")

if len(dataset) >= 2:
    all_texts = [doc['cleaned_content'] for doc in dataset]
    
    # 1. Deterministic calendar components to eliminate monthly noise
    calendar_noise = [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 2. Correctly combine standard English words with calendar noise upfront
    custom_stop_words = list(text.ENGLISH_STOP_WORDS.union(calendar_noise))
    
    # token_pattern filters out standalone numbers and odd fragments
    vectorizer = TfidfVectorizer(
        stop_words=custom_stop_words, 
        max_df=0.85,
        token_pattern=r'\b[a-zA-Z]{3,}\b'
    )
    
    # Compute global weights
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    feature_names = np.array(vectorizer.get_feature_names_out())
    
    plot_dates = []
    plot_shifts = []
    
    # Pairwise displacement loops
    for i in range(1, len(dataset)):
        current_meeting = dataset[i]
        previous_meeting = dataset[i-1]
        
        vec_prev = tfidf_matrix[i-1]
        vec_curr = tfidf_matrix[i]
        
        # FIXED: Added [0][0] to extract the raw decimal value out of the array matrix
        similarity_score = cosine_similarity(vec_prev, vec_curr)[0][0]
        true_change_percentage = (1 - similarity_score) * 100
        
        # Isolate indices of highest absolute feature shift
        diff_vector = np.abs(vec_curr.toarray() - vec_prev.toarray()).flatten()
        top_changing_indices = np.argsort(diff_vector)[::-1][:4]
        top_words = feature_names[top_changing_indices]
        
        # Convert date to standard YYYY-MM-DD
        raw_d = current_meeting['date']
        formatted_date = f"{raw_d[:4]}-{raw_d[4:6]}-{raw_d[6:8]}"
        
        plot_dates.append(formatted_date)
        plot_shifts.append(true_change_percentage)
        
        print(f"Meeting {formatted_date} vs Prior | Shift: {true_change_percentage:.2f}% | Top Drivers: {', '.join(top_words)}")

    # Calculate Summary Statistics for Logging
    mean_shift = np.mean(plot_shifts)
    print(f"\n==========================================================================")
    print(f"📊 DATA SUMMARY: Baseline Historical Mean Vocabulary Shift: {mean_shift:.2f}%")
    print("==========================================================================")

    # ==============================================================================
    # PLOTTING THE TIME-SERIES (OPTIMIZED FOR SCANNING)
    # ==============================================================================
    print("\nGenerating time-series plot...")
    plt.figure(figsize=(14, 6))
    
    # Visual line track
    plt.plot(plot_dates, plot_shifts, marker='o', color='#1f77b4', linewidth=2, linestyle='-', label='Vocabulary Shift %')
    plt.axhline(mean_shift, color='red', linestyle='--', alpha=0.7, label=f'Historical Baseline Mean ({mean_shift:.2f}%)')
    
    plt.title('FOMC Policy Vocabulary Displacement Over Time', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Meeting Date', fontsize=11, labelpad=10)
    plt.ylabel('True Vocabulary Profile Shift (%)', fontsize=12, labelpad=10)
    
    # FIX: Only display every 4th date string on the X-axis so labels remain legible
    visible_ticks = range(0, len(plot_dates), 4)
    plt.xticks(visible_ticks, [plot_dates[i] for i in visible_ticks], rotation=45, ha='right', fontsize=9)
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.tight_layout()
    
    plt.show()

else:
    print("Need at least 2 documents to compare.")
