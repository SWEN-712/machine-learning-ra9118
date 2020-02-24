#using NLTK library, we can do lot of text preprocesing
import nltk,string
#nltk.download('punkt')
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

import pandas as pd
import numpy as np

# remove  non alphabetic characters.
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)



class TextNLP:
     def textPreProcessing(self,text):
        print(text)
        #function to split text into word
        #tokens = word_tokenize(text)
        #print(tokens)
        tokens = word_tokenize(text.translate(remove_punct_dict))
        # remove  non alphabetic characters.
        #tokens=[word.lower() for word in tokens if word.isalpha()]
        print(tokens)

        #Removing stop words frequent words
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if not word in stop_words]
        print(tokens)

        #Lemmatizer
        wnl = WordNetLemmatizer()
        return " ".join([wnl.lemmatize(i) for i in tokens])

     def textPreProcessingOnlyAlphabetic(self,text):

        tokens = word_tokenize(text.translate(remove_punct_dict))

        return " ".join([word.lower() for word in tokens if word.isalpha() or word.isnumeric()])
     def informationExtraction(self,text):
         text = text.replace(".", " ")



## Test code
def main():
    textNLP = TextNLP()
    str= "Create a named mock of the request type from this builder. The same builder can be called to create multiple mocks.";
    #print(str)
    newText= textNLP.textPreProcessing(str)
    print(newText)
    str= "Creates mock object of given class or interface. See examples in javadoc for Mockito class";
    #print(str)
    newText= textNLP.textPreProcessing(str)
    print(newText)


if __name__ == '__main__':main()