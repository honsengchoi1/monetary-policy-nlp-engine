# 📑 Unsupervised Language Analytics Engine for Macroeconomic Regime Tracking

An enterprise-ready, automated NLP data engineering and matrix analysis pipeline that monitors structural narrative changes across sequential Federal Reserve FOMC policy minutes.


| 🤖 GITHUB ACTIONS <br> *(The Background Engine)* | 💻 GITHUB REPOSITORY <br> *(The Central Cloud Storage)* |
| :--- | :--- |
| • Runs your scheduling file (`.yml` script). <br>• Wakes up automatically on Fed release days. <br>• Downloads the new text. | • Stores your code. <br>• Holds the master database file (`fomc_cleaned_data.json`). <br>• Updates the database directly in the cloud when a new minute drops. |

$$\Downarrow \text{ Pushes Data Updates} \qquad\qquad\qquad\qquad \Uparrow \text{ Pulls Latest Data}$$

| 📊 STREAMLIT COMMUNITY CLOUD <br> *(Where Your Dashboard Resides Live on the Web)* |
| :--- |
| • Pulls data directly from your GitHub repository. <br>• Auto-refreshes to instantly display new math analytics to recruiters. |

## 🏗️ Enterprise Architecture & Implementation Specifications

### 1. Incremental Ingestion Layer (`src/data_pipeline.py`)
*   **Persistent Cloud JSON Database Envelope:** Solves the ephemeral file system challenge of serverless cloud runtimes by treating the repository data ledger (`data/fomc_cleaned_data.json`) as an active, append-only dictionary state object.
*   **Dynamic Future Calendar Extraction:** Automatically scrapes upcoming calendar tables from the Federal Reserve Board site, programmatically parsing month blocks and range limits into uniform 8-character string indexes (`YYYYMMDD`).
*   **Timezone-Aware UTC Diagnostic Auditing:** Implements localized defensive logging routines to track execution times, transaction payloads, and system status markers committed to `data/pipeline_audit_log.json`.

### 2. Mathematical Controller Core Engine (`src/analytics_engine.py`)
*   **NLP Feature Vectorization:** Converts raw text strings into normalized mathematical dimensions using `TfidfVectorizer` parameter variables (`max_df`, customized calendar stop-word arrays, and dynamic runtime-compiled character length regular expressions).
*   **Policy Displacement Geometry:** Computes semantic distance metrics by programmatically unwrapping Scikit-Learn's nested 2D arrays down to standalone scalar floating-point values via `cosine_similarity()[0][0]` matrix coordinates.
*   **Automated Regime Anomaly Tracking:** Evaluates true vocabulary profile drift percentages ($(1 - \text{Cosine Similarity}) \times 100$) against an explicit, mathematically locked historical mean baseline ceiling of **52.10%** to flag macro regime disruptions.

### 3. Front-End User Presentation Layer (`src/dashboard.py`)
*   **Hyperparameter Slider Tuning:** Exposes internal algorithmic core variables directly to external modules, giving analysts real-time control over token patterns and threshold limits.
*   **Decoupled Interface Signature:** Safely reads calculated time-series data and countdown remaining parameters from the analytical core controller completely independent of raw data ingestion processes.

---

### 🧪 Automated Health Integration & Assertion Testing (`tests/test_suite.py`)
To prevent software regressions or boundary leaks before cloud deployment pushes, the custom test harness runs programmatically inside execution loops:
*   **Schema Validation:** Validates that the top JSON container layer matches dictionary constraints and target field string properties perfectly.
*   **Mathematical Boundary Constraints:** Enforces strict physical math parameters, ensuring vector drift scales evaluate strictly inside physical bounds ($0.0\% \le \text{Shift Value} \le 100.0\%$), triggering `exit(1)` code exceptions on any breach.

---

### 🚀 Continuous Cloud Deployment Workflow Roadmap

*   **Background Cron Scheduling Automation:** Triggers container spin-ups automatically via GitHub Actions workflows (`.github/workflows/pipeline_cron.yml`) synchronized to post-meeting release windows.
*   **Secure Environment Infrastructure:** Utilizes private runtime secrets management inside GitHub repository values to securely map pipeline email targets and alert tokens while keeping code vectors completely pristine.

---

### 📈 Future Engineering Expansion Backlog
*   **Topic Modeling Expansion:** Integrate Latent Dirichlet Allocation (LDA) or BERTopic layers to isolate specific structural macro themes.
*   **Market Data Overlays:** Map rolling historical correlations against secondary financial indicators (2-Year Treasury Yields, S&P 500 benchmarks, DXY indices).


