-- Azure Synapse Analytics (Serverless SQL Pool) DDL
-- Context: POC for CAN 2025 Pilotage
-- Optimization: Added Time Dimension and Infrastructure Granularity

-- 1. Setup Data Source (Assumed)
/*
IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'AzureDataLakeStorage')
CREATE EXTERNAL DATA_SOURCE [AzureDataLakeStorage] 
WITH ( LOCATION = 'https://<datalake>.dfs.core.windows.net/bi-container' );
*/

-- 2. External File Format
/*
IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseParquetFormat')
CREATE EXTERNAL FILE FORMAT [SynapseParquetFormat] 
WITH ( FORMAT_TYPE = PARQUET, DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec' );
*/

-- =============================================
-- Dimensions
-- =============================================

-- Dim_Time (NEW: Essential for hourly analysis)
CREATE EXTERNAL TABLE [dbo].[Dim_Time] (
    [time_id] INT,              -- HHMM format (e.g. 1430)
    [hour_24] INT,              -- 0-23
    [time_slot] VARCHAR(20),    -- 'Morning', 'Afternoon', 'Peak Match'
    [is_peak_hour] BIT
)
WITH (
    LOCATION = 'gold/dim_time/',
    DATA_SOURCE = [AzureDataLakeStorage],
    FILE_FORMAT = [SynapseParquetFormat]
);

-- Dim_Date
CREATE EXTERNAL TABLE [dbo].[Dim_Date] (
    [date_id] INT,
    [full_date] DATE,
    [day_name] VARCHAR(10),
    [match_day] BIT,
    [peak_period] BIT,
    [week_number] INT
)
WITH (
    LOCATION = 'gold/dim_date/',
    DATA_SOURCE = [AzureDataLakeStorage],
    FILE_FORMAT = [SynapseParquetFormat]
);

-- Dim_Zone
CREATE EXTERNAL TABLE [dbo].[Dim_Zone] (
    [zone_id] INT,
    [zone_name] VARCHAR(100),
    [city] VARCHAR(50),
    [zone_type] VARCHAR(20),
    [capacity_max] INT,
    [latitude] DECIMAL(10,8),
    [longitude] DECIMAL(11,8)
)
WITH (
    LOCATION = 'gold/dim_zone/',
    DATA_SOURCE = [AzureDataLakeStorage],
    FILE_FORMAT = [SynapseParquetFormat]
);

-- Dim_Infrastructure (Linked to Zone)
CREATE EXTERNAL TABLE [dbo].[Dim_Infrastructure] (
    [infra_id] INT,
    [infra_name] VARCHAR(100),
    [infra_type] VARCHAR(30),
    [zone_id] INT,              -- Parent Zone
    [capacity] INT,
    [opening_hours] VARCHAR(50)
)
WITH (
    LOCATION = 'gold/dim_infrastructure/',
    DATA_SOURCE = [AzureDataLakeStorage],
    FILE_FORMAT = [SynapseParquetFormat]
);

-- Dim_EventType
CREATE EXTERNAL TABLE [dbo].[Dim_EventType] (
    [event_type_id] INT,
    [type_name] VARCHAR(50),
    [domain] VARCHAR(20),
    [criticality_base] INT
)
WITH (
    LOCATION = 'gold/dim_eventtype/',
    DATA_SOURCE = [AzureDataLakeStorage],
    FILE_FORMAT = [SynapseParquetFormat]
);

-- Dim_Severity
CREATE EXTERNAL TABLE [dbo].[Dim_Severity] (
    [severity_id] INT,
    [severity_level] VARCHAR(20),
    [color_code] VARCHAR(20),
    [action_required] VARCHAR(10)
)
WITH (
    LOCATION = 'gold/dim_severity/',
    DATA_SOURCE = [AzureDataLakeStorage],
    FILE_FORMAT = [SynapseParquetFormat]
);

-- =============================================
-- Fact Table
-- =============================================

-- Fact_Operational_Events
-- Improvements:
-- 1. Added [time_id] for intraday analytics (Traffic peaks, halftime crowds).
-- 2. Added [infra_id] for granular location (Specific gate failure vs generic Stadium issue).
CREATE EXTERNAL TABLE [dbo].[Fact_Operational_Events] (
    [event_id] BIGINT,
    [date_id] INT,
    [time_id] INT,              -- FK to Dim_Time (NEW)
    [zone_id] INT,
    [infra_id] INT,             -- FK to Dim_Infrastructure (NEW, Nullable)
    [event_type_id] INT,
    [severity_id] INT,
    
    -- Metrics
    [duration_minutes] INT,
    [impact_score] DECIMAL(5,2),
    [resolution_time_min] INT,
    [affected_people] INT,
    [cost_estimate_mad] DECIMAL(12,2),
    
    -- Audit
    [ingestion_timestamp] DATETIME2
)
WITH (
    LOCATION = 'gold/fact_operational_events/',
    DATA_SOURCE = [AzureDataLakeStorage],
    FILE_FORMAT = [SynapseParquetFormat]
);
