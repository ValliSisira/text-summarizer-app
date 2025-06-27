#  Text Summarizer Web App

This is a Flask-based web application that allows users to generate **abstractive** and **extractive** summaries from either raw text input or a public webpage URL.

##  Features

- 📝 Summarize raw input text using:
  - **Abstractive (GPT-style)** via Hugging Face BART (`facebook/bart-large-cnn`)
  - **Extractive summarization** using NLTK, spaCy, or Sumy LexRank
-  Summarize content directly from any **public webpage URL**
-  Compare output across multiple extractive methods
-  Displays estimated reading time and processing time
-  Built with Tailwind CSS for a responsive and modern UI
-  Includes **Clear** buttons and smooth user experience enhancements

---

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **NLP Models:** 
  - Abstractive: `facebook/bart-large-cnn` (via Hugging Face Transformers)
  - Extractive: NLTK, spaCy, Sumy LexRank
- **Frontend:** HTML, Tailwind CSS
- **Parsing:** BeautifulSoup (for scraping webpage content)

---

## 🚀 Getting Started

### ✅ Prerequisites

Make sure you have Python 3.7+ and `pip` installed.

### 🔧 Installation

1. **Clone the repo:**

```bash
git clone https://github.com/your-username/text-summarizer-app.git
cd text-summarizer-app
```



## 📁 Folder Structure

**text-summarizer-app/**

* `app.py` – Main Flask application
* `huggingface_summarization.py` – Abstractive summarization logic using BART
* `nltk_summarization.py` – Extractive summarizer using NLTK
* `spacy_summarization.py` – Extractive summarizer using spaCy
* `requirements.txt` – Python dependencies
* `README.md` – Project documentation
* **templates/**

  * `index.html` – Homepage interface for summarizing text or URL
  * `compare_summary.html` – Interface to compare summaries using different methods
* **static/**

  * `style.css` – Custom CSS styling for the application



## 📸 Screenshots

You can summarize content by either:

- ✍️ Entering raw **text** into the text box, or  
- 🌐 Providing a **URL** to a public article or webpage.

Then, click on the appropriate button (Abstractive, NLTK, spaCy, or URL Summarize) to generate your summary.  
The result, along with reading time and processing time, will be shown below the input.

### 🏠 Home Page
![Home](screenshots/home-page.png)

### 📊 Compare Page
![Compare Page](screenshots/compare-page.png)

### 📝 Text Input Summarization- Extractive
![Text Input](screenshots/text.png)

![Text Summarize](screenshots/text-summarize-extractive.png)

### 📝 Text Input Summarization- Abstractive
![Text Input](screenshots/text-abstractive.png)

![Text Summarize](screenshots/abstractive-summarizer.png)


### 🔍 Compare Summaries

![Compare Input](screenshots/compare.png)

![Compare Summaries](screenshots/compare-result.png)
