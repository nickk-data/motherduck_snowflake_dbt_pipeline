# Batch Data Migration and Modern Analytics Architecture

## Project Overview

This project demonstrates a production-grade, end-to-end data engineering pipeline that orchestrates batch data ingestion, establishes enterprise warehouse governance, and models raw data for downstream business intelligence.

The architecture bridges an external MotherDuck catalog into a highly secure, optimized Snowflake cloud data warehouse. This governed environment serves as the foundational source layer for a modular dbt (Data Build Tool) project, transforming raw ingredients into production-ready data marts.

## Repository Structure

The repository is organized into distinct functional layers to mirror modern data engineering team standards:
- [`ingestion`](/ingestion/): a Python-driven data orchestration and extraction script.
- [`snowflake_setup`](/snowflake_setup/): Warehouse infrastructure, roles & access, cost controls, and data resiliency.
- [`dbt`](/dbt/): Modular data transformation models, schema tests, and documentation.

## Infrastructure & Architecture Components

### [Ingestion Layer (Python & MotherDuck)](/ingestion/)

Located in the [ingestion](/ingestion/) directory, this layer handles the extraction and landing of source data:

- **Automated Extraction:** Developed a decoupled Python automation script [`motherduck_migration.py`](/ingestion/motherduck_migration.py) leveraging the `snowflake-connector-python` library to dynamically pull source tables from a shared MotherDuck catalog.
- **Secure Session Handshake:** Implemented a caching mechanism to elegantly resolve Snowflake Multi-Factor Authentication (MFA/TOTP) gates, ensuring secure, non-interactive script execution.
- **Environment Isolation:** Separated infrastructure secrets and connection strings from the core runtime logic using a decoupled environment layer `.env` to prevent credential leaks.

### [Warehouse Governance & Administration Layer (Snowflake SQL)](/snowflake_setup/)

Located in the [snowflake_setup](/snowflake_setup/) directory, this layer configures the databas compute and security infrastructure:

- **Role-Based Access Control (RBAC):** Enforced an enterprise-grade security model using a custom privilege hierarchy [`sf_roles.sql`](/snowflake_setup/sf_roles.sql). Created specialized functional roles (`engineering_role`, `analyst_role`) to strictly isolate read/write access, ensuring data engineers could control ingestion schemas while analysts are limited to downstream presentation layers.
- **FinOps Optimization & Cost Controls:** Configured the virtual compute warehouse [`sf_cost_controls.sql`](/snowflake_setup/sf_cost_controls.sql) to minimize cloud credit spend by dropping the auto-suspend window to 60 seconds from 10 minutes. Implemented automated Resource Monitors mapped to strict monthly quotas to proactively kill runaway queries.
- **Disaster Recovery & Resiliency:** Activated Snowflake's native Time Travel engine across ingestion schemas [`sf_data_resiliency.sql`](/snowflake_setup/sf_data_resiliency.sql). Documented business continuity protocols by establishing historical delta tracking and configuring table recovery commands (`UNDROP`) to safeguard against destructive operations.

### [Transformation & Data Modeling Layer (dbt)](/dbt/)

> **Status:** *In Active Development*

With the raw source data successfully migrated into Snowflake, I am currently building out the transformation layer using **dbt (Data Build Tool)** to turn raw data into analytics-ready data marts. This will be stored in the [dbt](/dbt/) directory.

#### Key Objectives & Architecture:
- **Multi-Layer Modeling:** Implementing a modular architecture moving from raw staging tables (Silver layer) to optimized business marts (Gold layer)
- **Semi-Structured Data Parsing:** Extracting, flattening, and modeling complex raw **JSON payloads** into clean, relational flat marts
- **Data Quality & Testing:** Enforcing data integrity by implementing robust dbt tests for primary keys, null values, and referential integrity across all critical schemas


## Technical Skills Demonstrated

- **Languages:** Python, SQL (Snowflake dialect), Git, Bash, dbt
- **Cloud Architecture:** Snowflake Cloud Data Warehouse Administration, MotherDuck Data Sharing
- **Security & Governance:** Role-Based Access Control (RBAC), Privilege Hierarchies, IAM Principles
- **Cloud FinOps:** Cost Optimization, Compute Isolation, Warehouse Resource Monitoring
- **Methodologies:** ELT Target Design, System Environment Isolation, Disaster Recovery / Data Resiliency, Data Modeling