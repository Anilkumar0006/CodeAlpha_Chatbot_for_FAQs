# College FAQ Chatbot Using Natural Language Processing (NLP)

**Task 2 — B.Tech CSE College Assignment Project**

A simple, clear, and beginner-friendly web-based chatbot built with Python, Flask, NLTK, Scikit-learn, HTML, CSS, and JavaScript. The chatbot answers frequently asked questions (FAQs) about college admissions, courses, fees, examinations, attendance, and campus placements using basic NLP techniques.

---

## 📌 Project Overview

When students or parents visit a college website, they often have common questions regarding fees, eligibility, course branches, exam timetables, attendance rules, and placements. Instead of searching through long documents, they can ask the chatbot in natural language.

The chatbot works by:
1. Taking the user's natural language question.
2. Cleaning and preprocessing the text using **NLTK** (lowercase, removing punctuation, tokenizing words, and removing stopwords).
3. Converting the FAQ questions and the user query into numerical vectors using **TF-IDF Vectorizer**.
4. Finding the closest matching FAQ question using **Cosine Similarity**.
5. Displaying the corresponding answer on a clean, responsive web interface. If no question matches, it shows a friendly fallback message.

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language for logic and algorithms |
| **Flask** | Lightweight web framework for running the local server |
| **NLTK** | Natural Language Toolkit for text cleaning and tokenization |
| **Scikit-learn** | Machine learning library for TF-IDF and Cosine Similarity |
| **JSON** | Storing the predefined FAQ dataset (`faq_data.json`) |
| **HTML5 & CSS3** | Webpage structure and clean, responsive styling |
| **JavaScript** | Sending questions and displaying answers without reloading |

> **Note:** This project operates 100% locally. It does not require any paid APIs, external cloud services, or API keys.

---

## 📂 Project Structure

```text
CodeAlpha_Chatbot_for_FAQs/
│
├── app.py                  # Main Flask application with NLP logic and routes
├── faq_data.json           # FAQ dataset (18 college questions and answers)
├── requirements.txt        # Python package dependencies
├── README.md               # Project documentation and setup guide
│
├── templates/
│   └── index.html          # Web frontend layout with chat window and input
│
├── static/
│   ├── style.css           # Simple and clean CSS styling
│   └── script.js           # JavaScript for sending messages via fetch API
│
└── tests/
    ├── __init__.py         # Package file
    └── test_chatbot.py     # Automated unit tests for NLP and Flask routes
```

---

## 🔍 How the NLP Pipeline Works (Easy Explanation for Viva)

### Step 1: Text Preprocessing (`preprocess_text`)
Computers cannot directly understand plain English sentences. Before comparing text, we clean it:
1. **Lowercase:** Convert everything to lowercase so `"Fees"` and `"fees"` are treated as the same word.
2. **Punctuation Removal:** Remove symbols like `?`, `!`, `,`, and `.` that do not carry semantic meaning.
3. **Tokenization:** Split the sentence into a list of individual words using NLTK's `word_tokenize()`.
4. **Stopword Removal:** Remove common grammatical filler words like `"is"`, `"the"`, `"what"`, `"for"` so the algorithm focuses on key terms like `"admission"`, `"fee"`, `"btech"`.

*Example:*  
`"What is the fee for B.Tech?"` $\rightarrow$ `["fee", "btech"]`

### Step 2: TF-IDF Vectorization (`TfidfVectorizer`)
- **TF (Term Frequency):** Measures how frequently a word appears in a sentence.
- **IDF (Inverse Document Frequency):** Gives higher importance to rare, distinctive words (like `"attendance"`, `"placement"`) and lower importance to words that appear everywhere.
- The `TfidfVectorizer` converts all preprocessed FAQ questions and the user's question into rows of numbers (vectors).

### Step 3: Cosine Similarity (`cosine_similarity`)
- Cosine similarity calculates the cosine of the angle between two vectors in multi-dimensional space:
  $$\text{Cosine Similarity} = \frac{A \cdot B}{\|A\| \|B\|}$$
- Score ranges from **0.0** (completely unrelated) to **1.0** (identical meaning).
- The algorithm picks the FAQ with the highest similarity score.

### Step 4: Threshold & Fallback
- If the highest score is $\ge 0.20$ (20% similarity), the chatbot returns the matching answer.
- If the score is $< 0.20$ (e.g., if someone asks *"How to bake a cake?"*), it safely returns:  
  `"Sorry, I could not find a suitable answer. Please try another question."`

---

## 💻 How to Setup and Run in VS Code

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Click **File** $\rightarrow$ **Open Folder...**
3. Select the folder `CodeAlpha_Chatbot_for_FAQs`.

### Step 2: Open PowerShell Terminal in VS Code
Press `` Ctrl + ` `` (or click **Terminal** $\rightarrow$ **New Terminal**).

### Step 3: Install Required Packages
In the VS Code terminal, run:
```powershell
pip install -r requirements.txt
```

### Step 4: Run the Application
Start the Flask development server:
```powershell
python app.py
```

You will see output in the terminal:
```text
[*] Starting College FAQ Chatbot on http://127.0.0.1:5000
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 5: Open the Chatbot in Your Browser
Open your browser (Chrome, Edge, Firefox) and go to:
```
http://127.0.0.1:5000
```

---

## 🧪 Testing with Sample Questions

You can test the chatbot by typing questions in the input field or clicking the sample question buttons:

| Category | Try Asking |
| :--- | :--- |
| **Admissions** | `"What is the admission procedure for B.Tech?"` |
| **Eligibility** | `"What are the eligibility criteria for admission?"` |
| **Fees** | `"What is the annual fee structure for B.Tech?"` |
| **Installments** | `"Can fees be paid in installments?"` |
| **Attendance** | `"What is the minimum attendance requirement?"` |
| **Exams** | `"When are the semester exams conducted?"` |
| **Placements** | `"Which top companies visit the campus for placements?"` |
| **Hostel** | `"Are hostel facilities available for students?"` |
| **Greetings** | `"hello"` or `"hi"` |
| **Unrelated (Fallback)** | `"How to make pizza?"` $\rightarrow$ Triggers fallback response |

---

## 🔬 Running Automated Tests

To run the unit tests:
```powershell
python -m unittest tests/test_chatbot.py
```

Expected output:
```text
.........
----------------------------------------------------------------------
Ran 9 tests in 0.124s

OK
```

---

## 🎓 Viva Questions and Answers for Review

1. **Q: Why did you use TF-IDF instead of simple keyword matching?**  
   *A:* Keyword matching only checks for exact string presence. TF-IDF accounts for word importance across the whole dataset and works with vectors, allowing us to compute similarity even when questions are phrased differently.

2. **Q: What is Cosine Similarity?**  
   *A:* It is a mathematical metric that measures the cosine of the angle between two non-zero vectors. It tells us how closely two text documents are related in terms of content, regardless of sentence length.

3. **Q: Why is a similarity threshold required?**  
   *A:* Without a threshold, the chatbot would return an answer even for completely irrelevant questions (like questions about cooking or weather). The threshold ensures answers are only returned when there is a meaningful match.

4. **Q: What happens if the user inputs an empty message?**  
   *A:* The application checks for empty strings both on the frontend and backend, returning a polite prompt asking the user to type a question.
