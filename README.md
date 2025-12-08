# Climate Variability and Agricultural Productivity in Illinois

A reproducible data analysis project examining the relationship between climate variability and crop yields in Illinois.

**Course:** IS477 - Data Lifecycle  
**Authors:** Dev Rishi Udata, Rohit Shah  
**Institution:** University of Illinois at Urbana-Champaign

**Status:** Complete - All Analysis and Visualizations Finished

**Box Data Link:** [INSERT YOUR BOX LINK HERE - data.zip contains all raw and processed data]

---

## Project Overview

This project integrates historical weather data (NOAA) with agricultural yield data (USDA) to analyze how climate variability affects corn and soybean production in Illinois. Agriculture is a cornerstone of Illinois's economy, and understanding the relationship between climate patterns and crop productivity is crucial for future planning and adaptation strategies.

### Research Questions

1. **How does year-to-year temperature volatility impact corn and soybean yields in Illinois counties?**
2. **Are there identifiable thresholds in temperature or precipitation beyond which yields significantly decline?**
3. **Can long-term climate patterns (e.g., increasing average summer temperatures) be statistically linked to changes in productivity trends?**

---

## Project Structure

```
climate-agriculture-il/
│
├── data/
│   ├── raw/                  # Original data (hosted on Box)
│   │   ├── noaa_full.csv
│   │   └── usda_yields.csv
│   ├── processed/            # Cleaned & integrated data (hosted on Box)
│   │   ├── noaa_clean.csv
│   │   ├── usda_clean.csv
│   │   └── integrated.csv
│   ├── metadata/             # Data dictionaries
│   └── checksums.json        # Data integrity checksums
│
├── scripts/
│   ├── get_noaa_data.py      # NOAA data acquisition
│   ├── get_usda_data.py      # USDA data acquisition
│   ├── clean_noaa.py         # NOAA data cleaning
│   ├── clean_usda.py         # USDA data cleaning
│   ├── integrate_datasets.py # Data integration
│   ├── profile_data.py       # Data quality profiling
│   ├── analyze_data.py       # Statistical analysis
│   ├── visualize_results.py  # Visualization generation
│   ├── verify_data.py        # Checksum verification
│   └── README.md             # Scripts documentation
│
├── workflow/
│   └── run_all.sh            # Complete automated workflow
│
├── docs/
│   ├── ProjectPlan.md        # Original proposal
│   ├── QUICKSTART.md         # Quick start guide
│   └── API_SETUP_GUIDE.md    # API configuration guide
│
├── results/                  # Analysis outputs and visualizations
│   ├── analysis_results.json
│   ├── data_profile.json
│   └── *.png (visualizations)
│
├── Snakefile                 # Snakemake workflow
├── config.yaml               # Workflow configuration
├── requirements.txt          # Python dependencies
├── LICENSE                   # Code license (MIT)
├── DATA_LICENSE              # Data license (Public Domain/CC0)
├── CITATION.cff              # Citation metadata
├── REPRODUCIBILITY.md        # Complete reproduction guide
└── README.md                 # This file
```

---

## Data Sources

### 1. NOAA Climate Data Online (CDO)

