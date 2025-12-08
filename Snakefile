"""
Snakefile

Snakemake workflow for the Climate Variability and Agricultural Productivity project.
Automates the entire analysis pipeline from data acquisition to visualization.

Authors: Dev Rishi Udata & Rohit Shah
Course: IS477
"""

# Configuration
configfile: "config.yaml"

# Define all output files
rule all:
    input:
        # Cleaned data
        "data/processed/noaa_clean.csv",
        "data/processed/usda_clean.csv",
        "data/processed/integrated.csv",
        # Analysis outputs
        "results/analysis_results.json",
        "results/data_profile.json",
        # Visualizations
        "results/yield_vs_volatility.png",
        "results/temporal_trends.png",
        "results/correlation_matrix.png",
        # Data integrity
        "data/checksums.json"

# Data acquisition rules
rule download_noaa:
    output:
        "data/raw/noaa_full.csv"
    log:
        "logs/download_noaa.log"
    shell:
        "python scripts/get_noaa_data.py > {log} 2>&1"

rule download_usda:
    output:
        "data/raw/usda_yields.csv"
    log:
        "logs/download_usda.log"
    shell:
        "python scripts/get_usda_data.py > {log} 2>&1"

# Data cleaning rules
rule clean_noaa:
    input:
        "data/raw/noaa_full.csv"
    output:
        "data/processed/noaa_clean.csv"
    log:
        "logs/clean_noaa.log"
    shell:
        "python scripts/clean_noaa.py > {log} 2>&1"

rule clean_usda:
    input:
        "data/raw/usda_yields.csv"
    output:
        "data/processed/usda_clean.csv"
    log:
        "logs/clean_usda.log"
    shell:
        "python scripts/clean_usda.py > {log} 2>&1"

# Data integration rule
rule integrate_data:
    input:
        noaa="data/processed/noaa_clean.csv",
        usda="data/processed/usda_clean.csv"
    output:
        "data/processed/integrated.csv"
    log:
        "logs/integrate_data.log"
    shell:
        "python scripts/integrate_datasets.py > {log} 2>&1"

# Data profiling rule
rule profile_data:
    input:
        "data/processed/integrated.csv"
    output:
        "results/data_profile.json"
    log:
        "logs/profile_data.log"
    shell:
        "python scripts/profile_data.py > {log} 2>&1"

# Analysis rule
rule analyze_data:
    input:
        "data/processed/integrated.csv"
    output:
        "results/analysis_results.json"
    log:
        "logs/analyze_data.log"
    shell:
        "python scripts/analyze_data.py > {log} 2>&1"

# Visualization rule
rule visualize_results:
    input:
        "data/processed/integrated.csv"
    output:
        "results/yield_vs_volatility.png",
        "results/temporal_trends.png",
        "results/correlation_matrix.png",
        "results/volatility_distribution.png",
        "results/yield_by_quartile.png",
        "results/geographic_summary.png"
    log:
        "logs/visualize_results.log"
    shell:
        "python scripts/visualize_results.py > {log} 2>&1"

# Data integrity rule
rule verify_data:
    input:
        "data/processed/integrated.csv"
    output:
        "data/checksums.json"
    log:
        "logs/verify_data.log"
    shell:
        "python scripts/verify_data.py > {log} 2>&1"

# Clean rule to remove generated files
rule clean:
    shell:
        """
        rm -f data/processed/*.csv
        rm -f results/*
        rm -f logs/*.log
        rm -f data/checksums.json
        """

