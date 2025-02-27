import pdfplumber
import tensorflow_hub as hub
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load TensorFlow Universal Sentence Encoder (USE)
embed_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''  # Handle cases where text extraction fails
        return text.strip()  # Remove leading/trailing whitespace
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ''

def get_text_embedding(text):
    """Convert text to a 2D vector using TensorFlow Universal Sentence Encoder."""
    embedding = embed_model([text]).numpy()
    return embedding.squeeze()  # Ensure the output is always (512,) instead of (1, 512)

def calculate_similarity_using_tensorflow(reference_texts, student_text):
    """Compute similarity scores using Universal Sentence Encoder embeddings."""
    
    # Convert reference texts into 2D NumPy array
    reference_embeddings = np.array([get_text_embedding(text) for text in reference_texts])

    # Ensure reference embeddings are 2D
    if reference_embeddings.ndim == 3:
        reference_embeddings = reference_embeddings.squeeze(axis=1)  # Convert (N,1,D) → (N,D)

    # Convert student text into 2D NumPy array
    student_embedding = get_text_embedding(student_text).reshape(1, -1)  # Ensure (1, D)

    # Compute cosine similarity
    similarities = cosine_similarity(student_embedding, reference_embeddings)

    # Get highest similarity score
    max_similarity = np.max(similarities)  

    return max_similarity * 100  # Return as percentage
