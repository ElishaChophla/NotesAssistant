import os
import pickle

import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_vector_store(chunks):

    embeddings = model.encode(
        chunks
    )

    embeddings = np.array(
        embeddings,
        dtype=np.float32
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    os.makedirs(
        "faiss_db",
        exist_ok=True
    )

    faiss.write_index(
        index,
        "faiss_db/index.faiss"
    )

    with open(
        "faiss_db/chunks.pkl",
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )

    return len(chunks)