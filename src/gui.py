import tkinter as tk
from tkinter import filedialog, messagebox
from scorer import extract_text_from_pdf, calculate_similarity_using_tensorflow, calculate_similarity_tfidf
import os
import glob

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

        # DEBUG PRINT - Check which files are detected
        ref_pdfs = glob.glob(os.path.join(ref_dir, "*.pdf"))
        print(f"Reference PDFs found: {ref_pdfs}")

        # Extract text from all reference PDFs
        for pdf_path in ref_pdfs:
            raw_text = extract_text_from_pdf(pdf_path)
            if raw_text:
                reference_texts.append(raw_text)

        if not reference_texts:
            messagebox.showerror("Error", "No valid reference text extracted!")
            return {}

        results = {}

        # DEBUG PRINT - Check which student files are detected
        student_pdfs = glob.glob(os.path.join(student_dir, "*.pdf"))
        print(f"Student PDFs found: {student_pdfs}")

        # Process each student PDF separately
        for pdf_path in student_pdfs:
            filename = os.path.basename(pdf_path)  # Get only the filename
            raw_text = extract_text_from_pdf(pdf_path)
            if raw_text:
                # Use TF-IDF similarity instead of USE for better accuracy
                score = calculate_similarity_tfidf(reference_texts, raw_text)
                results[filename] = score
                print(f"Processed {filename}: {score:.2f}%")  # DEBUG PRINT

        return results
    
    def display_results(self, results):
        self.results_text.delete(1.0, tk.END)
        if not results:
            self.results_text.insert(tk.END, "No results found!\n")
        else:
            for filename, score in results.items():
                self.results_text.insert(tk.END, f"{filename}: {score:.2f}%\n")

def run_gui():
    root = tk.Tk()
    app = NLPScorerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
