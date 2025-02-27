# PaperCHECK

A simple tool to compare student PDFs with reference PDFs and score their similarity using Natural Language Processing (NLP). It's built from scratch with no external APIs.

## What It Does
- Reads text from PDFs in two folders: correct answers and student answers.
- Cleans the text (removes extra words, simplifies forms).
- Compares the text and gives a similarity score (0-100%).
- Shows results in a window and saves them to a file.
- Lets you tweak scoring options (strict/lenient, key words, thresholds).

## Getting Started

### Prerequisites
- Python 3.8 or higher (download from [python.org](https://www.python.org/downloads/)).

### Installation
1. Clone or download this repository to your computer.
2. Open a terminal and go to the project folder (`PaperCHECK/`).
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Put your PDFs in the `data/` folder:
   - Correct answers in `data/reference_pdfs/`.
   - Student answers in `data/student_pdfs/`.
2. Run the tool:
   - Go to `src/`:
     ```bash
     cd src
     ```
   - Start the program:
     ```bash
     python main.py
     ```
3. Use the window to:
   - Pick the PDF folders.
   - Set scoring options (if needed).
   - Click "Score PDFs" to see results.
4. Check scores in the window or `output/scores.txt`.

## File Structure
```
PaperCHECK/
├── data/
│   ├── reference_pdfs/    # Correct answer PDFs
│   └── student_pdfs/      # Student answer PDFs
├── src/                   # All code files
│   ├── text_processor.py  # Reads and cleans text
│   ├── scorer.py         # Compares and scores text
│   ├── gui.py            # Creates the window
│   └── main.py           # Starts the program
├── output/                # Results file
│   └── scores.txt        # Saved scores
├── requirements.txt       # Lists needed libraries
└── README.md             # This file
```

## Contributing
Feel free to fork this repo, make changes, and submit pull requests. Let me know if you want to improve it!

## License
No specific license—use it freely for personal or educational purposes.