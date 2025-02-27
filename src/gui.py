import tkinter as tk
from tkinter import filedialog, messagebox
from scorer import extract_text_from_pdf, calculate_similarity_using_tensorflow
import os

class NLPScorerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NLP PDF Plagiarism Checker")
        self.root.geometry("600x500")
        
        # Variables
        self.ref_dir = tk.StringVar()
        self.student_dir = tk.StringVar()
        self.threshold = tk.DoubleVar(value=0.3)
        
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
        tk.Label(self.root, text="Similarity Threshold (0-1):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.threshold, width=10).pack()
        
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
            
            results = self.process_pdfs(ref_dir, student_dir, threshold)
            self.display_results(results)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def process_pdfs(self, ref_dir, student_dir, threshold):
        reference_texts = []
        for filename in os.listdir(ref_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(ref_dir, filename)
                raw_text = extract_text_from_pdf(pdf_path)
                if raw_text:  # Only add non-empty texts
                    reference_texts.append(raw_text)
        
        results = {}
        for filename in os.listdir(student_dir):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(student_dir, filename)
                raw_text = extract_text_from_pdf(pdf_path)
                if raw_text:
                    score = calculate_similarity_using_tensorflow(reference_texts, raw_text)
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
