import os
from openai import OpenAI
import pandas as pd
from tkinter import Tk, Label, Button, filedialog, ttk
from tkinter.messagebox import showinfo, showerror
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG_ID")
)

def generate_flashcards(input_text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"""Extract key concepts and create flashcards from the following text. 
                Please generate at least 10-15 flashcards (or more if needed).
                
                Format each flashcard as:
                Question:
                Answer:
                
                Make sure to cover all important concepts from the text.
                
                Text to process:
                {input_text}
                """}
            ],
            max_tokens=2000 
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error generating flashcards:", e)
        return None

def save_flashcards_to_csv(flashcards, filename="flashcards.csv"):
    questions = []
    answers = []
    
    current_question = None
    current_answer = None
    
    for line in flashcards.split('\n'):
        line = line.strip()
        if line.startswith('Question:'):
            
            if current_question and current_answer:
                questions.append(current_question)
                answers.append(current_answer)
            
            current_question = line.replace('Question:', '').strip()
            current_answer = None
        elif line.startswith('Answer:'):
            current_answer = line.replace('Answer:', '').strip()
    
    
    if current_question and current_answer:
        questions.append(current_question)
        answers.append(current_answer)
    
    df = pd.DataFrame({
        'Question': questions,
        'Answer': answers
    })
    df.to_csv(filename, index=False)

def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "r") as file:
            text = file.read()
        flashcards = generate_flashcards(text)
        if flashcards:
            save_flashcards_to_csv(flashcards)
            showinfo("Success", "Flashcards generated and saved to flashcards.csv")
        else:
            showerror("Error", "Failed to generate flashcards. Please check your input.")

def setup_gui():
    root = Tk()
    root.title("AI Flashcard Generator")
    root.geometry("600x300")  
    root.configure(bg="#f0f0f0")  
    
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TButton", padding=10, font=("Helvetica", 12))
    style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
    style.map("TButton",
        background=[("active", "#2980b9"), ("!active", "#3498db")],
        foreground=[("active", "white"), ("!active", "white")])

    header_label = ttk.Label(
        root, 
        text="AI Flashcard Generator", 
        font=("Helvetica", 18), 
        anchor="center"
    )
    header_label.pack(pady=20)

    description_label = ttk.Label(
        root, 
        text="Generate flashcards from text files using AI.", 
        font=("Modern", 12), 
        anchor="center"
    )
    description_label.pack(pady=10)

    open_button = ttk.Button(
        root, 
        text="Open Text File", 
        command=open_file,
        cursor="pointinghand"
    )
    open_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()

