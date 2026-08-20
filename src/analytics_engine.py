# -*- coding: utf-8 -*-
"""
Private Dev Lab Workbench: Mathematical Core Engine
Created: 2026-07-26 | Author: hsc
"""
import os
import json
import numpy as np
from datetime import datetime, timezone, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text

def load_local_envelope():
    """
    Safely accesses and parses the JSON ledger workspace envelope from the /data folder.
    """
    # 1. Finds the directory of this script (resolves to production_github_repo\src)
    script_directory = os.path.dirname(os.path.abspath(__file__)) 
    
    # 2. Moves up one level to the root directory (resolves to production_github_repo)
    repository_root = os.path.dirname(script_directory) 
    
    # 3. Joins the root path with the new folder and file name
    input_filename = os.path.join(repository_root, "data", "fomc_cleaned_data.json")
    
    if not os.path.exists(input_filename):
        return {"documents": [], "fomc_schedule_upcoming": []}
        
    with open(input_filename, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return {"documents": data, "fomc_schedule_upcoming": []}
            return data
        except json.JSONDecodeError:
            return {"documents": [], "fomc_schedule_upcoming": []}


def get_countdown_metrics():
    """
    Computes countdown metrics dynamically against the verified JSON database schedule.
    Automatically scales fallback logic forward to eliminate hardcoded expiration dates.
    """
    envelope = load_local_envelope()
    upcoming_schedule = envelope.get("fomc_schedule_upcoming", [])
    
    # --- ENTERPRISE PATCH: ENFORCE STRICT EASTERN TIME (ET) ---
    # Shift UTC time backwards by 4 hours to simulate US Eastern Time.
    # This prevents the UI countdown from rolling over to "0 days" at 8:00 PM ET.
    now_utc = datetime.now(timezone.utc)
    now_et = now_utc - timedelta(hours=4) 
    today_active_date = now_et.date()
    
    # 2. EXPIRATION-PROOF FALLBACK: Calculate a target exactly 3 weeks from today
    dynamic_fallback_date = today_active_date + timedelta(days=21)
    days_remaining = 21
    target_release_str = dynamic_fallback_date.strftime("%b %d, %Y")
    
    if not upcoming_schedule:
        return target_release_str, days_remaining
        
    for date_str in upcoming_schedule:
        try:
            meeting_date = datetime.strptime(date_str, "%Y%m%d").date()
            release_date = meeting_date + timedelta(days=21)
            
            # 3. Check if the release date is today or in the future
            if release_date >= today_active_date:
                days_remaining = (release_date - today_active_date).days
                target_release_str = release_date.strftime("%b %d, %Y")
                break
                
        except ValueError:
            continue
            
    return target_release_str, days_remaining


def run_vocabulary_analysis(max_df_param=0.85, word_length=3, threshold_param=52.10):
    envelope = load_local_envelope()
    dataset = envelope.get("documents", [])
    
    if not dataset or len(dataset) < 2:
        return None
        
    dataset = sorted(dataset, key=lambda x: x['date'])

    all_texts = [doc['cleaned_content'] for doc in dataset]
    calendar_noise = ['january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    custom_stop_words = list(text.ENGLISH_STOP_WORDS.union(calendar_noise))
    
    token_regex = f'\\b[a-zA-Z]{{{word_length},}}\\b'
    vectorizer = TfidfVectorizer(stop_words=custom_stop_words, max_df=max_df_param, token_pattern=token_regex)
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    feature_names = np.array(vectorizer.get_feature_names_out())
    
    plot_dates, plot_shifts, top_words_history = [], [], []
    for i in range(1, len(dataset)):
        vec_prev = tfidf_matrix[i-1]
        vec_curr = tfidf_matrix[i]
        
        similarity_score = cosine_similarity(vec_prev, vec_curr)[0][0]
        true_change_percentage = (1 - similarity_score) * 100
        
        diff_vector = np.abs(vec_curr.toarray() - vec_prev.toarray()).flatten()
        top_changing_indices = np.argsort(diff_vector)[::-1][:4]
        top_words = feature_names[top_changing_indices].tolist()
        
        raw_d = dataset[i]['date']
        formatted_date = f"{raw_d[:4]}-{raw_d[4:6]}-{raw_d[6:8]}"
        
        plot_dates.append(formatted_date)
        plot_shifts.append(true_change_percentage)
        top_words_history.append(top_words)

    latest_shift = plot_shifts[-1]
    latest_date = plot_dates[-1]
    latest_keywords = top_words_history[-1]
    is_anomaly = latest_shift > threshold_param
    
    return {
        "dates": plot_dates,
        "shifts": plot_shifts,
        "historical_mean": np.mean(plot_shifts),
        "latest_date": latest_date,
        "latest_shift": latest_shift,
        "latest_keywords": latest_keywords,
        "is_anomaly": is_anomaly,
        "top_words_history": top_words_history
    }
