import os
from pinecone import Pinecone, ServerlessSpec
from services.openai_client import create_embeddings

# Pinecone configuration from environment
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")  # e.g. 'us-west1-gcp'
# Ensure index name is lowercase alphanumeric or '-' only
defined_index = os.getenv("PINECONE_INDEX_NAME", "default-index")
PINECONE_INDEX = ''.join(c if c.isalnum() or c == '-' else '-' for c in defined_index.lower())

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

# Parse cloud and region from environment
if PINECONE_ENV and '-' in PINECONE_ENV:
    region, cloud = PINECONE_ENV.rsplit('-', 1)
else:
    cloud = PINECONE_ENV or 'gcp'
    region = PINECONE_ENV or 'us-west1'

# Ensure cloud is valid
if cloud not in ['gcp', 'aws', 'azure']:
    cloud = 'gcp'

# Ensure index exists
existing = pc.list_indexes().names()
if PINECONE_INDEX not in existing:
    spec = ServerlessSpec(cloud=cloud, region=region)
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=1536,
        metric="cosine",
        spec=spec
    )

# Get index client
index = pc.Index(PINECONE_INDEX)

class VectorStore:
    @staticmethod
    def upsert(documents: list[dict]):
        """
        Inserts or updates documents into Pinecone index.
        documents: list of {'id': str, 'text': str, ...}
        """
        vectors = []
        for doc in documents:
            emb = create_embeddings(doc['text'])[0]
            vectors.append((doc['id'], emb, doc))
        index.upsert(vectors)

    @staticmethod
    def query(query_text: str, top_k: int = 5) -> list[dict]:
        """
        Queries Pinecone for nearest documents to query_text.
        Returns list of metadata dicts.
        """
        # Create embedding vector
        emb = create_embeddings(query_text)[0]
        # Query using the 'vector' parameter
        result = index.query(
            vector=emb,
            top_k=top_k,
            include_metadata=True
        )
        # result.matches is a list of Match objects
        return [match.metadata for match in result.matches]
