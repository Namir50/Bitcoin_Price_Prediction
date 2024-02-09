use mydatabase;

CREATE TABLE bitcoin_data (
    timestampp DATE,
    openn FLOAT,
    highh FLOAT,
    loww FLOAT,
    closee FLOAT,
    volume FLOAT,
    quote_asset_volume FLOAT,
    number_of_trades INT,
    taker_buy_base_asset_volume FLOAT,
    taker_buy_quote_asset_volume FLOAT
);

BULK INSERT bitcoin_data
FROM "C:\\Users\\namir\\Downloads\\bitcoin data\\bitcoin_2017_to_2023.csv"
WITH (
    FIELDTERMINATOR = ',',  
    ROWTERMINATOR = '\n',    
    FIRSTROW = 2

);

Select  *from bitcoin_data 
DELETE FROM bitcoin_data
WHERE YEAR(timestampp) BETWEEN 2017 AND 2021;





