# -*- coding: utf-8 -*-
"""
Private Dev Lab: Incremental Ingestion Data Pipeline with Automated Logging
Created: 2026-07-26 | Author: hsc
"""
import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import time
from datetime import datetime, timezone

def run_incremental_pipeline():
    calendar_url = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
    base_url = "https://www.federalreserve.gov"

    # 1. Resolves to the 'src' subfolder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Steps one level up to the 'production_github_repo' root directory
    repository_root = os.path.dirname(script_dir)
    
    # 3. Targets the new professional folder structures precisely
    output_filename = os.path.join(repository_root, "data", "fomc_cleaned_data.json")
    audit_filename = os.path.join(repository_root, "data", "pipeline_audit_log.json")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Track metrics for logging
    start_time = time.time()
    payload_changes = []
    status = "SUCCESS"
    log_message = "System Synced: No new monetary policy minutes detected online."
    
    # 1. Read and Parse the Envelope Structured Ledger
    if os.path.exists(output_filename):
        with open(output_filename, 'r', encoding='utf-8') as f:
            try:
                ledger_envelope = json.load(f)
                if isinstance(ledger_envelope, list):
                    ledger_envelope = {"documents": ledger_envelope, "fomc_schedule_upcoming": []}
            except json.JSONDecodeError:
                ledger_envelope = {"documents": [], "fomc_schedule_upcoming": []}
    else:
        ledger_envelope = {"documents": [], "fomc_schedule_upcoming": []}
        
    cleaned_dataset = ledger_envelope.get("documents", [])
    existing_dates = {doc['date'] for doc in cleaned_dataset}
    
    print("Connecting to central FOMC Calendar page...")
    try:
        response = requests.get(calendar_url, headers=headers, timeout=10)
        if response.status_code != 200:
            status = "FAILED"
            log_message = f"Failed to fetch calendar. Status: {response.status_code}"
            write_audit_log(audit_filename, status, start_time, log_message, [])
            print(log_message)
            return
    except Exception as e:
        status = "FAILED"
        log_message = f"Connection error: {e}"
        write_audit_log(audit_filename, status, start_time, log_message, [])
        print(log_message)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # --- TASK 1: EXTRACT UPCOMING CALENDAR MEETINGS DYNAMICALLY ---
    upcoming_dates = []
    current_year = datetime.now(timezone.utc).year
    

    for panel in soup.find_all('div', class_=lambda x: x and 'panel' in x):
        year_header = panel.find('h4')
        if year_header and str(current_year) in year_header.get_text():
            for row in panel.find_all('div', class_='fomc-meeting'):
                month_div = row.find('div', class_='fomc-meeting__month')
                date_div = row.find('div', class_='fomc-meeting__date')
                
                if month_div and date_div:
                    month_text = month_div.get_text(strip=True)
                    day_text = date_div.get_text(strip=True).split('-')[-1].strip()
                    day_cleaned = ''.join(c for c in day_text if c.isdigit())
                    
                    try:
                        date_obj = datetime.strptime(f"{current_year} {month_text} {day_cleaned}", "%Y %B %d")
                        upcoming_dates.append(date_obj.strftime("%Y%m%d"))
                    except ValueError:
                        continue
                        
    if upcoming_dates:
        ledger_envelope["fomc_schedule_upcoming"] = sorted(list(set(upcoming_dates)))

    # --- TASK 2: SEQUENTIAL HISTORIC MINUTES PROCESSING ---
    html_minutes_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'fomcminutes' in href.lower() and '.pdf' not in href.lower():
            absolute_url = urllib.parse.urljoin(base_url, href)
            date_string = absolute_url.split('fomcminutes')[-1].replace('.htm', '')
            
            if len(date_string) == 8 and date_string not in existing_dates and (date_string, absolute_url) not in html_minutes_links:
                html_minutes_links.append((date_string, absolute_url))
                
    if not html_minutes_links:
        print(f"✅ {log_message}")
    else:
        log_message = f"Found {len(html_minutes_links)} new document(s) to process."
        print(log_message)
        for date_str, target_url in html_minutes_links:
            print(f" -> Processing incremental node: {date_str}")
            time.sleep(1)
            
            try:
                m_res = requests.get(target_url, headers=headers, timeout=10)
                if m_res.status_code == 200:
                    m_soup = BeautifulSoup(m_res.text, 'html.parser')
                    container = m_soup.find('div', id='leftText') or m_soup.find('div', id='article')
                    
                    if container:
                        raw_text = container.get_text(separator=' ', strip=True).lower()
                        clean_text = " ".join(raw_text.split())
                        
                        cleaned_dataset.append({
                            'date': date_str,
                            'url': target_url,
                            'text_length': len(clean_text),
                            'cleaned_content': clean_text
                        })
                        payload_changes.append(date_str)
                        print(f"    Success: Appended node {date_str} smoothly.")
            except Exception as e:
                status = "WARNING"
                log_message = f"Partial failure. Error reading node {date_str}: {e}"
                print(f"    {log_message}")
                
    # Update ledger and save
    ledger_envelope["documents"] = cleaned_dataset
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(ledger_envelope, f, ensure_ascii=False, indent=4)
        
    # Append the operational metadata trace to the audit log
    write_audit_log(audit_filename, status, start_time, log_message, payload_changes)
    print("🚀 Database Ledger verification completed successfully.")

def write_audit_log(filepath, status, start_time, message, changes):
    """
    Appends a structured execution logging node to the audit trail file.
    """
    log_entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "execution_duration_sec": round(time.time() - start_time, 3),
        "status": status,
        "message": message,
        "payload_changes_appended": changes
    }
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []
        
    logs.append(log_entry)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4)

# THIS IS THE BLOCK THAT EXECUTED THE ENGINE SCRIPT
if __name__ == "__main__":
    run_incremental_pipeline()
