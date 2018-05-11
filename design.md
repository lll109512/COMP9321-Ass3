## Comprehensive Statistical Data of Australian Universities (CSDAU) Design Documentation

<center>Group: CharStarport</center>


### Introduction

CSDAU is a system which can acquire data from specified data source; analyze and integrate them together, and then publish via website app.

### Data source

Three source data were required by CSDAU:

1. Research income and HDR completion: obtained from [Australian Federal Government Public Datasets](https://data.gov.au/)

2. Undergraduate applications offers and acceptance: source same above

3. World university ranking: obtained from [Kaggle Datasets](https://www.kaggle.com/datasets)

### Architecture

#### Data Analytics Module

In this module, source data could be provided manually in file, or by given URL.  All raw datasets will be saved in /data, specified analyse program will read them, and store all useful data in database(MySQL).  This part will access both raw data and system database.

#### Data Publication Module

After the previous module finished analysing and storing all necessary data, all data could be accessed by data publication API of this module.

#### Web App Module

Publication module could provide all data via API, but that is not easy to use for non-professional users.  Web app could provide a clear UI, which is easy to use for everyone.  It could also provide some features like comparison and so on.
