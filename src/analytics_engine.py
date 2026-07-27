# -*- coding: utf-8 -*-
"""
Private Dev Lab Workbench: Mathematical Core Engine
Created: 2026-07-26 | Author: hsc
"""
import os
import json
import numpy as np
from datetime import date, timedelta, datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text

def load_local_envelope():
    """
    Safely accesses and parses the JSON ledger workspace envelope.
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    input_filename = os.path.join(script_directory, "fomc_cleaned_data.json")
    
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
    Computes countdown metrics dynamically using dates scraped directly 
    by the ingestion pipeline, removing hardcoded schedules.
    """
    envelope = load_local_envelope()
    upcoming_schedule = envelope.get("fomc_schedule_upcoming", [])
    
    today = date.today()
    
    # Fallback default constants in case the scraper has not populated the JSON ledger yet
    target_release_str = "Aug 19, 2026"
    days_remaining = 25
    
    if not upcoming_schedule:
        return target_release_str, days_remaining
        
    for date_str in upcoming_schedule:
        try:
            meeting_date = datetime.strptime(date_str, "%Y%m%d").date()
            if meeting_date >= today:
                # The Fed releases historical text minutes exactly 21 days (3 weeks) post-meeting
                release_date = meeting_date + timedelta(days=21)
                days_remaining = (release_date - today).days
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
