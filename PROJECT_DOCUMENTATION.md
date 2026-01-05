#  CAN 2025 Command Center - Project Documentation


## 1.  Project Overview

The **CAN 2025 Pilotage Platform** is a data-driven Decision Support System (DSS) designed to ensure the operational success of the Africa Cup of Nations in Morocco. It centralizes critical data streams to anticipate incidents, optimize mobility, and ensure fan safety.

### Key Scope
*   **Multi-City Coverage**: Surveillance across **Casablanca** (High Density), **Rabat** (Admin), **Marrakech**, and **Agadir**.
*   **Multi-Domain Intelligence**: Unified view of **Mobility**, **Affluence** (Crowd), **Weather**, **Security**, and **Infrastructure**.
*   **Predictive Core**: Unlike passive dashboards, this system calculates active **Risk Scores** to trigger alerts *before* critical failures occur.

### The "Casablanca Storm" Scenario
To demonstrate the platform's value, the POC includes a specific simulation:
*   **Casablanca (Zone 1)**: Simulates a severe storm hitting at **20:00 (Match Peak)**, causing traffic gridlock (Mobility) and crowd bottlenecks (Affluence).
*   **Control Groups (Rabat/Others)**: Maintain standard operating parameters to prove the system's ability to distinguish localized crises from normal operations.

---

## 2.  Architecture & Data Flow

The solution runs on a **Modern Data Lakehouse** architecture (Azure Synapse + Python), prioritizing flexibility and batch reliability over complex streaming infrastructure.

### Data Pipeline Stages
1.  **Ingestion (Bronze)**: Raw data (CSV/JSON) collected from 5 domain sources for each city.
2.  **Processing (Silver)**: **Python ETL** script adds semantic meaning, cleans nulls, and aligns timestamps.
3.  **Intelligence (Gold)**: Application of the **Risk Scoring Model** (Python) to generate `Fact_Operational_Events`.
4.  **Serving**: **Star Schema** hosted in **Azure Synapse Serverless SQL** for high-performance querying.
5.  **Visualization**: **Power BI** consumes the Gold layer for 3 strategic dashboards.

### Star Schema Diagram
```text
       [Dim_Date]          [Dim_Zone]           [Dim_Time]
            |                  |                    |
            +---------+--------+---------+----------+
                      |        |         |
                  [Fact_Operational_Events]
                      |        |         |
            +---------+--------+---------+----------+
            |                  |                    |
   [Dim_EventType]      [Dim_Severity]      [Dim_Infrastructure]
```

**Orchestration**:
*   **Azure Data Factory (ADF)** triggers the pipeline every **15 minutes** during operational windows.
*   This batch approach reduces costs by 90% compared to real-time streaming while meeting the 30-minute decision cycle requirement.

---

## 3.  ETL & Simulation

The core logic is encapsulated in a robust Python pipeline that handles Multi-City generation and Domain syncing.

### Project Structure
*   `etl_pipeline.py`: Main driver. Generates simulated data, applies scenarios, and outputs Parquet.
*   `risk_scoring.py`: (Optional Import) Reference class for the scoring logic verification.
*   `gold_layer/`: Directory containing the analytics-ready `fact_operational_events.parquet`.

### Simulation Logic
The ETL explicitly generates 5 event types per hour per zone:
1.  **Mobility** (Traffic congestion index)
2.  **Affluence** (Fan Zone density)
3.  **Weather** (Precipitation/Wind impact)
4.  **Security** (Incident probability)
5.  **Infrastructure** (Status check)

---

## 4.  Risk Scoring & Scenarios

The "Brain" of the platform is a deterministic, white-box algorithm ensuring explainability to government officials.

### The Composite Formula
```python
Risk Score = (
    (Affluence % * 0.35) +    # Crowd Density (Highest Weight)
    (Weather %   * 0.25) +    # Environmental Multiplier
    (Traffic %   * 0.20) +    # Emergency Access Blockers
    (Infra %     * 0.20)      # Operational Failure
) * 100
```

