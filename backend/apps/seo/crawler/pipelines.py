# apps/seo/crawler/pipelines.py
from services.vector_store import VectorStore
import hashlib

class PineconePipeline:
    def process_item(self, item, spider):
        docs = []
        base_id = hashlib.md5(item["url"].encode()).hexdigest()
        for field, val in item.items():
            if field == "url" or not val:
                continue
            doc_id = f"{spider.name}_{base_id}_{field}"
            docs.append({
                "id": doc_id,
                "text": f"{field}: {val}"
            })
        if docs:
            VectorStore.upsert(docs)
        return item
