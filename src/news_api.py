import json
import requests
from datetime import datetime
from src.utils import NewsData, Config
from src.utils import logger as log
from typing import List, Dict, Any

class NewsAPI:
    def __init__(self, 
                 news_storage_path: str, 
                 config: Config, 
                 start_date, 
                 end_date, 
                 category="general"
    ) -> None:
        self.news_storage_path = news_storage_path
        self.start_date = start_date
        self.end_date = end_date
        self.url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=ar&country=eg&max={config.conf['n_requests']}&from={start_date}&to={end_date}&apikey={config.env['GNEWAPI']}"
    @staticmethod
    def good_data(fetched_data: List[Dict[str, Any]]):
        log.LOG_GET.info("Checking Data")
        for data in fetched_data:
            try:
                data = NewsData(**data)
            except Exception as exp:
                log.LOG_GET.error(f"Error When Validating the Data: {exp}")
                fetched_data.remove(data)
        return fetched_data
        
    def fetch_api_data(self):
        log.LOG_GET.info(f"Fetch News Data From API between {self.start_date} and {self.end_date}")
        response = requests.get(self.url)
        if response.status_code == 200:
            news_json = response.json()
            articles = NewsAPI.good_data(news_json["articles"])
            news_json["articles"] = articles
            self.news_json = news_json
            log.LOG_GET.info("Data Fetched Successfully")
        else:
            log.LOG_GET.error(f"Error when Fetching the Data with status code: {response.status_code}")
    def save_data(self):
        dt_now = datetime.strftime(
            datetime.strptime(self.start_date, "%Y-%m-%dT%H:%M:%SZ"),
            "%Y-%m-%d"
        )
        log.LOG_GET.info("Saving Data to Destination Path")
        with open(
            f"{self.news_storage_path}/news_{dt_now}.json",
            mode = "w", 
            encoding = "utf-8"
            ) as js:
            json.dump(
                self.news_json,
                js,
                ensure_ascii=False,
                indent=4
            )
        log.LOG_GET.info("News Data Saved Successfully")

        
        
        
