import numpy as np
import os

incoming_pdf_path = "./data/latest"
repo_pdf_path =  "./data/source_repo"

class DocSim:
    def __init__(self, w2v_model, stopwords=None):
        self.w2v_model = w2v_model
        self.stopwords = stopwords if stopwords is not None else []

    def vectorize(self, doc: str) -> np.ndarray:
        """
        Identify the vector values for each word in the given document
        :param doc:
        :return:
        """
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        vector = np.mean(word_vecs, axis=0)
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, incoming_doc, source_repo=None, threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""

        if not source_repo:
            return []

        # if isinstance(source_repo, str):
        #     source_repo = [source_repo]

        incoming_vec = self.vectorize(incoming_doc)
        results = []

        for filename, text in source_repo.items():
            # print(f"File: {filename}")
            # print(f"Text: {text}\n")
            source_vec = self.vectorize(text)
            sim_score = self._cosine_sim(incoming_vec, source_vec)
            if sim_score > threshold:
                results.append({"score": sim_score,"doc":filename})
                # results.append({"score": sim_score, "doc": doc})
            # Sort results by score in desc order
            results.sort(key=lambda k: k["score"], reverse=True)

        return results
