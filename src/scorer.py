from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def vectorize_texts(texts, key_terms=None):
    """Convert texts to TF-IDF vectors, optionally emphasizing key terms."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # If key terms are provided, boost their weights
    if key_terms:
        feature_names = vectorizer.get_feature_names_out()
        for term in key_terms:
            if term in feature_names:
                idx = np.where(feature_names == term)[0][0]
                tfidf_matrix[:, idx] *= 2.0  # Double weight for key terms (adjustable)
    
    return tfidf_matrix

def calculate_similarity(tfidf_matrix, ref_indices, student_index, mode='strict', threshold=0.3):
    """Calculate similarity with customizable mode and threshold."""
    similarities = cosine_similarity(tfidf_matrix[student_index:student_index+1], 
                                   tfidf_matrix[ref_indices])
    max_similarity = np.max(similarities)
    
    # Scoring modes
    if mode == 'strict':
        score = max_similarity if max_similarity >= threshold else 0
    elif mode == 'lenient':
        score = max_similarity  # No threshold, full range
    else:
        raise ValueError("Mode must be 'strict' or 'lenient'")
    
    return score * 100  # Return as percentage

def compare_texts(reference_texts, student_text, key_terms=None, mode='strict', threshold=0.3):
    """Compare student text to reference texts with enhanced scoring."""
    all_texts = reference_texts + [student_text]
    tfidf_matrix = vectorize_texts(all_texts, key_terms)
    
    ref_indices = list(range(len(reference_texts)))
    student_index = len(reference_texts)
    
    score = calculate_similarity(tfidf_matrix, ref_indices, student_index, mode, threshold)
    return score