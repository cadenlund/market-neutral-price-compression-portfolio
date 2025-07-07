# Market Neutral Price Compression Portfolio

This repository contains code and data pipelines to build and evaluate a **market-neutral, factor-based long-short stock strategy** using a custom **price compression alpha factor**.

## How to follow along

A full, formal explanation of the code along with examples and images is available on my [personal website](https://www.cadenlund.com/projects/market-neutral-price-compression-portfolio)

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

- Create the tables (`ticker_metadata` and `ohlcv_data`) with the schema defined in the db folder.
- Download and clean the data.
- Adjust prices for stock splits.
- Store the clean data in the database.

Follow the comments in my blog post step-by-step.\
You’ll need to have a PostgreSQL server running and the TimescaleDB extension enabled.

### 5. Query, download, and clean the data

Start with the notebook `notebooks/data_ingestion_and_cleaning.ipynb`.\
This notebook demonstrates how to:

- Download data from [Polygon.io](https://polygon.io) (REST API + S3).
- Clean and prepare the raw data (null values and stock splits)
- Store the cleaned data into a TimescaleDB database for efficient querying.

```python
from dbapi import PostgresDataHandler

handler = PostgresDataHandler(db_uri)
df = handler.get_data(date='2025-04-15', lookback=200, columns=['close'])
```

You’ll see the full ingestion pipeline: from fetching the raw data to cleaning and loading it into the database.

### 6. Create and analyze the alpha factor

Next, move to `notebooks/Alpha_factor_analysis_and_portfolio.ipynb`.\
This notebook shows how to use the `PostgresDataHandler` to load clean price data from the database and perform analysis:

- Use the included `PostgresDataHandler` class (implemented in `src/dbapi.py`) to query your database from Python.
- Calculate the **price compression** alpha factor:
  - Compute absolute daily price changes.
  - Take rolling standard deviation over a 14-day window.
  - Invert the volatility to score stocks with tighter price ranges higher.
  - Stack into multi-index `(date, ticker)` format for Alphalens.
- Evaluate the factor:
  - Clean the factor and forward returns.
  - Generate Alphalens tearsheets.
  - Optionally, perform SIC (sector) group analysis.

```python
import alphalens as al

factor_data = al.utils.get_clean_factor_and_forward_returns(
    factor, prices, periods=(1, 2, 3)
)
al.tears.create_full_tear_sheet(factor_data)
```

### Notes

- The ingestion notebook downloads, cleans, and stores data in TimescaleDB.
- The `PostgresDataHandler` API is located in `src/dbapi.py`.
- Data is sourced from [Polygon.io](https://polygon.io) (REST API + S3).
- The `.env` file should never be committed — it contains sensitive information.
- The notebooks folder contains example queries, plots, and output files.
- For a full explanation of the methodology and results, visit the [project website](https://your-website-link.com).




