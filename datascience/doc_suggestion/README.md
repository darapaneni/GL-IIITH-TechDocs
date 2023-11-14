# Doc_suggestion
# Document suggestions based on user's document 

This code takes two parameters the first parameter is title of the document and the second parameter is text  from the document. 

If the text from document is sufficiently large i.e. word count is more than 100 then the key words from this text is extracted and 5 of them are used in addition to title as search parameter. Text parameter can be a blank string. 

Search query is generated using title and keywords extracted from text for screen Google scholar. English language selected as default and the results are sorted on chronologically descending order. First five results are used for presenting the suggestions to  user ensuring that latest information is presented. 


The code Returns list of dictionary containing latest 5 results as mentioned above. 

The dictionary will have structure as follows

    KEY                                            CONTENT
    
    "title"                        :            Title of the article

    "link"                         :            Link to the article

    "publication_info"             :            Publication information 

    "latest_versions_link"         :            Latest version link 

    "related_articles_link"        :            Related article links 

    "Resource"                     :            Dictonary 
   
Resource dictonary content

      KEY                                          CONTENT
     "r_title"                    :            Title of the resource file 

     "r_link"                     :            Link to resource file


Requirements.txt file is included for installing all requirements.
