# Unsupervised Macro Regime Tracker (FOMC Minutes Analytics)

This quantitative analytics framework tracks and monitors structural narrative changes across sequential Federal Reserve FOMC policy minutes. Designed for institutional macro analysts, quantitative researchers, multi-asset portfolio managers, and traders, the engine filters out routine administrative language to isolate unexpected deviations in central bank forward guidance.

[📁 View Full Analytical Whitepaper (PDF)](https://github.com)

## 📊 Empirical Framework & Statistical Baseline
*   **The Benchmark Baseline**: By analyzing historical minutes, the model establishes that the Federal Reserve naturally modifies approximately **52.10%** of its text from meeting to meeting to account for standard data updates.
*   **The Macro Signal**: When the text modification index spikes significantly above this 52.10% average, it mathematically signals that an external economic, financial, or geopolitical shock has forced the committee to structurally alter its forward guidance narrative.

### Unsupervised Macro Turning Points Isolated by the Engine:
*   **March 2022 (80.34% Shift)** ── *Key Word Drivers*: `invasion`, `ukraine`, `russian`. (Captures the outbreak of geopolitical conflict disrupting global macro projections).
*   **March 2023 (73.02% Shift)** ── *Key Word Drivers*: `banking`, `signature`, `closures`, `valley`. (Captures the regional banking liquidity crisis and the immediate shift to banking system stabilization).
*   **March 2026 (67.18% Shift)** ── *Key Word Drivers*: `east`, `conflict`, `middle`, `oil`. (Captures rapid escalation of energy market supply-chain risk vectors).

---

## 🏗️ Core Architecture Components

1.  **Automated Ingestion Layer (`src/data_pipeline.py`)**: Programmatically extracts the latest calendar transcripts directly from the Federal Reserve Board monetary archive and commits state changes cleanly to an audit-ready historic ledger.
2.  **Linguistic Vectorization Engine (`src/analytics_engine.py`)**: Transforms raw text strings into high-dimensional numerical vectors, mapping the geometric distance between consecutive meetings while filtering out repetitive, administrative boilerplate language.
3.  **Presentation Dashboard (`src/dashboard.py`)**: An interactive dashboard environment allowing macro analysts to visually audit shift anomalies and isolate underlying vocabulary keywords across target periods.

---

## 🎯 Next-Stage Research & Expansion Backlog

*   **Localized Policy Sentiment Classifier (Hawk / Dove / Neutral)**: Actively evaluating a specialized monetary domain framework to map whether structural text shifts represent a Hawkish (tightening), Dovish (easing), or Neutral (steady) stance. To mitigate subjective human bias, the current blueprint under consideration utilizes a hybrid data-driven methodology—combining academic anchor lexicons with the core engine's unsupervised statistical word-importance extractions to ensure model objectivity.
