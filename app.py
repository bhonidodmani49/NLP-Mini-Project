import os
import io
import json
import csv
import uuid
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename

# NLP Engine Imports
from nlp.setup_nltk import ensure_nltk_resources
from nlp.preprocessing import preprocess_lyrics
from nlp.statistics import calculate_statistics
from nlp.frequency import analyze_frequency
from nlp.sentiment import analyze_sentiment
from nlp.emotion import analyze_emotions
from nlp.rhyme import detect_rhymes
from nlp.phrases import extract_phrases
from nlp.structure import analyze_structure
from nlp.wordlength import analyze_word_length
from nlp.wordcloud_generator import generate_wordcloud

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'song-lyrics-explorer-secret-key-nlp-project'

# Directory Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
WORDCLOUD_DIR = os.path.join(BASE_DIR, 'static', 'generated', 'wordclouds')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(WORDCLOUD_DIR, exist_ok=True)

# Ensure NLTK datasets at startup
ensure_nltk_resources()

# Global in-memory cache for recent analysis sessions (for easy export download)
ANALYSIS_SESSIONS = {}

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------

@app.route('/')
def index():
    """Renders modern Hero Landing Page."""
    return render_template('index.html')

@app.route('/analyzer')
def analyzer():
    """Renders Lyrics Input & Interactive Analyzer Page."""
    return render_template('analyzer.html')

@app.route('/about')
def about():
    """Renders About NLP Project & Viva Explanation Page."""
    return render_template('about.html')

