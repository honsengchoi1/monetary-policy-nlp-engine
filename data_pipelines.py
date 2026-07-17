# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 19:00:45 2026

@author: hsc
"""

# -*- coding: utf-8 -*-
"""
FOMC Minutes Data Pipeline
Created on Sun July 12 2026
@author: hsc
"""

import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import json

calendar_url = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
base_url = "https://www.federalreserve.gov"
script_directory = os.path.dirname(os.path.abspath(__file__))
output_filename = os.path.join(script_directory, "fomc_cleaned_data.json")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

print("Step 1: Connecting to the central FOMC Calendar page...")
response = requests.get(calendar_url, headers=headers)

if response.status_code == 200:
    print("Successfully connected!")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    html_minutes_links = []
    all_links = soup.find_all('a', href=True)
    
    for link in all_links:
        href = link['href']
        if 'fomcminutes' in href.lower() and '.pdf' not in href.lower():
            absolute_url = urllib.parse.urljoin(base_url, href)
            if absolute_url not in html_minutes_links:
                html_minutes_links.append(absolute_url)
                
    print(f"\n🎯 SUCCESS! Filtered down to {len(html_minutes_links)} pure HTML minutes links.")
    
    cleaned_dataset = []
    
    if html_minutes_links:
        print(f"\nStep 2: Starting bulk download and text preprocessing for all {len(html_minutes_links)} links...")
        
        for index, test_url in enumerate(html_minutes_links, start=1):
            print(f" -> Downloading [{index}/{len(html_minutes_links)}]: {test_url}")
            
            time.sleep(1) 
            
            minutes_response = requests.get(test_url, headers=headers)
            if minutes_response.status_code == 200:
                minutes_soup = BeautifulSoup(minutes_response.text, 'html.parser')
                text_container = minutes_soup.find('div', id='leftText') or minutes_soup.find('div', id='article')
                
                if text_container:
                    full_text = text_container.get_text(separator=' ', strip=True)
                    clean_text = full_text.lower()
                    clean_text = " ".join(clean_text.split())
                    date_string = test_url.split('fomcminutes')[-1].replace('.htm', '')
                    
                    cleaned_dataset.append({
                        'date': date_string,
                        'url': test_url,
                        'text_length': len(clean_text),
                        'cleaned_content': clean_text
                    })
                else:
                    print(f"   Could not locate text container for {test_url}")
            else:
                print(f"   Failed to download {test_url}. Status: {minutes_response.status_code}")
                
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(cleaned_dataset, f, ensure_ascii=False, indent=4)
            
    print("\n==========================================================================")
    clean_display_name = os.path.basename(output_filename)
    print(f"🚀 SUCCESS: Preprocessed data saved locally to relative path: './{clean_display_name}'")
    print(f"Total structured documents downloaded and stored: {len(cleaned_dataset)}")
    print("==========================================================================")

else:
    print(f"Failed to fetch calendar page. Status code: {response.status_code}")
