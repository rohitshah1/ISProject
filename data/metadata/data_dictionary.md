# Data Dictionary

This document describes the schema and variables for all datasets in the Climate Variability and Agricultural Productivity project.

---

## Raw Data

### NOAA Climate Data (`data/raw/noaa_full.csv`)

Daily weather observations from Illinois weather stations.

| Column | Type | Description | Units | Example |
|--------|------|-------------|-------|---------|
| `date` | date | Observation date | YYYY-MM-DD | 2020-07-15 |
| `station` | string | Weather station ID | - | GHCND:USC00110338 |
| `county_fips` | string | County FIPS code | 5-digit | 17019 |
| `tmax` | integer | Maximum temperature | tenths of °C | 325 (32.5°C) |
| `tmin` | integer | Minimum temperature | tenths of °C | 185 (18.5°C) |
| `tavg` | integer | Average temperature | tenths of °C | 255 (25.5°C) |
| `prcp` | integer | Precipitation | tenths of mm | 52 (5.2 mm) |

**Notes:**
- Temperature values stored as integers representing tenths of degrees Celsius
- Precipitation stored as tenths of millimeters
- Missing values may be present for some stations/dates
- Multiple stations may exist per county

**Source:** NOAA National Centers for Environmental Information  
**License:** Public domain  
**Last Updated:** November 2024

---

### USDA Crop Yields (`data/raw/usda_yields.csv`)

Annual county-level crop yield data for Illinois.

| Column | Type | Description | Units | Example |
|--------|------|-------------|-------|---------|
| `Year` | integer | Harvest year | year | 2020 |
| `State` | string | State name | - | ILLINOIS |
| `State ANSI` | integer | State FIPS code | 2-digit | 17 |
| `County` | string | County name | - | CHAMPAIGN |
| `County ANSI` | integer | County ANSI code | 3-digit | 19 |
| `Commodity` | string | Crop type | - | CORN |
| `Data Item` | string | Measurement description | - | CORN, GRAIN - YIELD, MEASURED IN BU / ACRE |
| `Value` | mixed | Yield value | bu/acre | 195.5 or "(D)" |

**Notes:**
- `Value` may contain "(D)" for suppressed data to protect privacy
- Common commodities: "CORN", "CORN, GRAIN", "SOYBEANS", "SOYBEANS, ALL"
- Column names may vary depending on Quick Stats export settings

**Source:** USDA National Agricultural Statistics Service  
**License:** Public domain  
**Last Updated:** November 2024

---

## Processed Data

### Cleaned NOAA Data (`data/processed/noaa_clean.csv`)

County-year aggregated weather data.

| Column | Type | Description | Units | Range |
|--------|------|-------------|-------|-------|
| `county_fips` | string | 5-digit county FIPS code | - | 17001-17203 |
| `year` | integer | Year | year | 1990-2024 |
| `mean_temp` | float | Annual mean temperature | °C | 5-20 |
| `temp_sd` | float | Temperature volatility (std dev) | °C | 5-15 |
| `mean_tmax` | float | Mean maximum temperature | °C | 10-30 |
| `mean_tmin` | float | Mean minimum temperature | °C | 0-15 |
| `annual_prcp` | float | Total annual precipitation | mm | 500-1500 |
| `mean_daily_prcp` | float | Mean daily precipitation | mm | 1-5 |

**Aggregation Method:**
- Daily observations aggregated to annual county level
- `temp_sd` calculated as standard deviation of daily average temperatures within each county-year
- Missing values in original data excluded from calculations

**Data Quality:**
- ~102 counties in Illinois (some merged/changed over time)
- Typical coverage: 1990-present
- Counties with insufficient weather station coverage may be excluded

---

### Cleaned USDA Data (`data/processed/usda_clean.csv`)

Standardized crop yield data.

| Column | Type | Description | Units | Range |
|--------|------|-------------|-------|-------|
| `year` | integer | Harvest year | year | 1990-2024 |
| `county_fips` | string | 5-digit county FIPS code | - | 17001-17203 |
| `county_name` | string | County name | - | CHAMPAIGN |
| `commodity` | string | Standardized crop name | - | CORN, SOYBEANS |
| `yield` | float | Crop yield | bu/acre | 50-250 |

**Standardization:**
- Commodity names normalized: "CORN, GRAIN" → "CORN", "SOYBEANS, ALL" → "SOYBEANS"
- County FIPS codes padded to 5 digits
- Suppressed values "(D)" removed
- Unrealistic yields (< 0 or > 500 bu/acre) filtered out

**Data Quality:**
- Not all counties grow both corn and soybeans
- Some county-years may have missing data
- Typical corn yields: 100-200 bu/acre
- Typical soybean yields: 40-70 bu/acre

---

### Integrated Dataset (`data/processed/integrated.csv`)

Final analysis-ready dataset merging climate and yield data.

