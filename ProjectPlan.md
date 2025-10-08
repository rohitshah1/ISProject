Overview 
This project examines the relationship between climate variability and agricultural productivity in Illinois, focusing on corn and soybean yields. Agriculture is a cornerstone of Illinois’s economy, and both crops are highly sensitive to environmental conditions such as temperature, rainfall, and extreme weather events. By integrating historical weather data with agricultural yield data, the project will explore how fluctuations in climate patterns influence crop productivity. 
The overall goal is to design a reproducible, end-to-end data workflow that ingests raw data from multiple sources, integrates them into a unified schema, and analyzes the impact of temperature volatility on agricultural yields. The project also seeks to demonstrate data lifecycle management practices, ethical data use, and transparent documentation. 
Research Questions 
1. How does year-to-year temperature volatility impact corn and soybean yields in Illinois counties? 
2. Are there identifiable thresholds in temperature or precipitation beyond which yields significantly decline? 
3. Can long-term climate patterns (e.g., increasing average summer temperatures) be statistically linked to changes in productivity trends? 
Team 
Team Members: 
● Dev Rishi Udata 
● Rohit Shah 
Roles and Responsibilities: 
● Dev Rishi Udata ○ Dataset acquisition (NOAA weather data). 
○ Storage and organization (relational database setup). 
○ Workflow automation and reproducibility 
○ Markdown documentation and GitHub repository management. 
● Rohit Shah ○ Dataset acquisition (USDA crop yield data). 
○ Data cleaning, quality assessment, and integration of both datasets. 
○ Statistical modeling and regression analysis. 
○ Visualization of findings 
Both team members will contribute to project design, writing, and final report preparation. Contributions will be evident in the GitHub commit history. 
Data Sets 
This project will use two distinct datasets from reputable sources. The first is the NOAA Climate Data provided by the National Centers for Environmental Information, which contains daily weather observations such as temperature, precipitation, and humidity from Illinois weather stations. This dataset, available in CSV format or via API queries, is structured in a tabular format and will provide granular indicators to measure climate volatility and long-term trends. While it is highly relevant, the dataset is large, may contain missing values, and will require aggregation to the county and year level. The second dataset is the USDA Crop Yield Data from the National Agricultural Statistics Service (NASS Quick Stats), which reports county-level annual corn and soybean yields measured in bushels per acre. This dataset, also available through CSV exports and structured in a tabular format, serves as the outcome variable to be analyzed against climate conditions. Its constraints include variable coverage by county and year as well as the influence of non-climatic factors on yields. Together, the NOAA and USDA datasets satisfy the project requirement of using two trustworthy, distinct data sources with different schemas and access methods, allowing for meaningful integration and analysis. 


When it comes to a timeline, we are essentially divided into 9-10 weeks. The first week will be finalizing a project plan, having our GIT repository set up and even test our access to the dataset with the ability to obtain the sample files from the data. The people responsible are both of us. The next one is week 2-3 where we will collect a complete NOAA and USDA dataset with documents of the metadata and initial schema, I will work on NOAA, Dev will work on USDA. Weeks 4-5 will be working towards cleaning and standardizing the dataset such as handling the missing data, helping with aligning any country codes, etc and I think this is a one person job rohit can take care of. In week 6, we need to start with the integration of datasets by the country and year and then start the computation of volatility metrics like temperature variance and even standard deviation for some metrics. This will be done by rohit and dev together. Week 7-8 will be about performing the regression and looking into trend  analysis. This will allow us to generate multiple visualizations and even help us determine the results and this can be done by dev. Weeks 9-10 will work towards automating workflow, and helping finalize any documentation. We also will work toward the reproducibility testing and even uploading all our files to the results. This will be worked on by both rohit and dev. 

When it comes to the constraints, there could be some when it comes to data completeness. NOAA weather station coverage varies greatly by each county and the aggregation might be needed for interpolation. Temporal alignment could also be a problem and this is the fact that crop data are annual while the weather data is a daily thing so aggregation strategy must be consistent and this could lead to future problems. There is also worry when it comes to computational load, the NOAA API request may need batching or caching to handle large time spans. There are ethical legal worries as well. All datasets are public domains but have some proper citation and adherence to NOAA/USDA data usage terms.

When it comes to gaps/areas needing more input, we need a better understanding of the definition of temperature volatility with monthly vs seasonal standard deviation and there is potential for inclusion of additional climate indicators such as rainfall and even drought index. We will also need guidance from TAs on the best way for the overall workflow automation such as Makefile or snakemake. 

Our expected outcomes for this project include a quantitative analysis of how temperature variability impacts corn and soybean yields in Illinois. Visualization of the geographic and temporal patterns in yield response to volatility along with a reproducible data workflow and documentation which can be reused for similar climate agriculture studies. 
