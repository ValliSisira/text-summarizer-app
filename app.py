from __future__ import unicode_literals
from flask import Flask, render_template, url_for, request
# from openai_summarization import generate_abstractive_summary
from huggingface_summarization import generate_abstractive_summary

from spacy_summarization import text_summarizer
from nltk_summarization import nltk_summarizer
import time
import spacy
import nltk

# Download necessary NLTK resources
nltk.download('punkt_tab')

print(nltk.data.path)
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Sumy Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Sumy Summarizer
def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

# Reading Time
def readingTime(mytext):
    total_words = len([token.text for token in nlp(mytext)])
    estimatedTime = total_words / 200.0
    return estimatedTime

# Fetch Text From Url
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)
        final_summary = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end - start
    return render_template('index.html', ctext=rawtext, final_summary=final_summary,
                           final_time=final_time, final_reading_time=final_reading_time,
                           summary_reading_time=summary_reading_time)

@app.route('/analyze_url', methods=['GET', 'POST'])
def analyze_url():
    # ---- defaults so template variables always exist ----
    ctext = ""
    summary = ""
    final_time = 0
    final_reading_time = 0
    summary_reading_time = 0

    if request.method == 'POST':
        raw_url = request.form.get('raw_url', '').strip()
        try:
            start = time.time()

            #  fetch and summarise
            ctext = get_text(raw_url)                 # full article text
            summary = text_summarizer(ctext)          # extractive summary

            #   reading-time metrics
            final_reading_time   = readingTime(ctext)
            summary_reading_time = readingTime(summary)
            final_time           = time.time() - start

        except Exception as e:
            print(" analyse_url error:", e)
            summary = "Error: unable to fetch or summarise the provided URL."

    # ---- render the same index.html used for text ----
    return render_template(
        "index.html",
        ctext=ctext,
        summary=summary,
        final_time=final_time,
        final_reading_time=final_reading_time,
        summary_reading_time=summary_reading_time
    )


@app.route('/compare_summary', methods=['GET', 'POST'])
def compare_summary():
    return render_template('compare_summary.html')

@app.route('/comparer', methods=['GET', 'POST'])
def comparer():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)

        # SpaCy Summarizer
        final_summary_spacy = text_summarizer(rawtext)
        summary_reading_time_spacy = readingTime(final_summary_spacy)
        
        # NLTK Summarizer
        final_summary_nltk = nltk_summarizer(rawtext)
        summary_reading_time_nltk = readingTime(final_summary_nltk)
        
        # Sumy Summarizer
        final_summary_sumy = sumy_summary(rawtext)
        summary_reading_time_sumy = readingTime(final_summary_sumy)

        end = time.time()
        final_time = end - start
        
    return render_template('compare_summary.html', ctext=rawtext, 
                           final_summary_spacy=final_summary_spacy, 
                           final_summary_nltk=final_summary_nltk,
                           final_summary_sumy=final_summary_sumy, 
                           final_time=final_time,
                           final_reading_time=final_reading_time, 
                           summary_reading_time_spacy=summary_reading_time_spacy,
                           summary_reading_time_nltk=summary_reading_time_nltk,
                           summary_reading_time_sumy=summary_reading_time_sumy)

@app.route('/about')
def about():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def summarize_openai():
    summary = ""
    ctext = ""
    final_time = 0
    final_reading_time = 0
    summary_reading_time = 0

    print(" Route /home called")
    if request.method == 'POST':
        ctext = request.form['text']
        method = request.form['method']
        print(" Method:", method)
        print("Input Text:", ctext)

        try:
            start = time.time()

            if method == 'openai':
                print(" Using Hugging Face")
                summary = generate_abstractive_summary(ctext)
            elif method == 'nltk':
                print(" Using NLTK")
                summary = nltk_summarizer(ctext)
            elif method == 'spacy':
                print("Using SpaCy")
                summary = text_summarizer(ctext)

            end = time.time()

            # Time and reading stats
            final_time = end - start
            final_reading_time = readingTime(ctext)
            summary_reading_time = readingTime(summary)

            print(" Generated Summary:", summary)

        except Exception as e:
            # 🔗 <------------------------ add THIS block
            print(" Exception occurred:", e)
            return render_template(
                'index.html',
                summary="An error occurred while generating the summary.",
                ctext=ctext,
                final_time=0,
                final_reading_time=0,
                summary_reading_time=0
            )

    # normal successful render
    return render_template(
        'index.html',
        summary=summary,
        ctext=ctext,
        final_time=final_time,
        final_reading_time=final_reading_time,
        summary_reading_time=summary_reading_time
    )





if __name__ == '__main__':
    app.run(debug=True)
