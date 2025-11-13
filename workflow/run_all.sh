#!/bin/bash

################################################################################
# run_all.sh
#
# Data cleaning workflow for Climate Variability and Agricultural
# Productivity in Illinois project (Weeks 4-5).
#
# Authors: Dev Rishi Udata & Rohit Shah
# Course: IS477
################################################################################

set -e  # Exit on error

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================"
echo "Climate & Agriculture Data Pipeline"
echo "Weeks 4-5: Data Cleaning"
echo "========================================"
echo ""
echo "Project root: $PROJECT_ROOT"
echo ""

# Create necessary directories
echo "[1/4] Setting up directories..."
mkdir -p "$PROJECT_ROOT/data/raw"
mkdir -p "$PROJECT_ROOT/data/processed"
mkdir -p "$PROJECT_ROOT/scripts"
mkdir -p "$PROJECT_ROOT/docs"
echo ""

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Check if raw data exists
echo "[2/4] Checking for raw data files..."
if [ ! -f "$PROJECT_ROOT/data/raw/noaa_full.csv" ]; then
    echo "Warning: noaa_full.csv not found in data/raw/"
    echo "Run: python scripts/get_noaa_data.py"
fi

if [ ! -f "$PROJECT_ROOT/data/raw/usda_yields.csv" ]; then
    echo "Warning: usda_yields.csv not found in data/raw/"
    echo "Run: python scripts/get_usda_data.py"
fi
echo ""

# Step 1: Clean NOAA data
echo "[3/4] Cleaning NOAA weather data..."
python3 "$PROJECT_ROOT/scripts/clean_noaa.py"
if [ $? -eq 0 ]; then
    echo "NOAA data cleaned successfully"
else
    echo "Error: NOAA data cleaning failed"
    exit 1
fi
echo ""

# Step 2: Clean USDA data
echo "[4/4] Cleaning USDA crop yield data..."
python3 "$PROJECT_ROOT/scripts/clean_usda.py"
if [ $? -eq 0 ]; then
    echo "USDA data cleaned successfully"
else
    echo "Error: USDA data cleaning failed"
    exit 1
fi
echo ""

# Summary
echo "========================================"
echo "Pipeline Summary (Weeks 4-5)"
echo "========================================"
echo "Cleaned NOAA data: data/processed/noaa_clean.csv"
echo "Cleaned USDA data: data/processed/usda_clean.csv"
echo "========================================"
echo ""
echo "Data cleaning completed successfully!"
echo ""
echo "Next steps (Week 6):"
echo "  - Integrate NOAA and USDA datasets"
echo "  - Calculate temperature volatility metrics"
echo "  - Prepare for statistical analysis"
echo ""

# Show file sizes
echo "Output file sizes:"
ls -lh "$PROJECT_ROOT/data/processed/"*.csv 2>/dev/null || echo "No output files found"
echo ""

exit 0
