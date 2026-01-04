import pandas as pd
import os

FILE_PATH = 'gold_layer/fact_operational_events.parquet'

if not os.path.exists(FILE_PATH):
    print(f"Error: {FILE_PATH} not found. Run etl_pipeline.py first.")
else:
    df = pd.read_parquet(FILE_PATH)
    print(f"Loaded {len(df)} events from {FILE_PATH}")
    print("\n[Audit: High Risk Events (>70)]")
    audit_cols = ['zone_id', 'time_id', 'event_type_id', 'impact_score', 'severity_id']
    print(df[df['impact_score'] > 70][audit_cols].head(10).to_string(index=False))
