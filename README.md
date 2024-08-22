
# 🚀 AI PDF Assistant

AI PDF Assistant reads all uploaded PDF files and generates questions and answers from them, built using LangChain, Streamlit, and OpenAI.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_name>
```

### 2. Create a Python Virtual Environment
```bash
python -m venv env
```

### 3. Activate the Virtual Environment

- **For Windows:**
  ```bash
  .\env\Scripts\activate
  ```
- **For macOS/Linux:**
  ```bash
  source env/bin/activate
  ```

### 4. Navigate to the Project Directory
```bash
cd <repository_name>
```

### 5. Create a `.env` File
Create a `.env` file in the root directory of the project and add your OpenAI key:

```
OPEN_AI_KEY=your_open_ai_key_here
```

### 6. Install the Required Packages
```bash
pip install -r requirements.txt
```

### 7. Run the Application
```bash
streamlit run app.py
```
### 8. How to use
After opening the browser, keep the left-side menu open and click on 'Upload'. Here, you can upload any number of PDFs and then chat with the assistant about whatever you need from PDF content
