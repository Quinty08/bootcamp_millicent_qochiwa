\## Data Storage



\*\*Folder structure\*\*

\- `data/raw/` — immutable original inputs (CSV). Do not edit in place. New versions should be added with timestamped filenames.

\- `data/processed/` — cleaned / analysis-ready outputs (Parquet). These are reproducible from code.



\*\*Formats used and why\*\*

\- For exchange and tiny files (human edits, quick inspection): \*\*CSV\*\* (human-readable, easy diffs).

\- For analysis-ready storage and repeated reads: \*\*Parquet\*\* (columnar, compressed, preserves types, fast reads).

\- Rule: CSV in `data/raw/`, Parquet in `data/processed/`.



\*\*Environment-driven paths\*\*

\- Paths are defined in `.env` at repository root:



DATA\_DIR\_RAW=data/raw

DATA\_DIR\_PROCESSED=data/processed





\- Code uses `python-dotenv` + `pathlib` to resolve directories so the code works across machines:

```python

from dotenv import load\_dotenv

import os, pathlib



load\_dotenv()

RAW = pathlib.Path(os.getenv('DATA\_DIR\_RAW', 'data/raw'))

PROC = pathlib.Path(os.getenv('DATA\_DIR\_PROCESSED', 'data/processed'))



