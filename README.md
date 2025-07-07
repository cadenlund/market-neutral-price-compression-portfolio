# Market Neutral Price Compression Portfolio

This repository contains code and data pipelines to build and evaluate a **market-neutral, factor-based long-short stock strategy** using a custom **price compression alpha factor**.

## How to follow along

A full, formal explanation of the code along with examples and images is available on my [personal website](https://www.cadenlund.com/projects/Long-short-portfolio)

It demonstrates:

- How to set up a database for historical stock data.
- How to create and evaluate an alpha factor.
- How to prepare and store data for backtesting.

## How to Use This Repository

### 1. Clone the repository

Clone this repository and move into its directory:

```
git clone https://github.com/your-username/market-neutral-price-compression-portfolio.git
cd market-neutral-price-compression-portfolio
```

### 2. Set up the Python environment

Install the dependencies using the provided `environment.yml`:

```
conda env create -f environment.yml
conda activate market-neutral
```

Alternatively, you can use `pip` and `requirements.txt` if provided:

```
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the root of the repository with your credentials:

```
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
POLYGON_API_KEY=your_polygon_api_key
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=your_db_host
POSTGRES_PORT=your_db_port
POSTGRES_DB=your_db_name
```

This file is used to securely load API keys and database credentials.

### 4. Build the database

Run the notebook or script that creates the PostgreSQL + TimescaleDB schema and populates it with data from Polygon.io:

- Create the tables (`ticker_metadata` and `ohlcv_data`).
- Download and clean the data.
- Adjust prices for stock splits.
- Store the clean data in the database.

Follow the comments in my blog post step-by-step.\
You’ll need to have a PostgreSQL server running and the TimescaleDB extension enabled.

### 5. Query the database

Use the included `PostgresDataHandler` class to query your database from Python:

```
from dbapi import PostgresDataHandler

handler = PostgresDataHandler(db_uri)
df = handler.get_data(date='2025-04-15', lookback=200, columns=['close'])
```

### 6. Create the alpha factor

Use the provided code to compute the **price compression** factor from price data:

- Compute absolute daily price changes.
- Take rolling standard deviation over a 14-day window.
- Invert the volatility to score stocks with tight price ranges higher.
- Stack into multi-index (date, ticker) format for Alphalens.

### 7. Evaluate the factor

Run the Alphalens workflow:

- Clean the factor and forward returns.
- Generate tearsheets.
- Perform sector (SIC) group analysis if desired.

```
import alphalens as al
factor_data = al.utils.get_clean_factor_and_forward_returns(factor, prices, periods=(1, 2, 3))
al.tears.create_full_tear_sheet(factor_data)
```

## Notes

- Data is sourced from [Polygon.io](https://polygon.io) (REST API + S3).
- The database design and queries assume TimescaleDB is available for efficient time-series storage.
- The `.env` file should never be committed — it contains sensitive information.
- Example queries, plots, and output files can be found in the notebooks.

