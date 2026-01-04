import pandas as pd
import numpy as np
import os
import random

# Configuration
RAW_PATH = 'raw_data/'
OUTPUT_PATH = 'gold_layer/'
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Domain Definitions with Weights (for Global Score)
EVENT_TYPES = {
    0: {'name': 'Global Risk Snapshot', 'domain': 'Composite', 'weight': 0.0}, # Calculated
    1: {'name': 'Mobility Congestion', 'domain': 'Mobility', 'weight': 0.20},
    2: {'name': 'Fan Zone Density', 'domain': 'Affluence', 'weight': 0.35},
    3: {'name': 'Weather Condition', 'domain': 'Weather', 'weight': 0.25},
    4: {'name': 'Security Incident', 'domain': 'Security', 'weight': 0.00}, # Independent
    5: {'name': 'Infrastructure Status', 'domain': 'Infrastructure', 'weight': 0.20}
}

# 4 Zones
ZONES = {
    1: {'name': 'Casablanca Zone', 'city': 'Casablanca'},
    2: {'name': 'Rabat Zone', 'city': 'Rabat'},
    3: {'name': 'Marrakech Zone', 'city': 'Marrakech'},
    4: {'name': 'Agadir Zone', 'city': 'Agadir'}
}

def get_base_metrics(zone_id, hour):
    # Base Traffic: Peaks at 18:00-20:00
    is_peak = 17 <= hour <= 20
    base_traffic = random.randint(40, 70) if is_peak else random.randint(10, 30)
    
    # Base Affluence: Peaks at match time (assume 20:00)
    base_affluence = random.randint(60, 80) if (19 <= hour <= 21) else random.randint(10, 40)
    
    # Base Weather: Mostly Sunny/Clear (10-20)
    base_weather = random.randint(0, 20)
    
    # Base Infra: usually good
    base_infra = random.randint(0, 10)
    
    return base_traffic, base_affluence, base_weather, base_infra

def apply_scenario(zone_id, hour, base_metrics):
    traffic, affluence, weather, infra = base_metrics
    
    # SCENARIO: Casablanca (Zone 1) on Dec 21st
    if zone_id == 1:
        # Storm hits 18:00 - 22:00
        if 18 <= hour <= 22:
            weather = random.randint(90, 100) # Storm
            traffic = min(traffic + 40, 100)  # Gridlock
            affluence = min(affluence + 10, 100) # Crowds stuck
            infra = 65 # Drainage strain
            
    return traffic, affluence, weather, infra

def calculate_global_risk(traffic, affluence, weather, infra):
    # Weighted Sum Formula
    # Weights: Affluence(0.35), Weather(0.25), Traffic(0.20), Infra(0.20)
    score = (
        (affluence * 0.35) +
        (weather * 0.25) +
        (traffic * 0.20) +
        (infra * 0.20)
    )
    return round(score, 2)

