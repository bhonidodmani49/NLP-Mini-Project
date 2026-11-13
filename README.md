# SONG LYRICS EXPLORER — NLP Web Application

An advanced, full-stack Natural Language Processing (NLP) web application designed for analyzing song lyrics, extracting sentiment polarity, multi-emotion breakdowns, vocabulary richness, phrase collocations, POS distributions, and phonetic rhyming groups.

Developed as a college mini-project for **AI & Machine Learning Engineering NLP Project Viva & Demonstration**.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [NLP Pipeline Architecture](#nlp-pipeline-architecture)
5. [Folder Structure](#folder-structure)
6. [Installation & Setup Guide (Windows)](#installation--setup-guide-windows)
7. [Running the Application](#running-the-application)
8. [System Workflow](#system-workflow)
9. [Screenshots Placeholder](#screenshots-placeholder)
10. [Academic Viva Reference](#academic-viva-reference)
11. [Limitations & Future Enhancements](#limitations--future-enhancements)
12. [Conclusion](#conclusion)

---

## Introduction

Music lyrics are a unique form of unstructured text data characterized by poetic rhythm, emotional repetition, sub-clauses, and phonetic harmonies. **Song Lyrics Explorer** transforms raw song text into rich visual analytics. The platform enables users to enter song titles and lyrics or upload `.txt` files to analyze:
- Word Frequency & Type-Token Ratio (TTR) Vocabulary Richness
- VADER & TextBlob Sentiment Classification
- Lexicon-Based Emotion Scoring (Joy, Sadness, Anger, Fear, Love, Surprise, Trust)
- Phonetic Rhyme Clustering via CMU Pronouncing Dictionary
- Bigram & Trigram Phrase Extraction
- Dynamic Word Cloud Generation
- Part-of-Speech (POS) Tag Distributions

---

## Key Features

- 🎵 **Lyrics Preprocessing Inspector**: View raw text vs cleaned tokens and lemmatized stems.
- 📊 **Interactive Word Frequency**: Explore Top 10, 20, or 30 content words with interactive Chart.js bar charts.
- 😊 **Dual Sentiment Analysis**: Computes VADER Compound Score alongside TextBlob Polarity and Subjectivity.
- 💭 **Emotion Breakdown**: Multi-emotion scoring identifying dominant emotion with percentage shares.
- 🔤 **Phonetic Rhyme Detection**: Uses CMU Pronouncing Dictionary phonetic tails to group rhyming words.
- ☁️ **Dynamic Word Cloud**: Generates dark-theme word clouds with inline Base64 rendering and PNG download support.
- 💬 **N-Gram Phrase Collocations**: Switch between 2-word (Bigram) and 3-word (Trigram) recurring lyric motifs.
- 📈 **Vocabulary & Text Statistics**: Calculates Type-Token Ratio (TTR), average word length, sentence count, and line metrics.
- 📑 **Multi-Format Export**: Download complete reports as formatted PDF, clean CSV, raw JSON, or PNG Word Cloud.

---

## Technology Stack

- **Backend**: Python 3.9+, Flask Web Framework
- **NLP & Computational Libraries**: NLTK, VADER (`vaderSentiment`), TextBlob, WordCloud, Matplotlib, Pandas, NumPy
- **PDF Generation**: ReportLab
- **Frontend**: HTML5, CSS3 Glassmorphism UI, Vanilla JavaScript (ES6+)
- **Visualizations**: Chart.js 4.x CDN
- **Icons & Fonts**: Font Awesome 6.4, Google Fonts (Inter, Outfit, Fira Code)

---

## NLP Pipeline Architecture

1. **Preprocessing (`nlp/preprocessing.py`)**:
   - Case normalization (lowercasing).
   - Removal of punctuation and special symbols.
   - NLTK `punkt` tokenization.
   - Stopword filtering (removing non-semantic words like "the", "is").
   - Lemmatization via `WordNetLemmatizer` and stemming via `PorterStemmer`.

2. **Text Metrics & Vocabulary (`nlp/statistics.py`)**:
   - Type-Token Ratio (TTR %) = `(Unique Words / Total Words) * 100`.
   - Line, paragraph, sentence, and character metrics.

3. **Frequency & POS Analysis (`nlp/frequency.py`)**:
   - Word counts, repeated word ranking with share percentage.
   - NLTK POS tagging mapped into Nouns, Verbs, Adjectives, Adverbs, Pronouns, and Other.

4. **Sentiment & Emotion Engines (`nlp/sentiment.py` & `nlp/emotion.py`)**:
   - VADER compound polarity scoring classifying text as Positive, Negative, or Neutral.
   - Curated music emotion lexicon matching tokens across 7 emotional categories.

5. **Phonetic Rhyme Detection (`nlp/rhyme.py`)**:
   - CMU Dictionary lookup & phonetic tail extraction (stressed vowel to ending consonant phones).

6. **N-Gram Phrase Extraction (`nlp/phrases.py`)**:
   - NLTK `ngrams` generating Top Bigrams and Trigrams.

7. **WordCloud Generator (`nlp/wordcloud_generator.py`)**:
   - Matplotlib/WordCloud rendering saving PNG images and Base64 encoded data.

---

## Folder Structure

```
song-lyrics-explorer/
│
├── app.py                      # Main Flask application entrypoint & API routes
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
├── .gitignore                  # Git ignore specifications
│
├── data/
│   └── sample_lyrics.txt       # Demo song lyrics ("Midnight Dreams")
│
├── nlp/
│   ├── __init__.py             # NLP package marker
│   ├── setup_nltk.py           # Automatic NLTK dataset downloader
│   ├── preprocessing.py        # Tokenizer, stopword filter, lemmatizer
│   ├── statistics.py           # Text metrics & vocabulary richness (TTR)
│   ├── frequency.py            # Word frequency, repeated words, POS tagging
│   ├── sentiment.py            # VADER & TextBlob sentiment analysis
│   ├── emotion.py              # Lexicon-based emotion detector
│   ├── rhyme.py                # CMUDict phonetic rhyme detector
│   ├── phrases.py              # Bigram & Trigram phrase collocations
│   ├── structure.py            # Lyrics section & line structure analysis
│   ├── wordlength.py           # Word length distribution histogram
│   └── wordcloud_generator.py # Dynamic WordCloud PNG & Base64 generator
│
├── templates/
│   ├── base.html               # Master glassmorphism layout template
│   ├── index.html              # Hero landing page
│   ├── analyzer.html           # Input form & interactive dashboard
│   └── about.html              # Technical explanation & Viva FAQ guide
│
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphism dark-theme styling
│   ├── js/
│   │   ├── main.js             # General app interactions & utilities
│   │   ├── analyzer.js         # AJAX form submit, file upload & tab engine
│   │   └── charts.js           # Chart.js initialization routines
│   └── generated/
│       └── wordclouds/         # Saved PNG word cloud images
│
└── uploads/                    # Temporary uploaded text files
```

---

## Installation & Setup Guide (Windows)

### Step 1: Open PowerShell or Command Prompt
Navigate to your project folder:
```cmd
cd "C:\Users\prajwal pedru kola\.gemini\antigravity\scratch\song-lyrics-explorer"
```

### Step 2: Create a Python Virtual Environment
```cmd
python -m venv venv
```

### Step 3: Activate the Virtual Environment
Windows Command Prompt / PowerShell:
```cmd
venv\Scripts\activate
```

### Step 4: Install Dependencies
```cmd
pip install -r requirements.txt
```

---

## Running the Application

Execute the Flask server:
```cmd
python app.py
```

Once started, open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

> **Note**: On initial run, `nlp/setup_nltk.py` will automatically download required NLTK datasets (`punkt`, `stopwords`, `wordnet`, `vader_lexicon`, `cmudict`).

---

## System Workflow

```
[ HOME LANDING PAGE ]
        ↓
[ ANALYZER PAGE ]
        ↓
( Paste Lyrics OR Upload .txt File OR Click "Load Sample Lyrics" )
        ↓
[ CLICK "ANALYZE LYRICS" ]
        ↓
( AJAX Request to Flask POST /analyze )
        ↓
[ PYTHON NLP PIPELINE RUNS ]
  ├── Preprocessing & Lemmatization
  ├── VADER & TextBlob Sentiment
  ├── Emotion Lexicon Scoring
  ├── CMUDict Phonetic Rhyme Search
  ├── N-Gram Phrase Extraction
  └── Dynamic WordCloud Generation
        ↓
[ INTERACTIVE DASHBOARD RENDERS ]
  ├── Overview Stats Cards
  ├── Chart.js Word Frequency & Sentiment Charts
  ├── Emotion & POS Distribution
  ├── Rhyme Clusters & Structure Metrics
  └── PDF / CSV / JSON / Image Exports
```

---

## Screenshots Placeholder

- **Hero Landing Page**: Clean dark-mode hero section with feature cards.
- **Analyzer Input**: Form with title, artist, file upload dropzone, and sample loader.
- **NLP Dashboard**: Interactive tabs showing WordCloud, Sentiment Doughnut, Emotion Bar, and Rhymes.

---

## Academic Viva Reference

- **Why Tokenization?**: Splits continuous strings into atomic tokens for processing.
- **Why Remove Stopwords?**: Removes non-semantic words ("the", "is") so frequency rankings highlight meaningful keywords.
- **How VADER Works**: Combines a rule-based sentiment lexicon with valence intensity metrics to produce compound scores between -1.0 and +1.0.
- **How Rhyme Detection Works**: Matches phonetic tails in the CMU Pronouncing Dictionary from the last stressed vowel.

---

## Limitations & Future Enhancements

- **Limitations**:
  - Emotion detection uses lexicon matching rather than deep transformer models (like BERT) to keep deployment lightweight.
  - Rhyme detection relies on English CMUDict phonetics and may not cover custom slang or non-English lyrics.
- **Future Enhancements**:
  - Integration of Spotify API for automatic lyrics fetching.
  - Multi-language lyrics translation & multilingual NLP parsing.

---

## Conclusion

**Song Lyrics Explorer** bridges natural language processing theory with an engaging user interface. It provides an intuitive, robust, and academically sound tool for analyzing poetic and musical text.
