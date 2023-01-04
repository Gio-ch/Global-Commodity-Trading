# Global Commodity Trading statistics Dashboard

## Instructions for running: Macos

```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cd dashboard
python index.py
```

# Explanation
### Dataset used
https://www.kaggle.com/datasets/unitednations/globalcommodity-trade-statistics
## Objectives
• Create a multi page, interactive dashboard analysing global commodity trade statistics

## There are three main charts on page 1,
First chart allows comparison of Import and Emport(Total USD traded) for selected country(dropdown) and a range of years(slider).The Second chart displays the top 15 commodities traded for the selected filters. 
The charts allow additional interaction by means of radio buttons. On the left replacing the initial chart with a comparison of total import and export traded over whole selected period. On the right option to switch to a pie chart displaying same information(commodities which were traded with highest frequency).

## Page 2

Page two contains three charts, analysing evolution of total traded value. 
1.The table shows the total traded value for each country for the selected years and absolute change between the two years. Table is sorted by the absolute change. In case of nonexistent data for selected years, the value from the closest available date is displayed.
2. The line shows the evolution of traded commodities for top 15 areas
3. The choropleth shows the value of traded commodities over years for all countries.

## Values have been adjusted to correct for inflation

