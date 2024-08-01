import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from PIL import Image, ImageTk
import pymupdf

class AxiomApp:
    def __init__(self, master):
        self.master = master
        master.title("AXIOM")
        master.geometry("1280x720")

        self.create_header()
        self.create_home_page()

    def create_header(self):
        header = tk.Frame(self.master, bg="#f0f0f0")
        header.pack(fill=tk.X, pady=10)

        logo = tk.Label(header, text="⚖ AXIOM", font=("Arial", 20, "bold"), bg="#f0f0f0")
        logo.pack(side=tk.LEFT, padx=20)

        help_button = tk.Button(header, text="Help", bg="#f0f0f0")
        help_button.pack(side=tk.RIGHT, padx=10)

        settings_button = tk.Button(header, text="Settings", bg="#f0f0f0")
        settings_button.pack(side=tk.RIGHT, padx=10)

    def create_home_page(self):
        self.home_frame = tk.Frame(self.master)
        self.home_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        welcome_label = tk.Label(self.home_frame, text="Welcome to AXIOM", font=("Arial", 24, "bold"))
        welcome_label.pack(pady=50)

        description = "AXIOM is an AI-powered legal document analysis tool. Upload your document to get started."
        desc_label = tk.Label(self.home_frame, text=description, font=("Arial", 14), wraplength=600)
        desc_label.pack(pady=20)

        start_button = tk.Button(self.home_frame, text="Start Document Analysis", font=("Arial", 16), 
                                 command=self.show_upload_page, bg="#4CAF50", fg="white", padx=20, pady=10)
        start_button.pack(pady=50)

    def show_upload_page(self):
        self.home_frame.pack_forget()
        self.create_main_content()
        self.upload_document()

    def create_main_content(self):
        main_content = tk.Frame(self.master)
        main_content.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        left_frame = tk.Frame(main_content, width=640)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = tk.Frame(main_content, width=640)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_left_content(left_frame)
        self.create_right_content(right_frame)

    def create_left_content(self, parent):
        self.document_text = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=70, height=30)
        self.document_text.pack(expand=True, fill=tk.BOTH, pady=10)
        
        button_frame = tk.Frame(parent)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        upload_button = tk.Button(button_frame, text="Upload Document", bg="white", command=self.upload_document)
        upload_button.pack(side=tk.LEFT, padx=10)

        predict_button = tk.Button(button_frame, text="Predict Verdict", bg="black", fg="white")
        predict_button.pack(side=tk.RIGHT, padx=10)

    def create_right_content(self, parent):
        self.create_word_importance_table(parent)

        # Frame for Verdict and Performance Metrics
        metrics_verdict_frame = tk.Frame(parent)
        metrics_verdict_frame.pack(fill=tk.X, pady=10)

        # Verdict Frame
        verdict_frame = tk.Frame(metrics_verdict_frame, bg="white", padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
        verdict_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        tk.Label(verdict_frame, text="Verdict", font=("Arial", 16, "bold"), bg="white").pack()
        tk.Label(verdict_frame, text="Affirmed", font=("Arial", 14), bg="white").pack()
        tk.Label(verdict_frame, text="Confidence Score", font=("Arial", 12), bg="white").pack()
        tk.Label(verdict_frame, text="85.6%", font=("Arial", 16, "bold"), bg="white").pack()

        # Performance Metrics Frame
        metrics_frame = tk.Frame(metrics_verdict_frame, bg="white", padx=10, pady=10, relief=tk.RAISED, borderwidth=1)
        metrics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        tk.Label(metrics_frame, text="Performance Metrics", font=("Arial", 16, "bold"), bg="white").pack()

        metrics = [("Precision", "90%"), ("Accuracy", "90%"), ("Recall", "90%"), ("F1-Score", "90%")]
        for i, (metric, value) in enumerate(metrics):
            metric_frame = tk.Frame(metrics_frame, bg="white")
            metric_frame.pack(side=tk.LEFT, expand=True)
            tk.Label(metric_frame, text=metric, font=("Arial", 12), bg="white").pack()
            tk.Label(metric_frame, text=value, font=("Arial", 14, "bold"), bg="white").pack()

        button_frame = tk.Frame(parent)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        report_button = tk.Button(button_frame, text="Report Issues", bg="#8b0000", fg="white")
        report_button.pack(side=tk.LEFT, padx=10)

        feedback_button = tk.Button(button_frame, text="Give Feedback", bg="#2f4f4f", fg="white")
        feedback_button.pack(side=tk.RIGHT, padx=10)

    def create_word_importance_table(self, parent):
        table_frame = tk.Frame(parent)
        table_frame.pack(expand=True, fill=tk.BOTH, pady=10)
    
        columns = ('Word Importance', 'Label', 'Score')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
    
        self.tree.pack(expand=True, fill=tk.BOTH)

        # Sample data
        self.tree.insert('', 'end', values=('He is found guilty of the crime of Murder', 'affirmed', '1.29'))

    def upload_document(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.display_pdf_text(file_path)

    def display_pdf_text(self, file_path):
        text = ""
        with pymupdf.open(file_path) as doc:
            for page in doc:
                text += page.get_text("text")
        self.document_text.delete(1.0, tk.END)
        self.document_text.insert(tk.END, text)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = AxiomApp(root)
    root.mainloop()