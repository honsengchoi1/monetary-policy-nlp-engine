# -*- coding: utf-8 -*-
"""
Task 3: Automated Quality & Health Integration Test Check Script
Created: 2026-07-26 | Author: hsc
"""
from src.analytics_engine import load_local_envelope, run_vocabulary_analysis

def test_data_schema_completeness():
    print(" -> Checking structural data envelope rules...")
    envelope = load_local_envelope()
    
    assert isinstance(envelope, dict), "CRITICAL: Ledger top envelope must be a JSON dictionary object."
    assert "documents" in envelope, "CRITICAL: Ledger missing 'documents' target array."
    assert "fomc_schedule_upcoming" in envelope, "CRITICAL: Ledger missing dynamic schedule array."
    
    docs = envelope.get("documents", [])
    if docs:
        for idx, doc in enumerate(docs):
            assert "date" in doc, f"CRITICAL: Document index {idx} missing identification index date."
            assert "cleaned_content" in doc, f"CRITICAL: Document index {idx} missing text content."
            assert isinstance(doc["text_length"], int), f"CRITICAL: Document index {idx} text_length must be an integer."
            assert doc["text_length"] > 0, f"CRITICAL: Document index {idx} text length cannot be empty."

def test_mathematical_range_boundaries():
    print(" -> Checking mathematical core processing boundaries...")
    payload = run_vocabulary_analysis()
    
    if payload is not None:
        shifts = payload.get("shifts", [])
        for val in shifts:
            assert 0.0 <= val <= 100.0, f"CRITICAL: Mathematical anomaly detected. Vector drift percentage {val}% is out of boundary constraints."
        
        mean_val = payload.get("historical_mean", 0)
        assert 0.0 <= mean_val <= 100.0, f"CRITICAL: Historical mean {mean_val}% out of math bounds."

if __name__ == "__main__":
    print("==================================================")
    print("RUNNING AUTOMATED HEALTH INTEGRATION TEST SUITE...")
    print("==================================================")
    try:
        test_data_schema_completeness()
        test_mathematical_range_boundaries()
        print("\n✅ SUCCESS: All automated integration checks passed cleanly. Code frozen.")
    except AssertionError as error:
        print(f"\n❌ INTEGRATION FAILURE COMPILATION ERROR: {error}")
        exit(1)
    print("==================================================")