@app.route('/sample-lyrics', methods=['GET'])
def get_sample_lyrics():
    """Returns sample lyrics for quick demo testing."""
    sample_file = os.path.join(DATA_DIR, 'sample_lyrics.txt')
    sample_text = ""
    if os.path.exists(sample_file):
        with open(sample_file, 'r', encoding='utf-8') as f:
            sample_text = f.read()

    return jsonify({
        "success": True,
        "title": "Midnight Dreams",
        "artist": "Demo Artist",
        "lyrics": sample_text
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles .txt file upload and returns extracted text."""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file part provided in request."}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No file selected for upload."}), 400

        if file and allowed_file(file.filename):
            content = file.read().decode('utf-8', errors='ignore')
            if not content.strip():
                return jsonify({"success": False, "error": "The uploaded text file is empty."}), 400
            
            return jsonify({
                "success": True,
                "filename": secure_filename(file.filename),
                "lyrics": content
            })
        else:
            return jsonify({"success": False, "error": "Invalid file format. Please upload a .txt file."}), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": f"Error processing uploaded file: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def run_analysis():
    """
    Main NLP endpoint: Runs full processing pipeline on posted lyrics.
    """
    try:
        data = request.get_json() if request.is_json else request.form
        
        title = data.get('title', '').strip() or 'Untitled Song'
        artist = data.get('artist', '').strip() or 'Unknown Artist'
        lyrics = data.get('lyrics', '').strip()

        if not lyrics:
            return jsonify({"success": False, "error": "Please enter or upload lyrics before analyzing."}), 400

        if len(lyrics) < 10:
            return jsonify({"success": False, "error": "Lyrics are too short for meaningful NLP analysis."}), 400

        # Run NLP Pipeline
        preprocessed = preprocess_lyrics(lyrics)
        stats = calculate_statistics(lyrics, preprocessed)
        freq_data = analyze_frequency(preprocessed, stats['total_words'])
        sentiment = analyze_sentiment(lyrics)
        emotion = analyze_emotions(preprocessed)
        rhyme = detect_rhymes(preprocessed)
        phrases = extract_phrases(preprocessed)
        structure = analyze_structure(lyrics)
        word_len = analyze_word_length(preprocessed)
        wordcloud = generate_wordcloud(preprocessed, WORDCLOUD_DIR)

        session_id = uuid.uuid4().hex[:12]

        result = {
            "success": True,
            "session_id": session_id,
            "song": {
                "title": title,
                "artist": artist,
                "lyrics": lyrics
            },
            "preprocessing": {
                "cleaned_text": preprocessed["cleaned_text"],
                "sample_tokens": preprocessed["tokens"][:25],
                "sample_lemmas": preprocessed["lemmatized_tokens"][:25],
                "removed_stopwords_count": len(preprocessed["removed_stopwords"])
            },
            "statistics": stats,
            "frequency": freq_data,
            "sentiment": sentiment,
            "emotion": emotion,
            "rhyme": rhyme,
            "phrases": phrases,
            "structure": structure,
            "word_length": word_len,
            "wordcloud": wordcloud
        }

        # Cache session in memory for export downloads
        ANALYSIS_SESSIONS[session_id] = result

        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": f"An unexpected error occurred during NLP analysis: {str(e)}"}), 500


@app.route('/download/wordcloud/<filename>', methods=['GET'])
def download_wordcloud(filename):
    """Serves wordcloud PNG image for downloading."""
    safe_name = secure_filename(filename)
    filepath = os.path.join(WORDCLOUD_DIR, safe_name)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=f"wordcloud_{safe_name}")
    return "WordCloud file not found.", 404

@app.route('/download/export/<export_format>/<session_id>', methods=['GET'])
def export_results(export_format, session_id):
    """Exports analysis session results as JSON, CSV, or PDF report."""
    if session_id not in ANALYSIS_SESSIONS:
        return "Session expired or invalid.", 440

    data = ANALYSIS_SESSIONS[session_id]
    title = data['song']['title']
    artist = data['song']['artist']
    safe_title = "".join([c if c.isalnum() else "_" for c in title])

    if export_format == 'json':
        json_bytes = io.BytesIO()
        json_bytes.write(json.dumps(data, indent=2).encode('utf-8'))
        json_bytes.seek(0)
        return send_file(
            json_bytes,
            mimetype='application/json',
            as_attachment=True,
            download_name=f"{safe_title}_nlp_analysis.json"
        )

    elif export_format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["SONG LYRICS EXPLORER - ANALYSIS REPORT"])
        writer.writerow(["Song Title", title])
        writer.writerow(["Artist", artist])
        writer.writerow([])

        writer.writerow(["METRIC", "VALUE"])
        writer.writerow(["Total Words", data['statistics']['total_words']])
        writer.writerow(["Unique Words", data['statistics']['unique_words']])
        writer.writerow(["Vocabulary Richness (%)", data['statistics']['vocabulary_richness']])
        writer.writerow(["Total Lines", data['statistics']['total_lines']])
        writer.writerow(["Average Word Length", data['statistics']['avg_word_length']])
        writer.writerow(["Sentiment", data['sentiment']['classification']])
        writer.writerow(["Sentiment Compound Score", data['sentiment']['compound_score']])
        writer.writerow(["Dominant Emotion", data['emotion']['dominant_emotion']])
        writer.writerow([])

        writer.writerow(["TOP 10 WORDS", "FREQUENCY"])
        for item in data['frequency']['top_10']:
            writer.writerow([item['word'], item['frequency']])

        writer.writerow([])
        writer.writerow(["RHYME GROUPS DETECTED", data['rhyme']['total_groups_count']])
        for grp in data['rhyme']['rhyme_groups']:
            writer.writerow([grp['group_name'], ", ".join(grp['words'])])

        csv_bytes = io.BytesIO()
        csv_bytes.write(output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)

        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f"{safe_title}_nlp_analysis.csv"
        )

    elif export_format == 'pdf':
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib import colors

            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
            styles = getSampleStyleSheet()
            story = []

            # Custom styles
            title_style = ParagraphStyle(
                'DocTitle',
                parent=styles['Heading1'],
                fontSize=22,
                textColor=colors.HexColor('#8B5CF6'),
                spaceAfter=6
            )
            subtitle_style = ParagraphStyle(
                'DocSubTitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#64748B'),
                spaceAfter=15
            )
            heading2 = ParagraphStyle(
                'DocHeading2',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1E293B'),
                spaceBefore=10,
                spaceAfter=6
            )

            story.append(Paragraph("Song Lyrics Explorer - Academic Report", title_style))
            story.append(Paragraph(f"<b>Title:</b> {title} | <b>Artist:</b> {artist}", subtitle_style))
            story.append(Spacer(1, 10))

            # Statistics Table
            story.append(Paragraph("<b>1. Basic Statistics & Vocabulary</b>", heading2))
            stat_data = [
                ["Metric", "Value", "Metric", "Value"],
                ["Total Words", str(data['statistics']['total_words']), "Unique Words", str(data['statistics']['unique_words'])],
                ["Vocabulary Richness", f"{data['statistics']['vocabulary_richness']}%", "Avg Word Length", str(data['statistics']['avg_word_length'])],
                ["Total Lines", str(data['statistics']['total_lines']), "Total Paragraphs", str(data['statistics']['total_paragraphs'])]
            ]
            t_stat = Table(stat_data, colWidths=[130, 120, 130, 120])
            t_stat.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0F172A')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(t_stat)
            story.append(Spacer(1, 15))

            # Sentiment & Emotion
            story.append(Paragraph("<b>2. Sentiment & Emotion Analysis</b>", heading2))
            story.append(Paragraph(f"<b>Sentiment Classification:</b> {data['sentiment']['classification']} ({data['sentiment']['emoji']})", styles['Normal']))
            story.append(Paragraph(f"<b>Compound Score:</b> {data['sentiment']['compound_score']}", styles['Normal']))
            story.append(Paragraph(f"<b>Dominant Emotion:</b> {data['emotion']['dominant_emotion']} ({data['emotion']['dominant_emoji']})", styles['Normal']))
            story.append(Paragraph(f"<b>Analysis Summary:</b> {data['sentiment']['explanation']}", styles['Normal']))
            story.append(Spacer(1, 15))

            # Top Words Table
            story.append(Paragraph("<b>3. Top 10 Words Frequency</b>", heading2))
            freq_table_data = [["Word", "Frequency"]]
            for item in data['frequency']['top_10']:
                freq_table_data.append([item['word'], str(item['frequency'])])
            
            t_freq = Table(freq_table_data, colWidths=[250, 250])
            t_freq.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('PADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(t_freq)

            doc.build(story)
            pdf_buffer.seek(0)
            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"{safe_title}_nlp_report.pdf"
            )

        except Exception as e:
            # Fallback to JSON download if ReportLab fails
            return redirect(url_for('export_results', export_format='json', session_id=session_id))

    return "Invalid format specified.", 400

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Internal server error occurred."}), 500

if __name__ == '__main__':
    print("🚀 Starting Song Lyrics Explorer NLP Application on http://127.0.0.1:5000 ...")
    app.run(debug=True, host='127.0.0.1', port=5000)
