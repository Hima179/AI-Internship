import tkinter as tk
from tkinter import messagebox
import json
import random
import time
import os
from PIL import Image, ImageTk

class UAIQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal AI University Quiz")
        self.root.geometry("1000x600")
        self.root.configure(bg="#F5F5F5")
        
        self.questions = []
        self.responses = {} # q_index -> {"time_taken": float, "status": str}
        self.current_q_index = 0
        
        self.timer_job = None
        self.time_left = 10
        self.start_time = 0
        
        self.load_questions()
        self.setup_ui()
        self.load_question(0)

    def load_questions(self):
        try:
            with open("questions.json", "r") as f:
                self.questions = json.load(f)
            # Shuffle options for each question
            for q in self.questions:
                random.shuffle(q["options"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")
            self.questions = [{"question": "Failed to load questions", "options": ["A","B","C","D"], "answer": "A"}]

    def setup_ui(self):
        # LEFT PANEL
        self.left_panel = tk.Frame(self.root, width=200, bg="#003366")
        self.left_panel.pack(side="left", fill="y")
        self.left_panel.pack_propagate(False)

        # Logo
        try:
            logo_img = Image.open("assets/uai_logo.png")
            logo_img = logo_img.resize((150, 150))
            self.logo_tk = ImageTk.PhotoImage(logo_img)
            tk.Label(self.left_panel, image=self.logo_tk, bg="#003366").pack(pady=10)
        except:
            tk.Label(self.left_panel, text="[UAI LOGO]", bg="#003366", fg="white", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.left_panel, text="Question Navigator", bg="#003366", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Scrollable area
        canvas = tk.Canvas(self.left_panel, bg="#003366", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.left_panel, orient="vertical", command=canvas.yview)
        self.nav_frame = tk.Frame(canvas, bg="#003366")
        
        self.nav_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.nav_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.nav_buttons = []
        for i in range(len(self.questions)):
            btn = tk.Button(self.nav_frame, text=f"Q{i+1}", width=15, bg="gray", fg="white",
                            command=lambda idx=i: self.jump_to_question(idx))
            btn.pack(pady=2)
            self.nav_buttons.append(btn)
            
        # RIGHT MAIN AREA
        self.right_panel = tk.Frame(self.root, bg="#F5F5F5")
        self.right_panel.pack(side="right", fill="both", expand=True)
        
        # Top bar
        tk.Label(self.right_panel, text="Universal AI University", bg="#F5F5F5", fg="blue", font=("Arial", 20, "bold")).pack(pady=10)
        
        self.progress_lbl = tk.Label(self.right_panel, text="", bg="#F5F5F5", font=("Arial", 12))
        self.progress_lbl.pack()
        
        self.dept_lbl = tk.Label(self.right_panel, text="", bg="#F5F5F5", font=("Arial", 10, "italic"))
        self.dept_lbl.pack(pady=5)
        
        self.q_text_lbl = tk.Label(self.right_panel, text="", bg="#F5F5F5", font=("Arial", 16, "bold"), wraplength=700)
        self.q_text_lbl.pack(pady=20)
        
        self.options_frame = tk.Frame(self.right_panel, bg="#F5F5F5")
        self.options_frame.pack(pady=10)
        
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", width=60, font=("Arial", 12),
                            command=lambda idx=i: self.select_option(idx))
            btn.pack(pady=5)
            self.option_buttons.append(btn)
            
        self.timer_lbl = tk.Label(self.right_panel, text="10", bg="#F5F5F5", fg="red", font=("Arial", 30, "bold"))
        self.timer_lbl.pack(pady=10)
        
        # Bottom row
        self.bottom_frame = tk.Frame(self.right_panel, bg="#F5F5F5")
        self.bottom_frame.pack(side="bottom", fill="x", pady=20, padx=20)
        
        self.prev_btn = tk.Button(self.bottom_frame, text="Previous", command=self.prev_question)
        self.prev_btn.pack(side="left")
        
        self.time_taken_lbl = tk.Label(self.bottom_frame, text="", bg="#F5F5F5", font=("Arial", 10))
        self.time_taken_lbl.pack(side="left", expand=True)
        
        self.next_btn = tk.Button(self.bottom_frame, text="Next", command=self.next_question)
        self.next_btn.pack(side="right")
        
    def load_question(self, index):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            
        self.current_q_index = index
        q = self.questions[index]
        
        self.progress_lbl.config(text=f"Question {index+1} of {len(self.questions)}")
        
        # Assign department label from JSON
        dept = q.get("department", "Universal AI University")
        self.dept_lbl.config(text=f"Q{index+1} - {dept}")
        self.q_text_lbl.config(text=q["question"])
        
        for i in range(4):
            if i < len(q["options"]):
                self.option_buttons[i].config(text=q["options"][i], bg="SystemButtonFace", state="normal")
            else:
                self.option_buttons[i].config(text="", state="disabled", bg="SystemButtonFace")
            
        # Check if already answered
        if index in self.responses:
            ans = self.responses[index]
            if ans["status"] == "expired":
                self.time_taken_lbl.config(text="Time Expired")
            else:
                self.time_taken_lbl.config(text=f"Answered in {ans['time_taken']} seconds")
                
            self.timer_lbl.config(text="-")
            for i in range(4):
                self.option_buttons[i].config(state="disabled")
                if i < len(q["options"]) and q["options"][i].startswith(q["answer"]):
                    self.option_buttons[i].config(bg="lightgreen")
        else:
            self.time_taken_lbl.config(text="")
            self.time_left = 10
            self.timer_lbl.config(text="10")
            self.start_time = time.time()
            self.timer_job = self.root.after(1000, self.update_timer)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_lbl.config(text=str(self.time_left))
            self.timer_job = self.root.after(1000, self.update_timer)
        else:
            self.timer_expired()
            
    def select_option(self, opt_index):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            
        time_taken = round(time.time() - self.start_time, 1)
        q = self.questions[self.current_q_index]
        selected_text = q["options"][opt_index]
        
        is_correct = selected_text.startswith(q["answer"])
        status = "correct" if is_correct else "wrong"
        
        self.responses[self.current_q_index] = {
            "q_id": self.current_q_index + 1,
            "time_taken": time_taken,
            "status": status
        }
        
        # Color nav button
        self.nav_buttons[self.current_q_index].config(bg="green" if is_correct else "red")
        
        # Color options
        for i in range(4):
            self.option_buttons[i].config(state="disabled")
            if i < len(q["options"]):
                if q["options"][i].startswith(q["answer"]):
                    self.option_buttons[i].config(bg="lightgreen")
                elif i == opt_index and not is_correct:
                    self.option_buttons[i].config(bg="salmon")
                
        self.time_taken_lbl.config(text=f"Answered in {time_taken} seconds")
        self.save_session()
        self.root.after(1000, self.next_question)
        
    def timer_expired(self):
        q = self.questions[self.current_q_index]
        self.responses[self.current_q_index] = {
            "q_id": self.current_q_index + 1,
            "time_taken": None,
            "status": "expired"
        }
        
        self.nav_buttons[self.current_q_index].config(bg="orange")
        
        for i in range(4):
            self.option_buttons[i].config(state="disabled")
            if i < len(q["options"]) and q["options"][i].startswith(q["answer"]):
                self.option_buttons[i].config(bg="lightgreen")
                
        self.time_taken_lbl.config(text="Time Expired")
        self.save_session()
        self.root.after(1000, self.next_question)
        
    def jump_to_question(self, index):
        self.load_question(index)
        
    def next_question(self):
        if self.current_q_index < len(self.questions) - 1:
            self.load_question(self.current_q_index + 1)
        else:
            messagebox.showinfo("Quiz Completed", "You have reached the end of the quiz.")
            
    def prev_question(self):
        if self.current_q_index > 0:
            self.load_question(self.current_q_index - 1)
            
    def save_session(self):
        os.makedirs("results", exist_ok=True)
        with open("results/session_log.json", "w") as f:
            json.dump(list(self.responses.values()), f, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = UAIQuizApp(root)
    root.mainloop()
