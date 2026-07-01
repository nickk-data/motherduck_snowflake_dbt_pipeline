# Batch Data Migration and Modern Analytics Architecture

## Project Overview

This project establishes a production-ready, highly secure cloud data warehouse foundation inside Snowflake by executing an automated batch ingestion from MotherDuck.

The core architectural goal of this project was to establish a fully optimized, governed landing zone for raw data. By designing the compute infrastructure, access controls, and object layers natively inside Snowflake, the environment is now explicitly architected to act as a seamless source layer for a downstream dbt (Data Build Tool) project to build modular data models, staging layers, and denormalized data marts.

## Infrastructure & Architecture Components

### 1. Source Extraction & Ingestion

- Developed a Python-driven automation script [`motherduck_migration.py`](/ingestion/motherduck_migration.py) leveraging the `snowflake-connector-python` library to dynamically extract source tables from a MotherDuck shared catalog (`data_jobs`)
- Configured local secure storage caching modules to natively resolve Snowflake's Multi-Factor Authentication (MFA/TOTP) gates, establishing an automated, secure session handshake
- Separated infrastructure secrets from runtime logic by managing keys via a decoupled local environment layer (`.env`)

### 2. Production Snowflake Administration & FinOps Governance

- **Role-Based Access Control (RBAC):** Designed and enforced an enterprise-grade security model using specialized privilege rings [`sf_roles.sql`](/snowflake_setup/sf_roles.sql). Built custom operational roles (`engineering_role`, `analyst_role`), isolating access to ensure engineers retain structural administration over ingestion schemas while analysts are limited strictly to future presentation views.
- **Warehouse Optimization & Cost Controls:** Configured the `data_jobs` virtual warehouse to minimize cloud credit consumption by dropping the active cluster auto-suspend window to 60 seconds [`sf_cost_controls.sql`](/snowflake_setup/sf_cost_controls.sql). Implemented automated Resource Monitors bound to strict monthly credit quotes to automatically terminate runaway queries.
- **Data Resiliency & Disaster Recovery:** Activated Snowflake's native Time Travel engine on the ingestion schemas [`sf_data_resiliancy.sql`](/snowflake_setup/sf_data_resiliency.sql). Demonstrated business continuity techniques by configuring historical delta tracking and instant table recovery (`UNDROP`) to guard against destructive commands or manual deployment drops.

### 3. Transformations & Data Modeling in dbt
> **Status:** *In Active Development*

With the raw source data successfully migrated into Snowflake, I am currently building out the transformation layer using **dbt (Data Build Tool)** to turn raw data into analytics-ready data marts.

#### Key Objectives & Architecture:
- **Multi-Layer Modeling:** Implementing a modular architecture moving from raw staging tables (Silver layer) to optimized business marts (Gold layer)
- **Semi-Structured Data Parsing:** Extracting, flattening, and modeling complex raw **JSON payloads** into clean, relational flat marts
- **Data Quality & Testing:** Enforcing data integrity by implementing robust dbt tests for primary keys, null values, and referential integrity across all critical schemas


## Technical Skills Demonstrated

- **Languages:** Python, SQL (Snowflake dialect), Git, Bash
- **Cloud Architecture:** Snowflake Cloud Data Warehouse Administration, MotherDuck Data Sharing
- **Security & Governance:** Role-Based Access Control (RBAC), Privilege Hierarchies, IAM Principles
- **Cloud FinOps:** Cost Optimization, Compute Isolation, Warehouse Resource Monitoring
- **Methodologies:** ELT Target Design, System Environment Isolation, Disaster Recovery / Data Resiliency