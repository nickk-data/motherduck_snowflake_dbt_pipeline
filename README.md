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

- **Two-Tier Role-Based Access Control (RBAC):** Designed a decoupled governance hierarchy by mapping lower-level Object Access Roles (`raw_write_ar`, `raw_read_ar`) to functional business personas (`engineering_role`, `analyst_role`), ensuring strict privilege isolation across schemas [`sf_roles.sql`](/snowflake_setup/sf_roles.sql).
- **Multi-Tier FinOps Circuit Breakers:** Optimized compute consumption via aggressive 60-second auto-suspend gates paired with a monthly Resource Monitor budget cap configured with a hard `suspend_immediate` trigger to forcefully terminate runaway or sub-optimal queries [`sf_cost_controls.sql`](/snowflake_setup/sf_cost_controls.sql). 
- **Production Incident Recovery (Zero-Copy Cloning):** Formulated an enterprise disaster recovery protocol mimicking pipeline failures. Documented the use of state-targeted Time Travel (via Query ID markers) to perform Zero-Copy Cloning and metadata `swap with` table restoration to resolve data corruption with zero platform downtime [`sf_data_resiliency.sql`](/snowflake_setup/sf_data_resiliency.sql). 

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
- **Security & Governance:** Two-Tier RBAC, Future Access Privileges, Asymmetric Cryptography, RSA Key-Pair Ingestion
- **Cloud FinOps:** Resource Monitoring Circuit Breakers, `suspend_immediate` execution blocks
- **Methodologies:** ELT Target Design, System Environment Isolation, Zero-Copy Cloning, Table Metadata Swapping, Data Modeling
