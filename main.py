from src import NewsAPI, NewsToQdrant
from datetime import datetime, timedelta
from src.utils.load_configs import Config
from src.utils import logger as log
from qdrant_client import QdrantClient
from qdrant_client.http import models
import argparse

conf = Config()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Date Parameters.")
    parser.add_argument("--date",
                        type=str,
                        default=datetime.strftime(
                            datetime.now(),
                            "%Y-%m-%d"
                        ), 
                        help="Number of Orders.")
    args = parser.parse_args()
    log.LOG_MAIN.info("Main Flow Started")
    dt_now = datetime.strptime(args.date, "%Y-%m-%d") - timedelta(days = 1)
    start = dt_now.strftime("%Y-%m-%dT00:00:00Z")
    end = dt_now.strftime("%Y-%m-%dT23:00:00Z")
    news_api = NewsAPI("data/news",
                       conf,
                       start,
                       end)
    news_api.fetch_api_data()
    news_api.save_data()
    log.LOG_MAIN.info("Checking Production Collection Availability")
    client = QdrantClient(url = conf.env["QDRANT_URL"], location="data/db/", timeout=100,)
    available_collections=client.get_collections()
    available_collections = [item.name for item in available_collections.collections]
    if "prod" not in available_collections:
        client.create_collection(
            collection_name = "prod",
            vectors_config=models.VectorParams(
            size = conf.conf["vector_size"],
            distance=models.Distance.COSINE,
            ),
            quantization_config=models.ProductQuantization(
            product=models.ProductQuantizationConfig(
                compression=models.CompressionRatio.X16,
                always_ram=True,
            ),
        ),
        on_disk_payload=True,
        timeout=100
        )
    qdrant_loader = NewsToQdrant(
        qdrant_client=client,
        data_path="data/news",
        filename=f"news_{dt_now.strftime('%Y-%m-%d')}.json",
        config=conf,
    )
    qdrant_loader.embed_collection_point()
    log.LOG_MAIN.info("Main Flow Finished Successfully")