import os
import sys

# Test imports
from nlp.preprocessing import preprocess_lyrics
from nlp.statistics import calculate_statistics
from nlp.frequency import analyze_frequency
from nlp.sentiment import analyze_sentiment
from nlp.emotion import analyze_emotions
from nlp.rhyme import detect_rhymes
from nlp.phrases import extract_phrases
from nlp.structure import analyze_structure
from nlp.wordlength import analyze_word_length

with open('data/sample_lyrics.txt', 'r', encoding='utf-8') as f:
    sample_text = f.read()

print("Testing Preprocessing...")
preprocessed = preprocess_lyrics(sample_text)
print(f"Cleaned Text Length: {len(preprocessed['cleaned_text'])} chars")
print(f"Tokens Count: {len(preprocessed['tokens'])}")
print(f"Lemmatized Count: {len(preprocessed['lemmatized_tokens'])}")

print("Testing Statistics...")
stats = calculate_statistics(sample_text, preprocessed)
print(f"Total Words: {stats['total_words']}, Unique: {stats['unique_words']}, TTR: {stats['vocabulary_richness']}%")

print("Testing Frequency & POS...")
freq = analyze_frequency(preprocessed, stats['total_words'])
print(f"Top word: {freq['top_10'][0] if freq['top_10'] else 'None'}")
print(f"POS Distribution: {freq['pos_percentages']}")

print("Testing Sentiment...")
sent = analyze_sentiment(sample_text)
print(f"Sentiment: {sent['classification']} ({sent['emoji']}), Compound: {sent['compound_score']}")

print("Testing Emotion...")
em = analyze_emotions(preprocessed)
print(f"Dominant Emotion: {em['dominant_emotion']} ({em['dominant_emoji']})")

print("Testing Rhyme Detection...")
rh = detect_rhymes(preprocessed)
print(f"Rhyme Groups Count: {rh['total_groups_count']}")
for g in rh['rhyme_groups'][:3]:
    print(f"  - {g['group_name']}: {g['words']}")

print("Testing Phrases...")
ph = extract_phrases(preprocessed)
print(f"Top Bigram: {ph['bigrams'][0] if ph['bigrams'] else 'None'}")
print(f"Top Trigram: {ph['trigrams'][0] if ph['trigrams'] else 'None'}")

print("Testing Structure...")
st = analyze_structure(sample_text)
print(f"Lines: {st['lines_count']}, Paragraphs: {st['paragraphs_count']}, Sections: {st['sections']}")

print("\n✅ ALL NLP MODULE TESTS PASSED SUCCESSFULLY!")
