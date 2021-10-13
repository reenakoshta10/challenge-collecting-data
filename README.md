# WEB SCRAPING
### Get ready to collecting data from [ImmoWeb](https://www.immoweb.be/en) which is the most popular real estate website in Belgium? 🇧🇪 

![giphy](https://user-images.githubusercontent.com/46165841/137090779-60aef350-2a88-4158-89e5-af1cabcc395f.gif)

## 

The main mission of the project is creating a dataset for a machine learning model to make a price predictions on real estatse sales in Belgium.
Our dataset holds the following columns:

- Locality
- Type of property (House/apartment)
- Subtype of property (Bungalow, Chalet, Mansion, ...)
- Price
- Type of sale (Exclusion of life sales)
- Number of rooms
- Area
- Fully equipped kitchen (Yes/No)
- Furnished (Yes/No)
- Open fire (Yes/No)
- Terrace (Yes/No)
  - If yes: Area
- Garden (Yes/No)
  - If yes: Area
- Surface of the land
- Surface area of the plot of land
- Number of facades
- Swimming pool (Yes/No)
- State of the building (New, to be renovated, ...)

All these datasets are saved in ```property_data.csv``` file.


## Collaborators

Design and construction phase of the project was made by 4 collaborators.([Ujjwal Kandel](https://github.com/UjjwalKandel2000), [Reena Koshta](https://github.com/reenakoshta10), [Nichelle Pinto Machado](https://github.com/N1chelle),  [Yusuf Akcakaya](https://github.com/yusufakcakaya))


## Installation

- Pull requests are welcome.
- or ```git clone https://github.com/UjjwalKandel2000/challenge-collecting-data.git```

## Repo Architecture 

```
challenge-collecting-data
│
│   README.md          :explains the project
│   main.py            :Python script file necessary to initialize the project
│   property_data.csv  :keeps all data for properties
│   
│__   
│   driver             :directory contains chromedriver
│   │
│   │ chromedriver     :is a standalone server or a separate executable that is used by Selenium WebDriver to control Chrome.
│__ 
│   immo_scraping      :directory contains web_scraping.py
│   │
│   │ web_scraping.py  :Python script file for web scraping
│   

```

## Visuals
.
.
.
.


## Timeline

- Repository: `challenge-collecting-data`
- Type of Challenge: `Consolidation`
- Duration: `3 days`
- Deadline: `13/10/2021 16:30`
- Team challenge : 3

## Good Luck!