- **Source:** [National Centers for Environmental Information](https://www.ncdc.noaa.gov/cdo-web/)
- **Description:** Daily weather observations including temperature (TMIN, TMAX, TAVG) and precipitation (PRCP)
- **Coverage:** Illinois weather stations, 1990-present
- **Format:** CSV via API
- **License:** Public domain

**Citation:**
> NOAA National Centers for Environmental Information. Climate Data Online. Accessed November 2024. https://www.ncdc.noaa.gov/cdo-web/

### 2. USDA National Agricultural Statistics Service (NASS)

- **Source:** [NASS Quick Stats](https://quickstats.nass.usda.gov/)
- **Description:** County-level annual corn and soybean yields (bushels per acre)
- **Coverage:** Illinois counties, 1990-present
- **Format:** CSV via Quick Stats API
- **License:** Public domain

**Citation:**
> USDA National Agricultural Statistics Service. Quick Stats Database. Accessed November 2024. https://quickstats.nass.usda.gov/

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/climate-agriculture-il.git
cd climate-agriculture-il
```

2. **Create a virtual environment (recommended):**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Data Acquisition

Before running the cleaning scripts, you need the raw data:

#### Using the APIs

1. **NOAA API:**
   - Request a token: https://www.ncdc.noaa.gov/cdo-web/token
   - Use API to download Illinois weather data
   - Save as `data/raw/noaa_full.csv`

2. **USDA NASS API:**
   - Request an API key: https://quickstats.nass.usda.gov/api
   - Query for Illinois corn and soybean yields
   - Save as `data/raw/usda_yields.csv`

#### Manual download

1. Visit the NOAA CDO web interface and download Illinois data
2. Visit the USDA Quick Stats interface and download crop yield data
3. Place files in `data/raw/` directory

---

## Running the Pipeline

### Automated workflow

Run the data cleaning pipeline with one command:

```bash
cd workflow
./run_all.sh
```

This script will:
1. Check for required raw data files
2. Clean NOAA weather data
3. Clean USDA crop yield data
4. Generate summary statistics

### Running scripts individually

You can also run them one at a time:

```bash
# Download data (if needed)
python scripts/get_noaa_data.py
python scripts/get_usda_data.py

# Clean NOAA data
python scripts/clean_noaa.py

# Clean USDA data
python scripts/clean_usda.py
```

See [`scripts/README.md`](scripts/README.md) for detailed script documentation.

---

## Data Processing Steps

### 1. NOAA Weather Data Cleaning (`clean_noaa.py`)

**Input:** Daily weather observations  
**Output:** County-year aggregated climate metrics

**Processing:**
- Convert temperatures from tenths of °C to actual °C
- Handle missing values
- Aggregate daily data to annual county-level:
  - Mean annual temperature
  - **Temperature volatility** (standard deviation)
  - Annual precipitation totals
  - Max/min temperature statistics

**Key Metric:** Temperature volatility (daily temperature standard deviation) serves as the primary climate variability indicator.

### 2. USDA Crop Yield Cleaning (`clean_usda.py`)

**Input:** County-level annual crop yields  
**Output:** Standardized yield data for corn and soybeans

**Processing:**
- Filter for Illinois counties
- Filter for corn and soybean crops
- Remove suppressed data entries
- Standardize FIPS codes
- Remove unrealistic outliers

## Project Complete

This project has completed all phases of analysis:

**Data Pipeline (Weeks 1-5):**
- Automated data acquisition from NOAA and USDA APIs
- Comprehensive data cleaning and standardization
- Quality assessment and profiling
- Data integration and volatility metric calculation

**Analysis (Weeks 6-8):**
- Statistical regression analysis
- Temporal trend analysis
- Threshold effect testing
- Correlation analysis

**Deliverables (Weeks 9-10):**
- 6 publication-quality visualizations
- Complete Snakemake workflow
- Automated reproducibility pipeline
- Comprehensive documentation
- Data integrity verification (SHA-256 checksums)

**Key Outputs:**
- `integrated.csv` - Final analysis dataset (~10,000+ observations)
- `analysis_results.json` - Complete statistical results
- `data_profile.json` - Data quality assessment
- Multiple visualizations showing yield-volatility relationships

---

## Expected Analysis (Weeks 7-8)

### Statistical Modeling

**Regression Analysis:**
```
yield ~ mean_temp + temp_sd + annual_prcp + county_fixed_effects
```

**Expected findings:**
- Temperature volatility negatively impacts yields
- Optimal temperature ranges for corn vs. soybeans
- Precipitation thresholds for yield declines

### Visualizations

1. **Scatter plots:** Yield vs. temperature volatility
2. **Heat maps:** Geographic patterns of yield changes
3. **Time series:** Long-term trends in climate and productivity
4. **Box plots:** Yield distributions by temperature quartiles

---

## Project Timeline

| Week | Task | Responsible | Status |
|------|------|-------------|--------|
| 1 | Project plan, GitHub setup, test data access | Both | Complete |
| 2-3 | Data acquisition (NOAA & USDA) | Dev (NOAA), Rohit (USDA) | Complete |
| 4-5 | Data cleaning & standardization | Rohit | Complete |
| 6 | Data integration & volatility metrics | Both | Complete |
| 7-8 | Regression analysis & visualizations | Dev | Complete |
| 9-10 | Workflow automation, documentation, reproducibility | Both | Complete |

---

## Reproducibility

This project follows best practices for reproducible research:

- **Version Control:** All code tracked in Git
- **Documentation:** Comprehensive README and inline comments
- **Dependencies:** Explicit version requirements in `requirements.txt`
- **Automated Workflow:** One-command pipeline execution via `run_all.sh`
- **Logging:** Detailed progress tracking in all scripts
- **Modular Design:** Separate scripts for each processing stage

### Reproducing This Analysis

**Quick Start:**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/climate-agriculture-il.git
   cd climate-agriculture-il
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download data from Box:
   - Visit the Box link above
   - Download `data.zip`
   - Extract to project root
   
4. Run the complete pipeline:
   ```bash
   ./workflow/run_all.sh
   ```

5. Or use Snakemake:
   ```bash
   snakemake --cores 4
   ```

**Detailed Instructions:** See `REPRODUCIBILITY.md` for complete step-by-step instructions.

**Verify Results:** Compare your outputs with our checksums:
```bash
python scripts/verify_data.py verify
```

---

## Team Contributions

### Dev Rishi Udata
- NOAA data acquisition and API integration
- Database setup and storage organization
- Workflow automation (`run_all.sh`)
- Documentation and GitHub management

### Rohit Shah
- USDA data acquisition
- Data cleaning and quality assessment
- Statistical modeling and regression analysis
- Visualization development

*Contributions are evident in Git commit history.*

---

## Ethical Considerations

### Data Ethics

- **Public Data:** All datasets are publicly available and in the public domain
- **Proper Attribution:** NOAA and USDA datasets are properly cited
- **No PII:** No personally identifiable information is used
- **Terms of Use:** Compliance with NOAA and USDA data usage policies

### Limitations

- **Causation vs. Correlation:** Results show associations, not definitive causation
- **Confounding Factors:** Yields are influenced by many non-climatic factors (soil, technology, management)
- **Data Completeness:** Weather station coverage varies by county
- **Temporal Alignment:** Daily weather aggregated to annual may lose important seasonal patterns

---

## References

1. NOAA National Centers for Environmental Information. (2024). *Climate Data Online*. https://www.ncdc.noaa.gov/cdo-web/
2. USDA National Agricultural Statistics Service. (2024). *Quick Stats Database*. https://quickstats.nass.usda.gov/
3. Schlenker, W., & Roberts, M. J. (2009). Nonlinear temperature effects indicate severe damages to U.S. crop yields under climate change. *Proceedings of the National Academy of Sciences*, 106(37), 15594-15598.
4. Lobell, D. B., & Field, C. B. (2007). Global scale climate–crop yield relationships and the impacts of recent warming. *Environmental Research Letters*, 2(1), 014002.

---

## Contact

**Project Maintainers:**
- Dev Rishi Udata - [dudata2@illinois.edu](mailto:dudata2@illinois.edu)
- Rohit Shah - [rohitps2@illinois.edu](mailto:rohitps2@illinois.edu)

**Course:** IS477 - Data Lifecycle Management  
**Instructor:** [Instructor Name]  
**Semester:** Fall 2024

---

## License

This project is in the **public domain**. The source data from NOAA and USDA are public domain datasets provided by U.S. government agencies. All code and documentation produced for this project are freely available for use, modification, and distribution.

---

## Acknowledgments

- NOAA National Centers for Environmental Information for providing comprehensive climate data
- USDA National Agricultural Statistics Service for crop yield data
- IS477 teaching staff for guidance and feedback
- University of Illinois at Urbana-Champaign

---

*Last Updated: November 2024 (Weeks 4-5 Development Phase)*

