import tkinter as tk
from tkinter import filedialog, messagebox
from text_processor import extract_text_from_pdf, preprocess_text
from scorer import compare_texts
import os

class NLPScorerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NLP PDF Scorer")
        self.root.geometry("600x500")
        
        # Variables
        self.ref_dir = tk.StringVar()
        self.student_dir = tk.StringVar()
        self.mode = tk.StringVar(value="strict")
        self.threshold = tk.DoubleVar(value=0.3)
        self.key_terms = tk.StringVar()
        
        # GUI Elements
        self.create_widgets()
    
    def create_widgets(self):
        # Reference Directory
        tk.Label(self.root, text="Reference PDFs Folder:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.ref_dir, width=50).pack()
        tk.Button(self.root, text="Browse", command=self.browse_ref).pack()
        
        # Student Directory
        tk.Label(self.root, text="Student PDFs Folder:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.student_dir, width=50).pack()
        tk.Button(self.root, text="Browse", command=self.browse_student).pack()
        
        # Scoring Options
        tk.Label(self.root, text="Scoring Mode:").pack(pady=5)
        tk.Radiobutton(self.root, text="Strict", variable=self.mode, value="strict").pack()
        tk.Radiobutton(self.root, text="Lenient", variable=self.mode, value="lenient").pack()
        
        tk.Label(self.root, text="Similarity Threshold (0-1):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.threshold, width=10).pack()
        
        tk.Label(self.root, text="Key Terms (comma-separated, optional):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.key_terms, width=50).pack()
        
        # Run Button
        tk.Button(self.root, text="Score PDFs", command=self.run_scoring).pack(pady=10)
        
        # Results Display
        self.results_text = tk.Text(self.root, height=15, width=70)
        self.results_text.pack(pady=10)
    
    def browse_ref(self):
        folder = filedialog.askdirectory()
        if folder:
            self.ref_dir.set(folder)
    
    def browse_student(self):
        folder = filedialog.askdirectory()
        if folder:
            self.student_dir.set(folder)
    
    def run_scoring(self):
        ref_dir = self.ref_dir.get()
        student_dir = self.student_dir.get()
        if not ref_dir or not student_dir:
            messagebox.showerror("Error", "Please select both reference and student folders.")
            return
        
        try:
            threshold = self.threshold.get()
            if not 0 <= threshold <= 1:
                raise ValueError("Threshold must be between 0 and 1.")
            
            key_terms = [term.strip() for term in self.key_terms.get().split(',') if term.strip()]
            mode = self.mode.get()
            
            results = self.process_pdfs(ref_dir, student_dir, mode, threshold, key_terms)
            self.display_results(results)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def process_pdfs(self, ref_dir, student_dir, mode, threshold, key_terms):
        reference_texts = []
        for filename in os.listdir(ref_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(ref_dir, filename)
                raw_text = extract_text_from_pdf(pdf_path)
                clean_text = preprocess_text(raw_text)
                reference_texts.append(clean_text)
        
        results = {}
        for filename in os.listdir(student_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(student_dir, filename)
                raw_text = extract_text_from_pdf(pdf_path)
                clean_text = preprocess_text(raw_text)
                score = compare_texts(reference_texts, clean_text, key_terms, mode, threshold)
                results[filename] = score
        return results
    
    def display_results(self, results):
        self.results_text.delete(1.0, tk.END)
        for filename, score in results.items():
            self.results_text.insert(tk.END, f"{filename}: {score:.2f}%\n")

def run_gui():
    root = tk.Tk()
    app = NLPScorerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()