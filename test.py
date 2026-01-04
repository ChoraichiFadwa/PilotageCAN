# # import pandas as pd

# # df = pd.read_parquet('gold_layer/fact_operational_events.parquet')

# # Quick checks
# #print(df.shape)  # Should be (288, ...)
# # print(df['city_name'].unique())  # Casablanca, Rabat, Marrakech, Agadir
# # print(df['domain_name'].unique())  # Mobility, Affluence, Weather, Security, Infrastructure, Composite

# # Check a key scenario
# # print(df[(df['city_name']=='Casablanca') & (df['domain_name']=='Composite') & (df['time_id']==2000)])
# import pandas as pd

# df = pd.read_parquet('gold_layer/fact_operational_events.parquet')
# df.to_csv("gold_layer/fact_operational_events.csv", index=False)


import pandas as pd

# Load fact table
fact = pd.read_parquet('gold_layer/fact_operational_events.parquet')
print(fact.columns)
# 1. Dim_Date
# dim_date = fact[['date_id']].drop_duplicates()
# dim_date['full_date'] = pd.to_datetime(dim_date['date_id'], format='%Y%m%d')
# dim_date['day_name'] = dim_date['full_date'].dt.day_name()
# dim_date['week_number'] = dim_date['full_date'].dt.isocalendar().week
# dim_date['match_day'] = 1  # or logic to mark matches
# dim_date['peak_period'] = 0  # or logic
# dim_date.to_parquet('gold_layer/dim_date.parquet', index=False)

# # 2. Dim_Time
# dim_time = fact[['time_id']].drop_duplicates()
# dim_time['hour_24'] = dim_time['time_id'] // 100
# dim_time['time_slot'] = pd.cut(dim_time['hour_24'], bins=[0,12,18,24], labels=['Morning','Afternoon','Evening'])
# dim_time['is_peak_hour'] = dim_time['hour_24'].isin([18,19,20,21]).astype(int)
# dim_time.to_parquet('gold_layer/dim_time.parquet', index=False)

# # 3. Dim_Zone
# dim_zone = fact[['zone_id','city','zone_name']].drop_duplicates()  # You need city/zone_name in fact
# dim_zone.to_parquet('gold_layer/dim_zone.parquet', index=False)

# # 4. Dim_Infrastructure
# dim_infra = fact[['infra_id','zone_id']].drop_duplicates()  # Add infra_name/type if possible
# dim_infra.to_parquet('gold_layer/dim_infrastructure.parquet', index=False)

# # 5. Dim_EventType
# dim_event = fact[['event_type_id','domain']].drop_duplicates()  # Add type_name, criticality_base
# dim_event.to_parquet('gold_layer/dim_eventtype.parquet', index=False)

# # 6. Dim_Severity
# dim_sev = fact[['severity_id']].drop_duplicates()  # Add severity_level, color_code, action_required
# dim_sev.to_parquet('gold_layer/dim_severity.parquet', index=False)
