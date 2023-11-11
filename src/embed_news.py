import os
import json
import hashlib 
from src.utils import logger as log
from src.utils import CollectionVector, Config
from qdrant_client import QdrantClient
from qdrant_client.http import models
from transformers import AutoTokenizer, AutoModel
from typing import Dict, Any
from tqdm import tqdm

class NewsToQdrant:
    def __init__(self, 
                 qdrant_client: QdrantClient,
                 data_path: str, 
                 filename: str,
                 config: Config, 
                 collection_name: str = "prod"
    ) -> None:
        self.qdrant_client = qdrant_client
        self.data_path = data_path
        self.filename = filename
        self.config = config
        self.collection_name = collection_name
        self._tokenizer = AutoTokenizer.from_pretrained("sts/paraphrase-multilingual-MiniLM-L12-v2")
        self._model = AutoModel.from_pretrained("sts/paraphrase-multilingual-MiniLM-L12-v2")
    def prepare_collection_point(self, data: Dict[str, Any]):
        inputs = self._tokenizer(text=data["description"],
                                 padding=True,
                                 truncation=True,
                                 return_tensors="pt",
                                 max_length=self.config.conf["vector_size"]
                                )
        results = self._model(**inputs)
        embeddings = results.last_hidden_state[:, 0, :].cpu().detach().numpy()
        embeddings = embeddings.flatten().tolist()
        id = hashlib.md5(data["url"].encode()).hexdigest()
        try:
            components = CollectionVector(**{"id":id, 
                                             "embeddings":embeddings,
                                             "payload":{
                                             "title":data["title"], 
                                             "description":data["description"],
                                             "publishedAt":data["publishedAt"], 
                                             "name":data["source"]["name"],
                                             }
                                            }
                                        )
            return components
        except Exception as exp:
            log.LOG_DB.error(f"error due to {exp}")
    def embed_collection_point(self):
        log.LOG_DB.info("Load News Data")
        if os.path.exists(f"{self.data_path}/{self.filename}"):
            points = []
            with open(f"{self.data_path}/{self.filename}", 
                      mode="r", 
                      encoding="utf-8") as js:
                data = json.load(js)
                for article in tqdm(desc="prepare points: ", iterable=data["articles"]):
                    point=self.prepare_collection_point(article)
                    points.append(models.PointStruct(
                        id=point.id,
                        vector=point.embeddings,
                        payload=point.payload
                    ))
                log.LOG_DB.info(f"Add {len(points)} Points to Qdrant DB")
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points,
                    wait=True
                )
                log.LOG_DB.info("All Points Loaded Successfully..")
        else:
            log.LOG_DB.error(f"{self.filename} doesn't exist in data directory..")