| Column | Type | Description | Units | Notes |
|--------|------|-------------|-------|-------|
| `county_fips` | string | County identifier | - | Primary key with year |
| `county_name` | string | County name | - | Optional |
| `year` | integer | Year | year | Primary key with county |
| `commodity` | string | Crop type | - | CORN or SOYBEANS |
| `yield` | float | Crop yield | bu/acre | Outcome variable |
| `mean_temp` | float | Annual mean temperature | °C | Predictor |
| `temp_sd` | float | Temperature volatility | °C | **Key predictor** |
| `mean_tmax` | float | Mean max temperature | °C | Predictor |
| `mean_tmin` | float | Mean min temperature | °C | Predictor |
| `annual_prcp` | float | Total precipitation | mm | Predictor |
| `mean_daily_prcp` | float | Mean daily precipitation | mm | Predictor |

**Integration Method:**
- Inner join on `county_fips` and `year`
- Only county-year combinations present in both datasets are retained
- Separate rows for corn and soybeans in same county-year

**Expected Size:**
- Approximately 10,000-20,000 observations
- Depends on overlap between NOAA and USDA coverage
- Covers ~30-35 years × ~100 counties × 2 crops

**Use Cases:**
- Regression analysis: `yield ~ mean_temp + temp_sd + annual_prcp`
- Time series analysis: trends over years
- Spatial analysis: county-level patterns
- Crop comparison: corn vs. soybeans response to climate

---

## Variable Definitions

### Temperature Volatility (`temp_sd`)

**Definition:** Standard deviation of daily average temperatures within a county-year.

**Calculation:**
```python
temp_sd = daily_temps.groupby(['county', 'year'])['tavg'].std()
```

**Interpretation:**
- Higher values indicate more variable/volatile temperatures
- Lower values indicate more stable temperatures throughout the year
- Captures intra-annual temperature variability

**Expected Impact on Yields:**
- Hypothesis: Higher volatility → lower yields
- Extreme temperature swings stress crops
- Different crops may have different sensitivities

### Yield (`yield`)

**Definition:** Average production per unit area.

**Units:** Bushels per acre (bu/acre)

**Typical Ranges:**
- **Corn:** 50-250 bu/acre
  - Poor year: < 100 bu/acre
  - Average: 150-180 bu/acre
  - Excellent: > 200 bu/acre
- **Soybeans:** 20-80 bu/acre
  - Poor year: < 40 bu/acre
  - Average: 50-60 bu/acre
  - Excellent: > 70 bu/acre

**Factors Affecting Yield:**
- Climate (temperature, precipitation)
- Soil quality
- Farming practices
- Technology (seeds, equipment)
- Pests and diseases

---

## FIPS Codes

**FIPS (Federal Information Processing Standards) Codes** are unique identifiers for U.S. counties.

**Format:** 5 digits = 2-digit state code + 3-digit county code

**Illinois State Code:** 17

**Examples:**
- 17001 = Adams County, Illinois
- 17019 = Champaign County, Illinois
- 17031 = Cook County, Illinois
- 17113 = McLean County, Illinois

**Reference:** [Illinois County FIPS Codes](https://www.census.gov/library/reference/code-lists/ansi.html)

---

## Data Quality Notes

### Missing Data

**NOAA Weather Data:**
- Some weather stations have gaps in coverage
- Not all counties have weather stations
- Rural counties may have less complete data
- Solution: Counties with insufficient data excluded from final dataset

**USDA Yield Data:**
- Some county-year combinations have suppressed data "(D)"
- Not all counties grow all crops
- Minor crops may not be reported
- Solution: Focus on major crops (corn, soybeans) with better coverage

### Outliers

**Temperature Outliers:**
- Rare extreme readings may indicate sensor errors
- Generally retained if plausible for Illinois climate
- Illinois temperatures: -30°C to 40°C typical range

**Yield Outliers:**
- Values < 0 or > 500 bu/acre filtered as data errors
- Very high yields (> 250 bu/acre corn) may be legitimate record years
- Very low yields (< 20 bu/acre) may indicate crop failure

### Temporal Coverage

**Complete Coverage:** ~1990-2020 (30 years)
- Both NOAA and USDA data available
- Good for trend analysis

**Partial Coverage:** 2021-present
- Recent years may have incomplete data
- USDA data may be preliminary

---

## Conversion Factors

### Temperature

- Celsius to Fahrenheit: °F = (°C × 9/5) + 32
- Fahrenheit to Celsius: °C = (°F - 32) × 5/9
- NOAA storage: tenths of °C (divide by 10)

### Precipitation

- NOAA storage: tenths of mm (divide by 10)
- mm to inches: inches = mm / 25.4
- inches to mm: mm = inches × 25.4

### Area

- 1 acre = 0.405 hectares
- 1 hectare = 2.471 acres

### Yield

- Corn: 1 bu/acre ≈ 0.0628 tonnes/hectare
- Soybeans: 1 bu/acre ≈ 0.0673 tonnes/hectare

---

## Citations

When using this data, please cite:

**NOAA Data:**
> NOAA National Centers for Environmental Information. Climate Data Online. Accessed [Date]. https://www.ncdc.noaa.gov/cdo-web/

**USDA Data:**
> USDA National Agricultural Statistics Service. Quick Stats Database. Accessed [Date]. https://quickstats.nass.usda.gov/

**This Project:**
> Udata, D. R., & Shah, R. (2024). Climate Variability and Agricultural Productivity in Illinois. IS477 Data Lifecycle Project, University of Illinois at Urbana-Champaign.

---

*Last Updated: November 2024*  
*Contact: dudata2@illinois.edu, rohitps2@illinois.edu*

