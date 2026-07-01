# Batch Data Migration and Modern Analytics Architecture

## Project Overview

This project establishes a production-ready, highly secure cloud data warehouse foundation inside Snowflake by executing an automated batch ingestion from MotherDuck.

The core architectural goal of this project was to establish a fully optimized, governed landing zone for raw data. By designing the compute infrastructure, access controls, and object layers natively inside Snowflake, the environment is now explicitly architected to act as a seamless source layer for a downstream dbt (Data Build Tool) project to build modular data models, staging layers, and denormalized data marts.

## Infrastructure & Architecture Components

### 1. Source Extraction & Ingestion

- Developed a Python-driven automation script leveraging the `snowflake-connector-python` library to dynamically extract source tables from a MotherDuck shared catalog (`data_jobs`)
- Configured local secure storage caching modules to natively resolve Snowflake's Multi-Factor Authentication (MFA/TOTP) gates, establishing an automated, secure session handshake
- Separated infrastructure secrets from runtime logic by managing keys via a decoupled local environment layer (`.env`)

### 2. Production Snowflake Administration & FinOps Governance

- **Role-Based Access Control (RBAC):** Designed and enforced an enterprise-grade security model using specialized privilege rings. Built custom operational roles (`engineering_role`, `analyst_role`), isolating access to ensure engineers retain structural administration over ingestion schemas while analysts are limited strictly to future presentation views.
- **Warehouse Optimization & Cost Controls:** Configured the `data_jobs` virtual warehouse to minimize cloud credit consumption by dropping the active cluster auto-suspend window to 60 seconds. Implemented automated Resource Monitors bound to strict monthly credit quotes to automatically terminate runaway queries.
- **Data Resiliency & Disaster Recovery:** Activated Snowflake's native Time Travel engine on the ingestion schemas. Demonstrated business continuity techniques by configuring historical delta tracking and instant table recovery (`UNDROP`) to guard against destructive commands or manual deployment drops.

## Technical Skills Demonstrated

- **Languages:** Python, SQL (Snowflake dialect), Git, Bash
- **Cloud Architecture:** Snowflake Cloud Data Warehouse Administration, MotherDuck Data Sharing
- **Security & Governance:** Role-Based Access Control (RBAC), Privilege Hierarchies, IAM Principles
- **Cloud FinOps:** Cost Optimization, Compute Isolation, Warehouse Resource Monitoring
- **Methodologies:** ELT Target Design, System Environment Isolation, Disaster Recovery / Data Resiliency