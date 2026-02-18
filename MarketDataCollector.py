import logging
from typing import Dict, Any
import requests

class MarketDataCollector:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.data_sources = ['alphavantage', 'quandl']
        logging.basicConfig(level=logging.INFO)

    def fetch_data(self, symbol: str) -> Dict[str, Any]:
        """Fetches real-time market data from multiple sources."""
        data = {}
        try:
            for source in self.data_sources:
                api_key = self.api_keys[source]
                response = requests.get(
                    f"https://api.{source}.com/v1/{symbol}",
                    params={'apikey': api_key}
                )
                if response.status_code == 200:
                    data[source] = response.json()
                else:
                    logging.error(f"Failed to fetch data from {source}: {response.status_code}")
            return data
        except Exception as e:
            logging.error(f"Error fetching market data: {str(e)}")
            raise

    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, float]:
        """Processes raw market data to extract relevant metrics."""
        processed = {}
        try:
            for source in raw_data:
                data = raw_data[source]
                if 'price' in data:
                    processed['price'] = data['price']
                if 'volume' in data:
                    processed['volume'] = data['volume']
            return processed
        except KeyError:
            logging.error("Missing key in data processing")
            raise

    def on_error(self, error: Exception) -> None:
        """Handles errors during data collection."""
        logging.error(f"MarketDataCollector encountered an error: {str(error)}")