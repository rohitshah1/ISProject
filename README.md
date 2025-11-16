# Climate Variability and Agricultural Productivity in Illinois

A reproducible data analysis project examining the relationship between climate variability and crop yields in Illinois.

**Course:** IS477 - Data Lifecycle  
**Authors:** Dev Rishi Udata, Rohit Shah  
**Institution:** University of Illinois at Urbana-Champaign

**Status:** Weeks 4-5 Checkpoint - Data Cleaning Phase Complete

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
│   ├── raw/                  # Original data (not committed to Git)
│   │   ├── noaa_full.csv
│   │   └── usda_yields.csv
│   ├── processed/            # Cleaned data (not committed to Git)
│   │   ├── noaa_clean.csv
│   │   └── usda_clean.csv
│   └── metadata/             # Data dictionaries, schema documentation
│
├── scripts/
│   ├── get_noaa_data.py      # NOAA data acquisition
│   ├── get_usda_data.py      # USDA data acquisition
│   ├── clean_noaa.py         # NOAA weather data cleaning
│   ├── clean_usda.py         # USDA crop yield data cleaning
│   └── README.md             # Scripts documentation
│
├── workflow/
│   └── run_all.sh            # Automated cleaning workflow
│
├── docs/
│   ├── ProjectPlan.md        # Original project proposal
│   └── StatusReport.md       # Progress updates (Milestone 3)
│
├── results/                  # For future analysis outputs
│
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── config.py                # API configuration
└── README.md                # This file
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

## Current Status (Weeks 4-5 Complete)

As of this checkpoint, we have completed:

**Weeks 1-3:**
- Project planning and design
- GitHub repository setup
- API access configuration
- Data acquisition scripts for NOAA and USDA

**Weeks 4-5 (Current):**
- NOAA weather data cleaning and aggregation
- USDA crop yield data standardization
- Data quality assessment
- Documentation of cleaning procedures

**Cleaned Datasets:**
- `noaa_clean.csv` - County-year aggregated weather metrics
- `usda_clean.csv` - Standardized corn and soybean yields

**Next Steps (Week 6+):**
- Integrate NOAA and USDA datasets
- Calculate temperature volatility metrics
- Prepare data for statistical analysis
- Begin exploratory data analysis

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
| **4-5** | **Data cleaning & standardization** | **Rohit** | **Complete** |
| 6 | Data integration & volatility metrics | Both | Not Started |
| 7-8 | Regression analysis & visualizations | Dev | Not Started |
| 9-10 | Workflow automation, documentation, reproducibility | Both | Not Started |

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

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Place raw data in `data/raw/`
4. Run: `./workflow/run_all.sh`
5. Results will be in `data/processed/integrated.csv`

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

