
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from matplotlib.dates import HourLocator, DateFormatter
from dateutil.parser import ParserError

bitcoin_data = pd.read_csv('bitcoin_data.csv')

bitcoin_data['timestampp'] = pd.to_datetime(bitcoin_data['timestampp'])

# Set 'timestamp' column as index
bitcoin_data.set_index('timestampp', inplace=True)

# Removing duplicate timestamps if any
bitcoin_data = bitcoin_data[~bitcoin_data.index.duplicated(keep='first')]

# Resampling data to hourly frequency and fill missing values
bitcoin_data = bitcoin_data.resample('H').ffill()

# Defining the number of hours for prediction
forecast_hours = 24

model = LinearRegression()

# Extracting features and target variable
X = bitcoin_data.index.to_julian_date().values.reshape(-1, 1)
y = bitcoin_data['closee'].values
model.fit(X, y)

while True:
    input_date = input("Enter a date for prediction (in month/day/year format, e.g., 07-01-2023): ")
    try:
        pd.to_datetime(input_date)  # Check if the input date is valid
        break
    except ParserError:
        print("Invalid date format. Please enter the date in the format 'MM-DD-YYYY'.")

# Making future dataframe for prediction
future_dates = pd.date_range(start=input_date, periods=forecast_hours, freq='H')

# Forecasting future prices
future_dates_julian = future_dates.to_julian_date().values.reshape(-1, 1)
forecast = model.predict(future_dates_julian)

exchange_rate = 83

print("\nPredicted Bitcoin Prices for the Next 24 Hours:")
for date, price in zip(future_dates, forecast):
    price_in_rupees = price * exchange_rate
    print(f"{date}: ${price:.2f} (₹{price_in_rupees:.2f} in rupees)")

plt.figure(figsize=(12, 6))
plt.plot(future_dates, forecast, label='Predicted Prices', linestyle='-', marker='o')
plt.title('Bitcoin Price Prediction for the Next 24 Hours (Linear Regression)')
plt.xlabel('Time')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_locator(HourLocator(interval=1))  # Setting ticks every hour
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))  # Formatting time as HH:MM:SS
plt.tight_layout()
plt.show()
