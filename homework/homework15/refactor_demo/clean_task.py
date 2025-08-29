
import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
import pandas as pd

def retry(n_tries=3, delay=0.5, backoff=2.0):
    def decorator(fn):
        def wrapped(*args, **kwargs):
            _delay = delay
            last_exc = None
            for i in range(1, n_tries+1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logging.warning("Attempt %d/%d failed: %s", i, n_tries, str(e))
                    if i == n_tries:
                        logging.error("All retries failed.")
                        raise
                    time.sleep(_delay)
                    _delay *= backoff
            raise last_exc
        return wrapped
    return decorator

@retry(n_tries=3, delay=0.5, backoff=2.0)
def clean_task(input_path: str, output_path: str) -> None:
    """Read CSV/Excel/JSON (if available), drop NA for main feature, write cleaned CSV and a summary JSON."""
    logging.info("[clean_task] start: input=%s output=%s", input_path, output_path)
    p_in = Path(input_path)
    if not p_in.exists():
        logging.info("[clean_task] input not found; creating a simulated dataset")
        df = pd.DataFrame({'x_feature': [0.1, 1.2, 2.5, None, 3.3], 'y_target': [1,2,3,4,5]})
    else:
        # infer file type
        if p_in.suffix.lower() in ['.csv']:
            df = pd.read_csv(p_in)
        elif p_in.suffix.lower() in ['.xlsx', '.xls']:
            df = pd.read_excel(p_in)
        elif p_in.suffix.lower() in ['.json']:
            df = pd.read_json(p_in)
        else:
            raise ValueError("Unsupported input extension: " + p_in.suffix)

    rows_before = len(df)
    # Simple cleaning: drop rows where x_feature is NaN
    if 'x_feature' in df.columns:
        df_clean = df.dropna(subset=['x_feature']).copy()
    else:
        # if column missing, attempt to coerce first numeric column
        numcols = df.select_dtypes(include='number').columns.tolist()
        if not numcols:
            raise ValueError("No numeric columns found to use as x_feature")
        df_clean = df.dropna(subset=[numcols[0]])
        df_clean = df_clean.rename(columns={numcols[0]: 'x_feature'})

    rows_after = len(df_clean)

    # Ensure output dir exists
    p_out = Path(output_path)
    p_out.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned data (CSV)
    if p_out.suffix.lower() == '.csv':
        df_clean.to_csv(p_out, index=False)
    elif p_out.suffix.lower() in ['.json']:
        p_out.write_text(df_clean.to_json(orient='records'))
    else:
        # default to csv if unknown extension
        df_clean.to_csv(p_out.with_suffix('.csv'), index=False)
        p_out = p_out.with_suffix('.csv')

    
    summary = {
        'task': 'clean_task',
        'run_at': datetime.utcnow().isoformat(),
        'input_path': str(p_in),
        'output_path': str(p_out),
        'rows_before': int(rows_before),
        'rows_after': int(rows_after)
    }
    summary_path = p_out.with_suffix('.summary.json')
    summary_path.write_text(json.dumps(summary, indent=2))

    logging.info("[clean_task] done: wrote %s (rows %d -> %d)", p_out, rows_before, rows_after)

def main(argv=None):
    parser = argparse.ArgumentParser(description='Simple clean task CLI')
    parser.add_argument('--input', required=False, help='Input path (CSV/Excel/JSON). If absent, a demo dataset is used.')
    parser.add_argument('--output', required=True, help='Output cleaned CSV/JSON path (e.g., data/prices_clean.csv)')
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout),
                                                      logging.FileHandler("logs/clean_task.log")],
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        clean_task(args.input or '', args.output)
    except Exception as e:
        logging.exception("clean_task failed: %s", str(e))
        raise

if __name__ == '__main__':
    main()
