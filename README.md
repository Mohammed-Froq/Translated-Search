## **🎨 Artwork Search Engine with PDF Preview**

A Streamlit-based application to **search artwork PDFs** using keywords, partial matches, and translations.  
Preview PDFs inline, download them, and explore multilingual matches automatically.

---

## Artwork PDFs (Testing Purpose)

- Use this Folder for testing Purpose [Artwork Folder](https://drive.google.com/file/d/1qG-2meSD7kR6bPD5NSt89xdU1zExpsjf/view?usp=sharing)

---

## **📑 Table of Contents**

1. [Features](#features)  
2. [Demo](#demo)  
3. [Requirements](#requirements)  
4. [Installation](#installation)  
5. [Folder Structure](#folder-structure)  
6. [How It Works (Technical Details)](#how-it-works-technical-details)  
7. [Usage](#usage)  
8. [License](#license)  

---

## **Features**

- 🔹 Search artwork PDFs by **file name** or **product description**  
- 🔹 Supports **exact match**, **partial match**, and **translated matches** (English, Dutch, French, German, Spanish, Italian)  
- 🔹 Inline PDF preview using `iframe`  
- 🔹 PDF download button for offline access  
- 🔹 Multi-language search using `deep_translator`  
- 🔹 Clean, responsive UI using Streamlit  

---

## **Demo**

- Type a keyword (e.g., “chicken” or “kip”) in the search bar  
- View **Exact Matches**, **Partial Matches**, and **Translated Matches**  
- Preview PDFs inline and download them  
- Works entirely offline once PDFs and CSV are in place  

---

## **Requirements**

Python 3.10+ and the following libraries:

- streamlit
- pandas
- deep-translator
- streamlit_pdf

# Install dependencies via:

pip install -r requirements.txt

---

## **Installation**

**1️⃣ Clone the repository:**

- git clone https://github.com/<your-username>/artwork-search-engine.git
- cd artwork-search-engine

**2️⃣ Create a Python virtual environment:**

- python -m venv venv
- source venv/bin/activate  # macOS/Linux
- venv\Scripts\activate     # Windows

**3️⃣ Install dependencies:**

- pip install -r requirements.txt

**4️⃣ Place your CSV and PDF files:**

- CSV file: update CSV_PATH in the code
- PDFs folder: update PDF_DIR in the code

---

## **Folder Structure**

artwork-search-engine/


app.py                # Main Streamlit application

requirements.txt      # Python dependencies

data.csv              # CSV containing artwork info

pdfs/                 # Folder containing artwork PDFs

README.md

---

## **How It Works (Technical Details)**

**1️⃣ Load Data**

- Reads CSV file with columns file name and product description
- Caches data with Streamlit @st.cache_data

**2️⃣ Search Functionality**

- Exact Matches: regex-based search for whole words
- Partial Matches: substring search
- Translated Matches: queries translated to multiple languages, then back to English

**3️⃣ Display Results**

- Shows results in three sections: Exact, Partial, Translated
- Each result displays:

1.File name

2.Inline PDF preview using <iframe>

3.Download button

**4️⃣ Offline PDF Viewing**

- PDF is read as bytes and encoded in Base64
- Displayed safely in-browser without external URLs

---

## **Usage**

- Run the Streamlit app:
- streamlit run app.py
- Open your browser at http://localhost:8501
- Type a keyword in the search bar to find artwork PDFs

---

## **License**

MIT License — Free to use for personal and commercial projects 
