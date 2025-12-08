#!/bin/bash

################################################################################
# run_all.sh
#
# Complete reproducible workflow for Climate Variability and Agricultural
# Productivity in Illinois project.
#
# Authors: Dev Rishi Udata & Rohit Shah
# Course: IS477
################################################################################

set -e  # Exit on error

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "========================================"
echo "Climate & Agriculture Data Pipeline"
echo "Complete Analysis Workflow"
echo "========================================"
echo ""
echo "Project root: $PROJECT_ROOT"
echo ""

# Create necessary directories
echo "[1/11] Setting up directories..."
mkdir -p "$PROJECT_ROOT/data/raw"
mkdir -p "$PROJECT_ROOT/data/processed"
mkdir -p "$PROJECT_ROOT/results"
mkdir -p "$PROJECT_ROOT/logs"
echo ""

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version: $(python3 --version)"
echo ""

# Check if raw data exists
echo "[2/11] Checking for raw data..."
if [ ! -f "$PROJECT_ROOT/data/raw/noaa_full.csv" ]; then
    echo "Warning: noaa_full.csv not found"
    echo "Attempting to download..."
    python3 "$PROJECT_ROOT/scripts/get_noaa_data.py" || echo "Download skipped"
fi

if [ ! -f "$PROJECT_ROOT/data/raw/usda_yields.csv" ]; then
    echo "Warning: usda_yields.csv not found"
    echo "Attempting to download..."
    python3 "$PROJECT_ROOT/scripts/get_usda_data.py" || echo "Download skipped"
fi
echo ""

# Clean NOAA data
echo "[3/11] Cleaning NOAA weather data..."
python3 "$PROJECT_ROOT/scripts/clean_noaa.py"
if [ $? -eq 0 ]; then
    echo "NOAA data cleaned"
else
    echo "Error: NOAA cleaning failed"
    exit 1
fi
echo ""

# Clean USDA data
echo "[4/11] Cleaning USDA crop yield data..."
python3 "$PROJECT_ROOT/scripts/clean_usda.py"
if [ $? -eq 0 ]; then
    echo "USDA data cleaned"
else
    echo "Error: USDA cleaning failed"
    exit 1
fi
echo ""

# Integrate datasets
echo "[5/11] Integrating datasets..."
python3 "$PROJECT_ROOT/scripts/integrate_datasets.py"
if [ $? -eq 0 ]; then
    echo "Integration complete"
else
    echo "Error: Integration failed"
    exit 1
fi
echo ""

# Profile data
echo "[6/11] Profiling data quality..."
python3 "$PROJECT_ROOT/scripts/profile_data.py"
if [ $? -eq 0 ]; then
    echo "Data profiling complete"
else
    echo "Warning: Profiling had issues"
fi
echo ""

# Run analysis
echo "[7/11] Running statistical analysis..."
python3 "$PROJECT_ROOT/scripts/analyze_data.py"
if [ $? -eq 0 ]; then
    echo "Analysis complete"
else
    echo "Error: Analysis failed"
    exit 1
fi
echo ""

# Generate visualizations
echo "[8/11] Generating visualizations..."
python3 "$PROJECT_ROOT/scripts/visualize_results.py"
if [ $? -eq 0 ]; then
    echo "Visualizations created"
else
    echo "Error: Visualization failed"
    exit 1
fi
echo ""

# Verify data integrity
echo "[9/11] Computing checksums..."
python3 "$PROJECT_ROOT/scripts/verify_data.py"
if [ $? -eq 0 ]; then
    echo "Checksums generated"
else
    echo "Warning: Checksum generation had issues"
fi
echo ""

# Summary
echo "[10/11] Generating summary..."
echo "========================================"
echo "Pipeline Summary"
echo "========================================"
echo ""
echo "Data Files:"
echo "  Raw NOAA: data/raw/noaa_full.csv"
echo "  Raw USDA: data/raw/usda_yields.csv"
echo "  Cleaned NOAA: data/processed/noaa_clean.csv"
echo "  Cleaned USDA: data/processed/usda_clean.csv"
echo "  Integrated: data/processed/integrated.csv"
echo ""
echo "Analysis Outputs:"
echo "  Results: results/analysis_results.json"
echo "  Profile: results/data_profile.json"
echo "  Checksums: data/checksums.json"
echo ""
echo "Visualizations:"
ls -1 "$PROJECT_ROOT/results/"*.png 2>/dev/null | sed 's|.*/|  |' || echo "  (none generated)"
echo ""
echo "========================================"
echo ""

echo "[11/11] Workflow complete!"
echo ""
echo "All pipeline steps executed successfully!"
echo "Results are in the 'results/' directory"
echo ""

# Show file sizes
echo "Data file sizes:"
ls -lh "$PROJECT_ROOT/data/processed/"*.csv 2>/dev/null || echo "No files found"
echo ""

exit 0