def generate_events():
    print("Generating Multi-City, Multi-Domain Operational Events...")
    
    data = []
    event_id_counter = 1000
    date_id = 20251221
    
    for zone_id, zone_info in ZONES.items():
        city_name = zone_info['city']
        zone_name = zone_info['name']
        
        for hour in range(12, 24): # 12 hours
            
            # 1. Base Logic
            metrics = get_base_metrics(zone_id, hour)
            
            # 2. Apply Scenario
            traffic, affluence, weather, infra = apply_scenario(zone_id, hour, metrics)
            
            # 3. Calculate Global Risk for this Hour
            global_risk = calculate_global_risk(traffic, affluence, weather, infra)
            
            # 4. Generate Events
            
            # --- Type 0: Global Risk Snapshot (Composite) ---
            data.append({
                'event_id': event_id_counter,
                'date_id': date_id,
                'time_id': hour * 100,
                'zone_id': zone_id,
                'city_name': city_name,         # Explicit for Power BI
                'domain_name': 'Composite',     # Explicit for Power BI
                'event_type_id': 0,
                'impact_score': float(global_risk),
                'severity_id': 4 if global_risk > 70 else (3 if global_risk > 40 else 1),
                'affected_people': 0,
                'duration_minutes': 60
            })
            event_id_counter += 1

            # --- Type 1: Mobility ---
            data.append({
                'event_id': event_id_counter,
                'date_id': date_id,
                'time_id': hour * 100,
                'zone_id': zone_id,
                'city_name': city_name,
                'domain_name': 'Mobility',
                'event_type_id': 1,
                'impact_score': float(traffic),
                'severity_id': 1 if traffic < 40 else (3 if traffic > 70 else 2),
                'affected_people': random.randint(100, 5000),
                'duration_minutes': 60
            })
            event_id_counter += 1
            
            # --- Type 2: Affluence ---
            data.append({
                'event_id': event_id_counter,
                'date_id': date_id,
                'time_id': hour * 100,
                'zone_id': zone_id,
                'city_name': city_name,
                'domain_name': 'Affluence',
                'event_type_id': 2,
                'impact_score': float(affluence),
                'severity_id': 1 if affluence < 40 else (3 if affluence > 70 else 2),
                'affected_people': int(50000 * (affluence/100)),
                'duration_minutes': 60
            })
            event_id_counter += 1
            
            # --- Type 3: Weather ---
            data.append({
                'event_id': event_id_counter,
                'date_id': date_id,
                'time_id': hour * 100,
                'zone_id': zone_id,
                'city_name': city_name,
                'domain_name': 'Weather',
                'event_type_id': 3,
                'impact_score': float(weather),
                'severity_id': 1 if weather < 40 else (3 if weather > 70 else 2),
                'affected_people': 0,
                'duration_minutes': 60
            })
            event_id_counter += 1
            
            # --- Type 4: Security (Independent) ---
            sec_score = random.randint(0, 20)
            if zone_id == 1 and weather > 80: sec_score += 30
            
            data.append({
                'event_id': event_id_counter,
                'date_id': date_id,
                'time_id': hour * 100,
                'zone_id': zone_id,
                'city_name': city_name,
                'domain_name': 'Security',
                'event_type_id': 4,
                'impact_score': float(sec_score),
                'severity_id': 1 if sec_score < 40 else 2,
                'affected_people': 0,
                'duration_minutes': 60
            })
            event_id_counter += 1

             # --- Type 5: Infrastructure ---
            data.append({
                'event_id': event_id_counter,
                'date_id': date_id,
                'time_id': hour * 100,
                'zone_id': zone_id,
                'city_name': city_name,
                'domain_name': 'Infrastructure',
                'event_type_id': 5,
                'impact_score': float(infra),
                'severity_id': 1 if infra < 40 else 2,
                'affected_people': 0,
                'duration_minutes': 60
            })
            event_id_counter += 1

    return pd.DataFrame(data)

def main():
    df_fact = generate_events()
    
    # Output
    output_file = os.path.join(OUTPUT_PATH, 'fact_operational_events.parquet')
    print(f"Saving {len(df_fact)} events to {output_file}...")
    df_fact.to_parquet(output_file, index=False)
    
    print("\n[Validation - Casablanca Storm (Peak 20:00)]")
    cols = ['zone_id', 'city_name', 'time_id', 'domain_name', 'impact_score', 'severity_id']
    casa = df_fact[(df_fact['zone_id'] == 1) & (df_fact['time_id'] == 2000)]
    print(casa[cols].to_string(index=False))
    
    print("\n[Validation - Rabat Standard (20:00)]")
    rabat = df_fact[(df_fact['zone_id'] == 2) & (df_fact['time_id'] == 2000)]
    print(rabat[cols].to_string(index=False))
    
    print("\nVerify Security Events:")
    sec = df_fact[df_fact['domain_name'] == 'Security']
    print(f"Total Security Events: {len(sec)}")
    print(sec[['city_name', 'impact_score']].head(3).to_string(index=False))

if __name__ == "__main__":
    main()
