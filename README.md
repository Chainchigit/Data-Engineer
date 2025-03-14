# Data Engineer - Interview Assignment

##  Overview
This repository contains solutions for the **Data Engineer Take-Home Assignment**, covering three main tasks:
1. **Data Pipeline Design** - Designing a scalable ETL pipeline using GCP.
2. **Text Sanitizer** - Implementing a CLI-based text processing tool in Python.
3. **SQL Query** - Extracting top product sales using SQL.

---

##  **1. Data Pipeline Design**
### **Objective:**
- Design a **high-level daily batch ingestion pipeline** from **MongoDB** (semi-structured data) to **BigQuery**.
- Ensure **scalability, data quality, and exception handling**.
- Provide a user-friendly schema in **BigQuery** for business users and data scientists.

### **Solution:**
- **Extract** data from **MongoDB** using **Cloud Dataflow (Apache Beam)**.
- **Stage raw data** in **Google Cloud Storage (GCS)** in **Avro/Parquet format**.
- **Transform & Clean** using **Cloud Dataproc (Apache Spark)**.
- **Load structured data** into **partitioned & clustered BigQuery tables**.
- **Orchestrate & Monitor** using **Cloud Composer (Airflow) + Logging & Alerting**.

### **Deliverables:**
- **`data_pipeline_diagram.png`** - High-level architecture diagram.
- **`data_pipeline_design.md`** - Detailed explanation of the pipeline.

---

##  **2. Text Sanitizer**
### **Objective:**
- Implement a **text processing application** in **Python 3** that:
  - Reads a text file (`source` argument).
  - Converts text to **lowercase**.
  - Replaces **tabs (`\t`) with `____`**.
  - Generates **character occurrence statistics**.
  - Prints output to the console (or writes to a `target` file).
  - Supports **extensibility** for additional sanitization rules & statistics.

### **Deliverables:**
- **`text_sanitizer.py`** - Python script implementing text sanitization.
- **`sample_input.txt`** - Example input text file.

---

##  **3. SQL Query - Top 2 Sales per Product Class**
### **Objective:**
- Write an **SQL query** to extract **top 2 product sales per class**.
- Order by **product class, sales value**, and **quantity (tie-breaker)**.

### **Solution:**
- **Use CTEs (`WITH` clause)** to aggregate sales data.
- **Apply `RANK()`** to rank products within each class.
- **Filter top 2 products per class (`WHERE rank <= 2`)**.


