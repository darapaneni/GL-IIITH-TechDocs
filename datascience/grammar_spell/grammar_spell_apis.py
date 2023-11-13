from flask import Flask, request, jsonify
from flasgger import Swagger

from gramformer import Gramformer
# import torch

gf=None

app = Flask(__name__)
swagger = Swagger(app)

@app.post('/grammar_edits')
def edit_sentence():
    """
    Process a sentence and return a correction edits suggestion.
    ---
    parameters:
      - name: sentence
        in: formData
        type: string
        required: true
        description: The input sentence to process.
      - name: max_candidates
        in: formData
        type: string
        required: false
        description: Candidates maximum
    responses:
      200:
        description: Grammar edits response.
    """
    sentence = request.form['sentence'] 

    max_length = 128
    # if "max_candidates" in request.form:
    #     max_candidates=request.form["max_candidates"]
    if "max_length" in request.form:
        max_length = request.form["max_length"]
    
    # Your processing logic here
    corrected_sentences = gf.correct(sentence, max_candidates=1, max_len=max_length)

    processed_sentence = ""
    for corrected_sentence in corrected_sentences:
        processed_sentence = gf.highlight(sentence, corrected_sentence)
    return jsonify({'result': processed_sentence})


@app.post('/grammar_correction')
def correct_sentence():
    """
    Process a sentence and return a correction edits suggestion.
    ---
    parameters:
      - name: sentence
        in: formData
        type: string
        required: true
        description: The input sentence to process.
      - name: max_candidates
        in: formData
        type: string
        required: false
        description: Candidates maximum
    responses:
      200:
        description: Corrected sentence.
    """
    sentence = request.form['sentence'] 

    max_length = 128
    # if "max_candidates" in request.form:
    #     max_candidates=request.form["max_candidates"]
    if "max_length" in request.form:
        max_length = request.form["max_length"]
    
    # Your processing logic here
    corrected_sentences = gf.correct(sentence, max_candidates=1, max_len=max_length)

    ## exceptions 
    #  No output in corrected_sentences set
    #  multiple output in corrected_sentences set
    return jsonify({'result': str(corrected_sentences.pop())})


if __name__ == '__main__':
    gf = Gramformer(use_gpu=False)
    app.run(debug=True, port=8080)
