from gensim.models.keyedvectors import KeyedVectors
from DocSim_ver1 import DocSim
from preprocess_source_repo import iterate_files
from preprocess_incoming_doc import incoming_doc
import yaml
import bz2file as bz2
import pickle

# this is the main file which calls the functions to execute the plagiarism algorithm
# this main file calls both the preprocessing functions to convert the new and the existing pdfs into a list of strings
# it uses the pre-trained word2vec model trained using Google news corpus of 3 billion running words.


# Load the YAML data from the file
with open('src\path.yml', 'r') as yaml_file:
    config_data = yaml.safe_load(yaml_file)

# Access specific values from the YAML data

stopwords_path = config_data['path']['stopwords_path']
incoming_pdf_path = config_data['path']['incoming_pdf_path']
repo_pdf_path = config_data['path']['repo_pdf_path']
online_document_url = config_data['path']['online_document_url']


def decompress_pickle(file):

    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

pickle_model = decompress_pickle('model\doc2vec.pbz2')


with open(stopwords_path, 'r') as fh:
    stopwords = fh.read().split(",")
ds = DocSim(pickle_model,stopwords=stopwords)


new_doc = incoming_doc(incoming_pdf_path)
source_repo = iterate_files(repo_pdf_path)


sim_scores = ds.calculate_similarity(new_doc, source_repo)

print(sim_scores)