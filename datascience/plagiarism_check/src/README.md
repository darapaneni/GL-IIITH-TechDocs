# Document Similarity using Word2Vec

Calculate the similarity distance between documents using pre-trained word2vec model.

### Usage

- Load a pre-trained word2vec model. _Note_: You can use [Google's pre-trained word2vec model](https://bit.ly/w2vgdrive), if you don't have one.
    
     ```python
    from gensim.models.keyedvectors import KeyedVectors
    model_path = './data/GoogleNews-vectors-negative300.bin'
    w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
     ```

- Once the model is loaded, it can be passed to `DocSim_ver1` class to calculate document similarities.
 
    ```python
    from DocSim_ver1 import DocSim
    ds = DocSim(w2v_model)
    ```

- Calculate the similarity score between an incoming latest document & a list of target documents.

    ```python
    new_doc = incoming_doc(incoming pdf)
    source_repo = iterate_files(repository pdfs)
    ```

  # This will return all repository document names with similarity scores sorted from high to low
  sim_scores = ds.calculate_similarity(new_doc, source_repo)

  print(sim_scores)
  ```
- Output is as follows:
  ```python
    [{'score': 0.9999926, 'doc': 'gpt4.pdf'}, {'score': 0.78343254, 'doc': 'document1.pdf'}, {'score': 0.7518736, 'doc': 'document6.pdf'}, {'score': 0.74963504, 'doc': 'document2.pdf'}, {'score': 0.7432639, 'doc': 'document5.pdf'}, {'score': 0.72701806, 'doc': 'document7.pdf'}, {'score': 0.7019252, 'doc': 'document4.pdf'}]
  ```

- _Note_: You can optionally pass a `threshold` argument to the  `calculate_similarity()` method to return only the repository documents with similarity score above the threshold.

    ```python
    sim_scores = ds.calculate_similarity(source_doc, target_docs, threshold=0.7)
    ```


### Requirements
- Python 3 only
- **_gensim_** : to load the word2vec model
- **_numpy_**  : to calculate similarity scores
