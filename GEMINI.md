# **Study Notes Summarizer & Quiz Generator Agent**

AI-powered system for converting PDFs into structured study notes and generating quizzes using **Gemini CLI**, **OpenAgents SDK**, **PyPDF**, **Streamlit**, and **Context7 MCP**.

---

## ⭐ **Project Overview**

Yeh project students ko allow karta hai ke woh PDF files upload karen, unki clean text extraction karein, unse well-organized summaries generate karein, aur usi document ki base par quizzes bhi bana saken.

Is app mein powerful AI tools combine kiye gaye hain:

* Gemini CLI
* OpenAgents SDK
* PyPDF
* Context7 MCP Tools
* Streamlit UI
* Python 3.11+

---

## 📌 **Main Features**

### ✅ **1. PDF Summarizer**

* PDF upload
* Text extraction via **PyPDF**
* Output includes:

  * Point-wise study notes
  * Organized summaries
  * Important concepts
  * Definitions & key ideas

### ✅ **2. Quiz Generator**

Quizzes **original PDF text** se generate hotay hain — summary se nahi.

**Quiz Modes:**

#### • **MCQ Mode**

* Question
* Four options
* Correct choice provided

#### • **Mixed Mode**

* MCQs
* True/False
* Short-answer questions

---

## 🧩 **Technology Used**

| Technology         | Role                                     |
| ------------------ | ---------------------------------------- |
| **Gemini CLI**     | AI orchestration                         |
| **OpenAgents SDK** | Agent logic + tool calling               |
| **Context7 MCP**   | Tool provider for filesystem & utilities |
| **PyPDF**          | PDF → Text extraction                    |
| **Streamlit**      | User interface                           |
| **Python 3.11+**   | Backend engine                           |

---

# 📁 **Project Structure**

```
project/
│
├── gemini.md            # Primary agent prompt for Gemini CLI
├── README.md            # Documentation
├── app.py               # Streamlit UI
│
├── modules/
│   ├── extractor.py     # PDF text extraction
│   ├── summarizer.py    # Summary generation
│   ├── quiz_mcq.py      # Only MCQ quiz generator
│   ├── quiz_mixed.py    # Mixed-format quiz generator
│
├── assets/
│   └── samples/         # Example PDF files
│
└── requirements.txt
```

---

# 📌 **Workflow**

### **1. User uploads PDF**

→ Stored temporarily → Parsing begins

### **2. PyPDF extracts text**

→ Cleaned + processed text returned

### **3. Agent creates summary**

→ Structured notes in readable form

### **4. "Create Quiz" button pressed**

→ Agent reads full PDF text
→ Generates MCQs or mixed questions

### **5. Streamlit displays quiz**

→ User can review or export

---

# 🚀 **How to Run**

### **Install dependencies**

```
pip install -r requirements.txt
```

### **Start the Streamlit app**

```
streamlit run app.py
```

### **Run the Gemini agent**

```
gemini run gemini.md
```

---

# 🧠 **About gemini.md**

`gemini.md` file AI agent ka brain hai.
Is mein define hota hai:

* System behavior
* Summary rules
* Quiz formatting
* Tool usage
* Context7 interactions
* Response structure

Is file ko edit karke agent ka style aur functionality change ki ja sakti hai.

---

# 📌 **Quiz Output Rules**

### **MCQ Example**

```
Q1: ...
A. Option 1
B. Option 2
C. Option 3
D. Option 4
Correct Answer: B
```

### **Mixed Format Example**

```
MCQ:
Q1: ...
Correct: C

True/False:
Q2: ...
Answer: True

Short Answer:
Q3: ...
Required Keywords: ...
```

---

# 🛠️ **Modules Explanation**

### **Extractor Module**

* PyPDF ka use karke PDF se clean text nikalta hai

### **Summarizer Module**

* Gemini se structured notes banwata hai

### **Quiz MCQ Module**

* Original text se realistic MCQs banata hai

### **Mixed Quiz Module**

* MCQ + T/F + Short Answer combo generate karta hai

---

# 🌐 **Optional Deployment**

You can deploy the project on:

* Streamlit Cloud
* Railway
* Vercel backend

# ✅ **Project Status**

Fully configurable AI-based learning assistant designed for students, teachers, and creators.
