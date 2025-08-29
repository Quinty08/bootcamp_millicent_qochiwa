\# Handoff Plan (summary)



\- Endpoints: `POST /predict` (JSON `{"features":\[...]}`), `GET /predict/<x>`, `GET /plot`. Auth: API key header `X-API-KEY` (add in next iteration).

\- Data contract: model expects 1 numeric feature named `x\_feature` (shape: \[n\_samples,1]). CSV schema example provided in `data/`.

\- Model versioning: store `model\_v{n}.pkl` in `/model/` and maintain `model/registry.json` with active version.

\- Retraining: automated job (Airflow) but only active after manual sign-off for production; triggered automatically if PSI > 0.05 or 7-day MAE > +10%.

\- Runbook links: store runbook/alerts.md in repo root with immediate troubleshooting steps and contact list.

\- Testing: include `tests/test\_predict.py` (basic curl/requests calls) and sample input files under `data/samples/`.



