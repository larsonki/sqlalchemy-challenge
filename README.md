# Climate Analysis

## In a two-part project, perform a climate analysis of Honolulu, Hawaii.

### Part One: Using Python, SQLAlchemy, Pandas and Matplotlib, perform a basic analysis and data exploration of the provided climate database which includes data on precipitation as well as the weather stations on the island.

**Precipitation Analysis:**

- Find the most recent date in the dataset.
- Using this date, retrieve the previous 12 months of precipitation data by querying the 12 previous months of data. Note: Do not pass in the date as a variable to your query.
- Select only the date and prcp values.
- Load the query results into a Pandas DataFrame, and set the index to the date column.
- Sort the DataFrame values by date.
- Plot the results by using the DataFrame plot method.
- Use Pandas to print the summary statistics for the precipitation data.

**Station Analysis:**

- Design a query to calculate the total number of stations in the dataset.
- Design a query to find the most active stations (the stations with the most rows).
  - List the stations and observation counts in descending order.
  - Which station id has the highest number of observations?
  - Using the most active station id, calculate the lowest, highest, and average temperatures.
- Design a query to retrieve the previous 12 months of temperature observation data (TOBS).
  - Filter by the station with the highest number of observations.
  - Query the previous 12 months of temperature observation data for this station.
  - Plot the results as a histogram with bins=12.
  - Close out your session.


