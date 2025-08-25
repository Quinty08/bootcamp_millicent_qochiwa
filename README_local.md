# Corporate Loan Credit Scoring — Project (Stage 02)

**Purpose:** Build a reproducible project scaffold for evaluating credit risk of corporate loan applicants. This repository contains a controlled environment, configuration, and folder structure to support future data ingestion, preprocessing, modeling, and reporting efforts.

**Structure**
- `/data/` — raw and processed data (gitignored; contains .gitkeep)
- `/data/raw/` — raw source files (gitignored; contains .gitkeep)
- `/notebooks/` — exploratory and narrative Jupyter notebooks
- `/src/` — reusable Python modules (config, utils)
- `/docs/` — project documentation, stakeholder memos
- `requirements.txt` or `environment.yml` — project dependencies
- `.env.example` — template for local configuration (do not commit secrets)

**Quick start**
1. Create environment: `conda create -n fe-course python=3.11 -y && conda activate fe-course`
2. Install deps: `pip install -r requirements.txt` (or `pip install python-dotenv numpy jupyter` if requirements.txt not present)
3. Copy `.env.example` → `.env` and fill local values.
4. Open notebooks: `jupyter lab`
