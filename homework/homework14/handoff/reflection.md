1\) Reflection 



Risks if deployed:

Our baseline linear regression model, if deployed, could fail in several ways. Schema drift (extra or missing columns) may break inputs. Data pipelines may produce late or stale batches. Feature distributions could shift over time, reducing model accuracy. At the system level, API response times could increase under higher load. Finally, business metrics like approval/reject rates could deviate from expectations, harming downstream use cases.



Monitoring metrics across layers:



Data: freshness\_minutes < 10, null\_rate < 2%, schema\_hash must match expected signature.



Model: rolling MAE monitored daily; trigger alert if 7-day MAE rises >20% from baseline. Calibration error tracked quarterly.



System: p95 latency < 250ms; error\_rate < 1%.



Business: approval\_rate tracked weekly with alert if shift >5%; bad\_rate monitored monthly.



Ownership \& handoffs:



Data layer: monitored by data engineering team; alerts logged in issue tracker.



Model layer: reviewed weekly by data science team; retraining triggered if population stability index (PSI) > 0.05 or rolling AUC < 0.60.



System layer: owned by platform engineering; on-call receives alerts if latency/error thresholds breached.



Business layer: reviewed by analysts monthly; issues escalated to product owner.



Handoffs are defined in README: ownership roles, escalation contacts, and rollback procedures are documented. This ensures reproducibility and safe recovery if failures occur.

