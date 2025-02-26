import pdfplumber
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources (run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''  # Handle cases where text extraction fails
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ''

def preprocess_text(text):
    """Clean and preprocess text for NLP."""
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Tokenize and lowercase
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens, then lemmatize
    cleaned_tokens = [lemmatizer.lemmatize(token) for token in tokens 
                      if token.isalpha() and token not in stop_words]
    
    return ' '.join(cleaned_tokens)