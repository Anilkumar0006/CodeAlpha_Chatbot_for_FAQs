"""
College FAQ Chatbot - Flask Web Application
Developed for B.Tech CSE Project (Task 2)

This application uses Natural Language Processing (NLP):
1. NLTK for text preprocessing (lowercasing, punctuation removal, tokenization, stopword removal).
2. Scikit-learn for TF-IDF Vectorization and Cosine Similarity to find the most relevant FAQ answer.
"""

import json
import os
import re
import string
from flask import Flask, render_template, request, jsonify
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask application
app = Flask(__name__)

# Ensure required NLTK resources are downloaded safely
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Load stopwords list
try:
    stop_words = set(stopwords.words('english'))
except Exception:
    stop_words = {"what", "is", "the", "a", "an", "for", "to", "in", "of", "and", "are", "do", "can"}

# ---------------------------------------------------------------------------
# 1. Load the FAQ Dataset
# ---------------------------------------------------------------------------
def load_faq_data():
    """Loads FAQ questions and answers from faq_data.json"""
    file_path = os.path.join(os.path.dirname(__file__), "faq_data.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

faq_list = load_faq_data()
faq_questions = [item["question"] for item in faq_list]
faq_answers = [item["answer"] for item in faq_list]


# ---------------------------------------------------------------------------
# 2. Text Preprocessing Function (NLP)
# ---------------------------------------------------------------------------
def preprocess_text(text):
    """
    Cleans and preprocesses input text:
    1. Converts text to lowercase
    2. Removes punctuation
    3. Tokenizes text into words
    4. Removes common stopwords
    """
    if not text or not text.strip():
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize into words
    try:
        tokens = word_tokenize(text)
    except Exception:
        # Simple regex fallback if NLTK tokenizer has any issue
        tokens = re.findall(r"\b\w+\b", text)

    # Remove stopwords and filter empty tokens
    cleaned_tokens = [word for word in tokens if word not in stop_words]

    # Rejoin tokens into a single cleaned string
    return " ".join(cleaned_tokens)


# ---------------------------------------------------------------------------
# 3. Match User Question Using TF-IDF and Cosine Similarity
# ---------------------------------------------------------------------------
def get_chatbot_response(user_input):
    """
    Finds the most suitable FAQ answer using TF-IDF and Cosine Similarity.
    """
    # Check for empty input
    if not user_input or not user_input.strip():
        return "Please type a question so I can assist you."

    user_clean = user_input.strip().lower()

    # Handle simple greetings
    if user_clean in ["hi", "hello", "hey"]:
        return "Hello! I am your College FAQ Assistant. Ask me anything about admissions, courses, fees, exams, attendance, or placements!"

    if user_clean in ["thanks", "thank you"]:
        return "You are welcome! Let me know if you have any more questions."

    # Preprocess user question
    processed_user_query = preprocess_text(user_input)
    if not processed_user_query:
        return "Please ask a specific question related to the college."

    # Preprocess all FAQ questions
    processed_faq_questions = [preprocess_text(q) for q in faq_questions]

    # Combine FAQ questions with user query for TF-IDF vectorization
    all_texts = processed_faq_questions + [processed_user_query]

    # Create TF-IDF Vectorizer and fit on all texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # Separate FAQ question vectors and user query vector
    faq_vectors = tfidf_matrix[:-1]
    user_vector = tfidf_matrix[-1]

    # Calculate Cosine Similarity between user query and each FAQ question
    similarity_scores = cosine_similarity(user_vector, faq_vectors).flatten()

    # Find the index of the highest similarity score
    best_match_index = similarity_scores.argmax()
    best_score = similarity_scores[best_match_index]

    # Threshold for a valid match (e.g., 0.20 or 20% similarity)
    SIMILARITY_THRESHOLD = 0.20

    if best_score >= SIMILARITY_THRESHOLD:
        return faq_answers[best_match_index]
    else:
        return "Sorry, I could not find a suitable answer. Please try another question."


# ---------------------------------------------------------------------------
# 4. Flask Web Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    """Serves the chatbot home page"""
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    """API endpoint to receive user question and return chatbot response"""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"answer": "Invalid request."}), 400

    user_message = data.get("message", "")
    bot_reply = get_chatbot_response(user_message)

    return jsonify({"answer": bot_reply})


# Run the application
if __name__ == "__main__":
    print("[*] Starting College FAQ Chatbot on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
