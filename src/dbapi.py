import pandas as pd
import psycopg2 # PostgreSQL database adapter for Python
from psycopg2.extras import RealDictCursor # Allows us to get the results as a dictionary
from datetime import timedelta 

class PostgresDataHandler:
  def __init__(self, db_uri):
      self.conn = psycopg2.connect(db_uri, cursor_factory=RealDictCursor)  # Connect to DB

  def get_data(self, tickers=None, date=None, lookback=30, freq="daily", columns=['close']):
      """
      Query daily OHLCV data for one or more tickers over a lookback period ending on a specific date.
  
      Args:
          tickers (list or None): List of tickers, or None to fetch all.
          date (str): Last date of the lookback period (YYYY-MM-DD). Required.
          lookback (int): Number of days before `date` to fetch.
          freq (str): Only 'daily' is supported for now.
          columns (list): List of columns to retrieve.
  
      Returns:
          pd.DataFrame: Pivoted DataFrame (if one column) or tidy format (if multiple).
      """
      if date is None:
          raise ValueError("You must supply a `date` for get_data().")
  
      if freq != "daily":
          raise ValueError("Only daily frequency is supported.")
  
      end_date = pd.to_datetime(date)
      start_date = end_date - timedelta(days=lookback)
  
      selected_cols = ', '.join(['time', 'ticker'] + columns) # Columns to select in SQL query
  
      if tickers is None: # If no tickers specified, fetch all
          sql = f"""
          SELECT {selected_cols}
          FROM ohlcv_data
          WHERE time BETWEEN %s AND %s
          ORDER BY time
          """
          params = (start_date, end_date)
      else: # Fetch only specified tickers
          sql = f"""
          SELECT {selected_cols}
          FROM ohlcv_data
          WHERE ticker = ANY(%s)
            AND time BETWEEN %s AND %s
          ORDER BY time
          """
          params = (tickers, start_date, end_date)
  
      with self.conn.cursor() as cur: # Execute the SQL query
          cur.execute(sql, params) 
          rows = cur.fetchall() # Fetch all results
  
      df = pd.DataFrame(rows) # Convert results to DataFrame
  
      if df.empty: 
          return df # Return empty DataFrame if no results
  
      df['date'] = pd.to_datetime(df['time'], utc=True) # Convert 'time' to datetime
  
      if len(columns) == 1: # If only one column, pivot the DataFrame
          return df.pivot(index='date', columns='ticker', values=columns[0])
      else: # If multiple columns, return tidy format
          return df

  def get_sic_codes(self):
      """
      Retrieve a dictionary mapping each ticker to its SIC code.

      Returns:
          dict: { ticker: sic_code }
      """
      sql = "SELECT ticker, sic_code FROM ticker_metadata" # SQL query to fetch ticker and sic_code
      with self.conn.cursor() as cur: # Execute the SQL query
          cur.execute(sql) 
          rows = cur.fetchall() # Fetch all results
      # rows are dicts thanks to RealDictCursor
      return {row['ticker']: row['sic_code'] for row in rows} # Convert results to dictionary

  def close(self): # Close the database connection
      self.conn.close()