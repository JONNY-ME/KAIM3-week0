# Data Analysis Report

## Introduction
This report outlines the data analysis workflow implemented in the notebook. It leverages Python libraries such as NumPy, Pandas, Matplotlib, Seaborn, and Windrose to load, clean, analyze, and visualize solar irradiance and meteorological data from three distinct locations:

- **Benin Malanville**
- **Sierra Leone Bumubuna**
- **Togo Dapaong**

The objective is to gain insights into patterns in solar radiation, wind conditions, and temperature trends, alongside ensuring data quality and consistency.

---

## Data Loading
The notebook starts by loading data from three CSV files. Each dataset represents a location's solar irradiance and meteorological readings. The datasets contain:

- 525,600 rows
- 19 columns

The initial exploration of the datasets involves inspecting the first few rows using `.head()` and examining their shapes to confirm structure and size.

---

## Data Exploration
### Column Categorization
Columns were categorized as numerical or categorical based on their data types. Initially, the **Timestamp** and **Comment** columns were classified as categorical, but further inspection revealed:

- **Timestamp** is a numerical column (date format).
- **Comment** lacks values and was removed.

### Summary Statistics
Using the `.describe()` method, the notebook computed summary statistics for numerical columns, including mean, standard deviation, and percentiles. Key observations include:

1. **Central Tendency and Distribution**: Symmetry in most variables suggests a balanced distribution.
2. **High Variability**: Solar metrics like GHI, DNI, and module outputs show significant fluctuations.
3. **Potential Anomalies**: Negative irradiance values indicate sensor errors or nighttime recording.

---

## Data Quality Check
A missing values check identified 525,600 missing values in the **Comments** column across all datasets, while other columns had no missing values.

---

## Outlier Detection and Removal
Outliers were detected using boxplots. Valid ranges for key variables (e.g., GHI, DNI, DHI) were defined, and values outside these ranges were clipped. The effectiveness of this approach was demonstrated by comparing pre- and post-clipping boxplots.

---

## Time Series Analysis
Time series line plots were generated for variables such as GHI, DNI, and ambient temperature (Tamb). The **Timestamp** column was converted to datetime format to enable monthly trend analysis. Observations include:

- Seasonal variations in solar radiation.
- Temperature trends correlating with radiation levels.

---

## Correlation Analysis
### Solar Radiation
Correlation heatmaps revealed strong positive correlations between:

- GHI and DNI
- GHI and DHI

### Module Temperatures
High correlations (0.8-0.99) were observed between TModA and TModB, indicating consistency in module behavior.

### Wind Conditions
Scatter plots were used to analyze relationships between wind speed (WS), wind gusts (WSgust), and wind direction (WD).

---

## Wind Analysis
Windrose plots visualized wind patterns for each location, highlighting:

1. **Sierra Leone Bumubuna**: Consistent wind direction, favoring wind energy production.
2. **Benin Malanville and Togo Dapaong**: Variable wind directions suggest diverse weather conditions and complex turbine placement.

---

## Temperature Analysis
The relationship between temperature and relative humidity was examined using scatter plots. Correlation heatmaps further detailed interactions between:

- Tamb and RH
- Module temperatures (TModA, TModB)

---

## Histogram Analysis
Histograms were created for variables such as GHI, DNI, and WS, revealing:

- Distribution characteristics.
- Insights into typical and extreme values.

---

## Conclusion
The notebook effectively explores solar irradiance and meteorological data, providing:

- Clear visualization of trends and patterns.
- Robust outlier detection and removal techniques.
- Actionable insights into energy production and environmental planning.

This workflow offers a comprehensive framework for analyzing large-scale environmental datasets.

