import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from collections import Counter
from parsel import Selector
import requests, json, os

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def extract_keywords(text, num_keywords):
    # Tokenize the text
    words = word_tokenize(text)

    # Part-of-Speech (POS) tagging
    tagged_words = pos_tag(words)

    # Extract nouns, pronouns, interjections, and adjectives
    allowed_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'JJ', 'JJR', 'JJS', 'UH']
    filtered_words = [word for word, tag in tagged_words if tag in allowed_tags]

    # Get the most common words
    word_freq = Counter(filtered_words)
    keywords = word_freq.most_common(num_keywords)

    return [keyword[0] for keyword in keywords]


def scrape_Record(query: str, text: str):
    source = []
    sources = ""
    if len(text.split())>100 :
        
        source = extract_keywords(text, 5)
        #print(source)
    
        # source:NIPS OR source:Neural Information
        sources = " ".join([f'{item}' for item in source]) 
    #print(sources)
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": f'{query.lower()} {sources}',  # search query
        "hl": "en",                         # language of the search
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    html = requests.get("https://scholar.google.com/scholar?&scisbd=1", params=params, headers=headers, timeout=30)
    selector = Selector(html.text)

    suggestions = []
    for result in selector.css(".gs_r.gs_scl")[:5]:

        title = result.css(".gs_rt").xpath("normalize-space()").get()
        link = result.css(".gs_rt a::attr(href)").get()
        #result_id = result.attrib["data-cid"]
        #snippet = result.css(".gs_rs::text").get()
        publication_info = result.css(".gs_a").xpath("normalize-space()").get()
        #cite_by_link = f'https://scholar.google.com{result.css(".gs_or_btn.gs_nph+ a::attr(href)").get()}'
        #all_versions_link = f'https://scholar.google.com{result.css("a~ a+ .gs_nph::attr(href)").get()}'
        latest_versions_link = f'https://scholar.google.com{result.css("a~ a+ .gs_nph::attr(href)").get()}'
        related_articles_link = f'https://scholar.google.com{result.css("a:nth-child(4)::attr(href)").get()}'
        file_title = result.css(".gs_or_ggsm a").xpath("normalize-space()").get()
        file_link = result.css(".gs_or_ggsm a::attr(href)").get()

        suggestions.append({
            #"result_id": result_id,
            "title": title,
            "link": link,
            #"snippet": snippet,
            "publication_info": publication_info,
            #"cite_by_link": cite_by_link,
            #"all_versions_link": all_versions_link,
            "latest_versions_link": latest_versions_link,
            "related_articles_link": related_articles_link,
            "Resource": {
                "r_title": file_title,
                "r_link": file_link
            }
        })


       # print(json.dumps(suggestions, indent=2, ensure_ascii=False))
       #print(suggestions)

    return suggestions

#text = "Phyto-oestrogens have been suggested to have a preventive effect against various cancers. This review includes a discussion of the consumption of phyto-oestrogen-rich foods such as soy, a source of isoflavones, and whole grain products, which contain lignans, and their role in the prevention of breast, prostate, and colon cancer. In women, a soy-containing diet is only slightly protective against breast cancer, if at all, but is more likely to be beneficial if initiated before puberty or during adolescence. These findings are supported by conclusions of studies of immigrants and other epidemiological studies. However, in one case-control study and one prospective study, a low-lignan diet increased the risk of breast cancer. Experimental evidence also exists for an inhibitory effect of soy and rye bran on prostate-cancer growth and for rye bran or isolated lignans on colon cancer. Whether these observed protective effects are caused by the presence of dietary phyto-oestrogens, or whether they are merely indicators of a healthy diet in general, has not been established. The discovery of microRNAs (miRNAs) almost two decades ago established a new paradigm of gene regulation. During the past ten years these tiny non-coding RNAs have been linked to virtually all known physiological and pathological processes, including cancer. In the same way as certain key protein-coding genes, miRNAs can be deregulated in cancer, in which they can function as a group to mark differentiation states or individually as bona fide oncogenes or tumour suppressors. Importantly, miRNA biology can be harnessed experimentally to investigate cancer phenotypes or used therapeutically as a target for drugs or as the drug itself. "
#suggestions = scrape_Record("Cancer", text)
#print(len(suggestions))
