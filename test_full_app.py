import os
import io
import json
import unittest
from app import app, ANALYSIS_SESSIONS

class SongLyricsExplorerTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_01_index_route(self):
        """Test GET / returns 200 and renders landing page."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Song Lyrics Explorer', response.data)
        self.assertIn(b'Discover the hidden patterns', response.data)

    def test_02_analyzer_route(self):
        """Test GET /analyzer returns 200 and renders input form & dashboard."""
        response = self.client.get('/analyzer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lyrics Analyzer', response.data)
        self.assertIn(b'Analyze Lyrics', response.data)

    def test_03_about_route(self):
        """Test GET /about returns 200 and renders Viva guide."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About & Viva Guide', response.data)
        self.assertIn(b'Academic Project Viva Guide', response.data)

    def test_04_sample_lyrics_route(self):
        """Test GET /sample-lyrics returns sample song json."""
        response = self.client.get('/sample-lyrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['title'], 'Midnight Dreams')
        self.assertIn('dancing in the golden glow', data['lyrics'].lower())

    def test_05_file_upload_route(self):
        """Test POST /upload with valid .txt file and invalid file format."""
        # Test valid .txt upload
        file_content = b"Dancing in the moonlight\nBright stars in the sky\nLove forever"
        data = {
            'file': (io.BytesIO(file_content), 'my_test_song.txt')
        }
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        res_data = json.loads(response.data)
        self.assertTrue(res_data['success'])
        self.assertIn("Dancing in the moonlight", res_data['lyrics'])

        # Test invalid extension upload
        invalid_data = {
            'file': (io.BytesIO(b"binary data"), 'test.png')
        }
        response = self.client.post('/upload', data=invalid_data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_06_nlp_analyze_pipeline(self):
        """Test POST /analyze with complete lyrics input and verify all 14 NLP requirements."""
        lyrics_text = """
        [Verse 1]
        I am dancing in the bright night sky
        Stars are shining under golden light
        Feel the love and feel the spark
        Walking through the silent dark

        [Chorus]
        Oh midnight dreams guide my way
        Dancing free every single day
        Bright light shining high
        Open up the blue sky

        [Verse 2]
        Dancing through the starlight stream
        Living inside a happy dream
        Heart beats loud and clear
        Never feel the cold fear
        """

        payload = {
            "title": "Starlight Dance",
            "artist": "Test Artist",
            "lyrics": lyrics_text
        }

        response = self.client.post('/analyze', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        session_id = data['session_id']
        self.assertIn(session_id, ANALYSIS_SESSIONS)

        # 1. Preprocessing, tokenization, stopwords, lemmatization
        preproc = data['preprocessing']
        self.assertIn('cleaned_text', preproc)
        self.assertGreater(len(preproc['sample_tokens']), 0)
        self.assertGreater(len(preproc['sample_lemmas']), 0)

        # 2. Statistics & vocabulary richness (TTR)
        stats = data['statistics']
        self.assertGreater(stats['total_words'], 0)
        self.assertGreater(stats['unique_words'], 0)
        self.assertGreater(stats['vocabulary_richness'], 0.0)
        self.assertGreater(stats['total_lines'], 0)
        self.assertGreater(stats['avg_word_length'], 0.0)

        # 3. Frequency & repeated words
        freq = data['frequency']
        self.assertGreater(len(freq['top_10']), 0)
        self.assertGreater(len(freq['top_20']), 0)
        self.assertGreater(len(freq['top_30']), 0)
        self.assertIsNotNone(freq['most_repeated_word'])
        self.assertIn('pos_percentages', freq)

        # 4. Sentiment analysis
        sentiment = data['sentiment']
        self.assertIn(sentiment['classification'], ['Positive', 'Negative', 'Neutral'])
        self.assertIsNotNone(sentiment['compound_score'])

        # 5. Emotion detection
        emotion = data['emotion']
        self.assertIn('dominant_emotion', emotion)
        self.assertIn('percentages', emotion)

        # 6. Rhyme detection
        rhyme = data['rhyme']
        self.assertIn('rhyme_groups', rhyme)
        self.assertGreaterEqual(rhyme['total_groups_count'], 0)

        # 7. Bigrams & Trigrams
        phrases = data['phrases']
        self.assertIn('bigrams', phrases)
        self.assertIn('trigrams', phrases)

        # 8. Structure & Word Length
        self.assertIn('structure', data)
        self.assertIn('word_length', data)

        # 9. Word Cloud
        wc = data['wordcloud']
        self.assertTrue(wc['base64'].startswith('data:image/png;base64,'))

        # 10. Test Exports using session_id
        # JSON export
        res_json = self.client.get(f'/download/export/json/{session_id}')
        self.assertEqual(res_json.status_code, 200)

        # CSV export
        res_csv = self.client.get(f'/download/export/csv/{session_id}')
        self.assertEqual(res_csv.status_code, 200)

        # PDF export
        res_pdf = self.client.get(f'/download/export/pdf/{session_id}')
        self.assertEqual(res_pdf.status_code, 200)

if __name__ == '__main__':
    unittest.main()
