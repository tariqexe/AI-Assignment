import tkinter as tk
from tkinter import ttk
from owlready2 import get_ontology

# Load Ontology
ontology_path = "ds.owl"  # Replace with your OWL file path
onto = get_ontology(ontology_path).load()

# Fetch quiz questions from ontology

def fetch_quiz_questions():
    questions = []
    quiz_class = onto.search_one(iri="*#Quiz")  # Ensure the Quiz class exists
    if quiz_class is None:
        print("Quiz class not found in ontology.")
        return questions

    for question in onto.search(type=quiz_class):
        label = question.label[0] if question.label else "No question found"
        answer = question.comment[0] if question.comment else "No answer available"
        questions.append((label, answer))
    return questions


# Function to Fetch Concept Details
def fetch_concept_details(concept_name):
    concept = onto.search_one(label=concept_name)
    if concept:
        details = "\n".join([x for x in concept.isDefinedBy]) if concept.isDefinedBy else "No definition available."
        formatted_details = ""
        if "Definition:" in details:
            formatted_details += f"\n\nDefinition\n{'-'*10}\n" + details.split("Definition:")[1].split("Explanation:")[0].strip()
        if "Explanation:" in details:
            formatted_details += f"\n\nExplanation\n{'-'*12}\n" + details.split("Explanation:")[1].split("Example:")[0].strip()
        if "Example:" in details:
            formatted_details += f"\n\nExample\n{'-'*8}\n" + details.split("Example:")[1].split("Formula:")[0].strip()
        if "Formula:" in details:
            formatted_details += f"\n\nFormula\n{'-'*8}\n" + details.split("Formula:")[1].strip()
        return formatted_details
    else:
        return "Concept not found in ontology."

# Navigation Bar
class NavigationBar(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(fill="x")

        # Navigation Buttons
        ttk.Button(self, text="Home", command=lambda: master.switch_frame(HomePage)).pack(side="left", padx=5)
        ttk.Button(self, text="Learn Concepts", command=lambda: master.switch_frame(LearnConceptsPage)).pack(side="left", padx=5)
        ttk.Button(self, text="Quiz", command=lambda: master.switch_frame(QuizPage)).pack(side="left", padx=5)
        ttk.Button(self, text="Help", command=lambda: master.switch_frame(HelpPage)).pack(side="left", padx=5)

# Title Frame with Background Color
class TitleFrame(tk.Frame):
    def __init__(self, master, title_text, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(bg="#4CAF50")
        self.pack(fill="x")

        title_label = tk.Label(self, text=title_text, font=("Helvetica", 24, "bold"), fg="white", bg="#4CAF50")
        title_label.pack(pady=10)

# Home Page
class HomePage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        TitleFrame(self, "Intelligent Tutoring System - Descriptive Statistics")

        # Welcome Message
        welcome_label = tk.Label(self, text="Welcome to the Intelligent Tutoring System for Descriptive Statistics!", font=("Helvetica",14), wraplength=400, justify="center")
        welcome_label.pack(pady=20)

        # Navigation Buttons
        button_style = {"width": 20, "padding": 10, "style": "Custom.TButton"}
        ttk.Style().configure("Custom.TButton", font=("Helvetica", 12), relief="raised")
        ttk.Button(self, text="Learn Concepts", command=lambda: master.switch_frame(LearnConceptsPage), **button_style).pack(pady=10)
        ttk.Button(self, text="Take a Quiz", command=lambda: master.switch_frame(QuizPage), **button_style).pack(pady=10)
        ttk.Button(self, text="Help", command=lambda: master.switch_frame(HelpPage), **button_style).pack(pady=10)

# Learn Concepts Page
class LearnConceptsPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        TitleFrame(self, "Intelligent Tutoring System - Descriptive Statistics")

        # Scrollable List of Concepts
        concepts = ["Mean", "Median", "Mode", "Standard Deviation", "Variance", "Range"]

        listbox_frame = tk.Frame(self)
        listbox_frame.pack(pady=10, side="left", fill="y")

        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        concept_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, height=15, width=20, font=("Helvetica", 12))
        for concept in concepts:
            concept_listbox.insert(tk.END, concept)
        concept_listbox.pack(side="left", fill="y")
        scrollbar.config(command=concept_listbox.yview)

        # Display Box for Concept Details
        details_box = tk.Text(self, wrap="word", height=20, width=60, font=("Helvetica", 12), padx=10, pady=10, borderwidth=2, relief="solid")
        details_box.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        def display_concept():
            selected = concept_listbox.get(tk.ACTIVE)
            details = fetch_concept_details(selected)
            details_box.delete(1.0, tk.END)
            details_box.insert(tk.END, details)

        button_style = {"width": 15, "padding": 10, "style": "Custom.TButton"}
        ttk.Button(self, text="Show Details", command=display_concept, **button_style).pack(pady=10)

        # Navigation Buttons
        ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(HomePage), **button_style).pack(pady=10)

class QuizPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        TitleFrame(self, "Quiz Page")

        self.questions = fetch_quiz_questions()
        if not self.questions:
            self.questions = [("No questions available.", "")]

        self.current_question_index = 0

        # Question Label
        self.question_label = tk.Label(self, text="", wraplength=600, font=("Helvetica", 14))
        self.question_label.pack(pady=20)

        # Answer Entry
        self.answer_var = tk.StringVar()
        self.answer_entry = tk.Entry(self, textvariable=self.answer_var, font=("Helvetica", 12), width=40)
        self.answer_entry.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        self.check_button = ttk.Button(button_frame, text="Check Result", command=self.check_answer)
        self.check_button.pack(side="left", padx=10)

        self.next_button = ttk.Button(button_frame, text="Next Question", command=self.next_question)
        self.next_button.pack(side="left", padx=10)

        self.back_button = ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(HomePage))
        self.back_button.pack(pady=20)

        # Load the first question
        self.load_question()

    def load_question(self):
        if self.current_question_index < len(self.questions):
            question, _ = self.questions[self.current_question_index]
            self.question_label.config(text=f"Question {self.current_question_index + 1}: {question}")
            self.answer_var.set("")
            self.result_label.config(text="")
        else:
            self.question_label.config(text="Quiz completed! No more questions.")
            self.answer_entry.config(state="disabled")
            self.check_button.config(state="disabled")
            self.next_button.config(state="disabled")

    def check_answer(self):
        _, correct_answer = self.questions[self.current_question_index]
        user_answer = self.answer_var.get().strip()
        correct_answer = correct_answer.replace("Answer: ", "").strip()
        if user_answer == correct_answer:
            self.result_label.config(text="Correct!", fg="green")
        else:
            self.result_label.config(text=f"Wrong! The correct answer is: {correct_answer}", fg="red")

    def next_question(self):
        self.current_question_index += 1
        self.load_question()


        # Navigation Buttons
        # ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(HomePage)).pack(pady=10)

# Help Page
class HelpPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        TitleFrame(self, "Help Page")

        tk.Label(self, text="How to Use This Tutor:", font=("Helvetica", 16, "bold"), anchor="w").pack(pady=10, fill="x")
        instructions = (
            "1. Navigate to the 'Learn Concepts' page to explore key topics.\n"
            "2. Click on a concept to view its definition, explanation, example, and formula.\n"
            "3. Take quizzes on the 'Quiz Page' to test your knowledge.\n"
            "4. Use the navigation bar to move between sections."
        )
        tk.Label(self, text=instructions, font=("Helvetica", 12), wraplength=400, justify="left").pack(pady=20)

        # Navigation Buttons
        ttk.Button(self, text="Back to Home", command=lambda: master.switch_frame(HomePage)).pack(pady=10)

# Main Application
class TutorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")  # Set the frame size to 800x600

        # Navigation Bar
        self.navbar = NavigationBar(self)

        # Initialize Frame
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = TutorApp()
    app.mainloop()
