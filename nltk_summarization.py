# 

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq  

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def nltk_summarizer(raw_text):
    stopWords = set(stopwords.words("english"))
    word_frequencies = {}  
    
    # Tokenize words and calculate word frequencies excluding stopwords
    for word in word_tokenize(raw_text):  
        if word.lower() not in stopWords:  # Convert word to lowercase for consistency
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    # Calculate the maximum frequency of words
    maximum_frequency = max(word_frequencies.values())

    # Normalize word frequencies by dividing by the maximum frequency
    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    # Tokenize sentences from the raw text
    sentence_list = sent_tokenize(raw_text)
    sentence_scores = {}  

    # Score each sentence based on word frequencies
    for sent in sentence_list:  
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:  # Limit sentence length to avoid long ones
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    # Select the top 7 sentences with the highest scores for the summary
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    # Join the sentences into a summary
    summary = ' '.join(summary_sentences)  
    return summary