### Thresholds & Actions
| Score Range | Level | Action Plan |
|:---:|:---:|:---|
| **0 - 40** | 🟢 **NORMAL** | Standard Monitoring. |
| **40 - 70** | 🟠 **VIGILANCE** | Pre-position resources. Dashboard highlights driving factor. |
| **> 70** | 🔴 **CRITICAL** | **Push Alert**. Activate Emergency Response (e.g., Open Gates). |

---

## 5.  Power BI Integration

Three specialized views serve different stakeholders, all fed by the same Single Version of Truth (SVOT).

### 1. Command Center (Executive)
*   **Focus**: Global Situational Awareness.
*   **Key Visual**: Map of Morocco with Cities colored by Max Risk Score.
*   **Scenario demo**: Shows Casablanca turning **RED** at 20:00 while Rabat stays **GREEN**.

### 2. Mobility Dashboard (Operational)
*   **Focus**: Traffic flow & Parking.
*   **Key Metric**: `Duration Minutes` (Access Time).
*   **Scenario demo**: Shows "Access Time" spiking to 90 mins in Casablanca Zone 1.

### 3. Safety Dashboard (Field)
*   **Focus**: Fan Zones & Incidents.
*   **Key Metric**: `Affected People` vs `Capacity`.
*   **Scenario demo**: Details the specific "Storm" event type contributing to the risk.

---

## 6.  Validation & Testing

### Verification Checklist
| Check | Operational Goal | Status |
|---|---|---|
| **Row Counts** | ~240 Events (4 Cities * 12 Hrs * 5 Domains) | ✅ PASS |
| **Scoring Logic** | Casablanca Storm triggers Score > 90 | ✅ PASS |
| **Control Group** | Rabat maintains Score < 40 | ✅ PASS |
| **Integrity** | All `zone_id`s match `Dim_Zone` definitions | ✅ PASS |

### Sample Data Preview
*Fact Table Snapshot (Casablanca Storm Peak)*
```text
zone_id | time_id | domain   | score | severity
   1    |  2000   | Weather  | 93.0  | CRITICAL (3)
   1    |  2000   | Mobility | 95.0  | CRITICAL (3)
   1    |  2000   | Affluence| 88.0  | CRITICAL (3)
```

---

## 7.  Usage Instructions / Runbook

Follow these steps to reproduce the POC environment locally.

### Prerequisites
*   Python 3.8+
*   `pandas`, `numpy`, `pyarrow`, `fastparquet`

### Step-by-Step Execution

**1. Install Dependencies**
```bash
pip install pandas numpy pyarrow fastparquet
```

**2. Run the Simulation ETL**
This script generates the data and applies the "Casablanca Storm" logic.
```bash
python etl_pipeline.py
```
*Output: `gold_layer/fact_operational_events.parquet`*

**3. Verify Output (Optional)**
Create a simple script `preview_fact.py` to inspect the results.
```python
import pandas as pd
df = pd.read_parquet('gold_layer/fact_operational_events.parquet')
print(df[df['impact_score'] > 70].head())
```

**4. Connect Power BI**
1.  Open Power BI Desktop.
2.  Get Data -> **Parquet** -> Point to `gold_layer/`.
3.  (Or) Connect to Azure Synapse SQL Endpoint if deployed.

---

## 8. 📝 Notes & Recommendations

### Privacy & GDPR
*   **Aggregation**: Data is stored at `Zone` level, not Individual. No PII (Personally Identifiable Information) is ingested.
*   **Compliance**: Meets CNDP requirements for mass event monitoring.

### Scalability
*   **Batch vs Streaming**: Elected for 15-min Batch to ensure system robustness. Architecture allows "lifting and shifting" to Event Hubs/Stream Analytics if sub-minute latency becomes mandatory for specific domains (e.g., Medical Emergencies) in 2030.

---

