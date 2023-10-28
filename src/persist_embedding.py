"""
Effortless way to get embeddings from MongoDB so to search by using FAISS.
"""


# from pymongo import MongoClient
# import numpy as np
# import faiss
# 
# # initialize MongoDB python client
# client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
# 
# db_name = "deep_face_db"
# collection_name = "face_embeddings"
# collection = client[db_name][collection_name]
# 
# # Load embeddings from MongoDB
# embeddings = []
# for doc in collection.find():
#     embeddings.append(doc['embedding'])
# embeddings = np.array(embeddings)
# 
# # Initialize FAISS index
# dimension = embeddings.shape[1]  # Assuming embeddings are 1D arrays
# index = faiss.IndexFlatL2(dimension)
# 
# # Add embeddings to FAISS index
# index.add(embeddings)
# 
# # Now you can use FAISS for similarity search
# query_embedding = ...  # Get query embedding
# D, I = index.search(query_embedding.reshape(1, -1), k=10)  # Find 10 nearest neighbors