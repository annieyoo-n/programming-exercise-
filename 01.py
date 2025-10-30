import tkinter as tk
from tkinter import messagebox
import random

class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Arithmetic Quiz")
        self.root.geometry("600x500")
        self.root.configure(bg="#1a1a2e")
        self.score = self.question_num = self.attempt = 0
        self.total_questions = 10
        self.difficulty = self.current_answer = None
        self.displayMenu()
    
    def displayMenu(self):
        """Displaying the menu, I made it aesthetic 😎..."""
        self.clearScreen()
        canvas = tk.Canvas(self.root, width=600, height=500, bg="#1a1a2e", highlightthickness=0)
        canvas.pack()
        
        title = canvas.create_text(300, 80, text="ARITHMETIC QUIZ", 
                                  font=("Arial", 32, "bold"), fill="#2ba4bc")
        self.animate(canvas, title, "pulse")
        canvas.create_text(300, 140, text="✨ DIFFICULTY LEVEL ✨", 
                          font=("Arial", 18, "bold"), fill="#c96648")
        
        buttons = [
            {"text": "🟢 EASY", "y": 220, "color": "#559F74", "diff": 1},
            {"text": "🟡 MODERATE", "y": 310, "color": "#870b12", "diff": 2},
            {"text": "🔴 ADVANCED", "y": 400, "color": "#9a5990", "diff": 3}
        ]
        
        for btn in buttons:
            rect = canvas.create_rectangle(150, btn["y"]-25, 450, btn["y"]+25, 
                                          fill=btn["color"], outline="white", width=2)
            text = canvas.create_text(300, btn["y"], text=btn["text"], 
                                     font=("Arial", 16, "bold"), fill="white")
            canvas.tag_bind(rect, "<Button-1>", lambda e, d=btn["diff"]: self.startQuiz(d))
            canvas.tag_bind(text, "<Button-1>", lambda e, d=btn["diff"]: self.startQuiz(d))
            canvas.tag_bind(rect, "<Enter>", lambda e, r=rect: canvas.itemconfig(r, width=4))
            canvas.tag_bind(rect, "<Leave>", lambda e, r=rect: canvas.itemconfig(r, width=2))
    
    def randomInt(self, difficulty):
        
        ranges = {1: (0, 9), 2: (10, 99), 3: (1000, 9999)}
        return random.randint(*ranges[difficulty])
    
    def decideOperation(self):

        return random.choice(['+', '-'])
    
    def startQuiz(self, difficulty):
        """Starting the QUIZ 🚀 """
        self.difficulty = difficulty
        self.score = self.question_num = 0
        self.displayProblem()
    
    def displayProblem(self):
        
        self.clearScreen()
        
        if self.question_num >= self.total_questions:
            self.displayResults()
            return
        
        self.question_num += 1
        self.attempt = 1
        
        num1, num2 = self.randomInt(self.difficulty), self.randomInt(self.difficulty)
        operation = self.decideOperation()
        self.current_answer = num1 + num2 if operation == '+' else num1 - num2
        
        canvas = tk.Canvas(self.root, width=600, height=500, bg="#1a1a2e", highlightthickness=0)
        canvas.pack()
        
        # Progress bar with animation
        progress = (self.question_num / self.total_questions) * 500
        canvas.create_rectangle(50, 30, 550, 50, fill="#2c3e50", outline="#34495e")
        bar = canvas.create_rectangle(50, 30, 50, 50, fill="#00d4ff", outline="")
        self.animate(canvas, bar, "slide", 50 + progress)
        
        canvas.create_text(300, 80, text=f"Question {self.question_num}/{self.total_questions}", 
                          font=("Arial", 16, "bold"), fill="#d4c469")
        canvas.create_text(300, 110, text=f"💰 Score: {self.score}/100", 
                          font=("Arial", 18, "bold"), fill="#70b88e")
        
        # Problem with animation
        canvas.create_rectangle(100, 160, 500, 280, fill="#16213e", outline="#5ab4c6", width=3)
        problem = canvas.create_text(300, 220, text=f"{num1} {operation} {num2} =", 
                                    font=("Arial", 40, "bold"), fill="#ffffff")
        self.animate(canvas, problem, "scale")
        
        # Entry and button
        self.answer_entry = tk.Entry(self.root, font=("Arial", 24, "bold"), width=12, 
                                    justify="center", bg="#0f3460", fg="#258fa4", 
                                    insertbackground="#1c7587", relief=tk.FLAT, bd=5)
        self.answer_entry.place(x=200, y=310)
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())
        
        tk.Button(self.root, text="✓ SUBMIT", font=("Arial", 16, "bold"), 
                 bg="#6a1209", fg="white", width=18, height=2, relief=tk.FLAT,
                 command=self.checkAnswer).place(x=150, y=400)
        
        # Particles
        for _ in range(8):
            x, y = random.randint(50, 550), random.randint(100, 500)
            color = random.choice(["#0e6273", "#918852", "#409463"])
            p = canvas.create_oval(x, y, x+3, y+3, fill=color, outline="")
            self.animate(canvas, p, "float")
    
    def checkAnswer(self):
        """Check the answer 🙏🏻 """
        try:
            user_answer = int(self.answer_entry.get())
            self.isCorrect(user_answer)
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid number!")
            self.answer_entry.delete(0, tk.END)
    
    def isCorrect(self, user_answer):
        """Validate the answer 💪🏻"""
        if user_answer == self.current_answer:
            points = 10 if self.attempt == 1 else 5
            self.score += points
            messagebox.showinfo("🎉 CORRECT!", f"+{points} points\n💰 Score: {self.score}")
            self.displayProblem()
        else:
            if self.attempt == 1:
                self.attempt = 2
                messagebox.showwarning("❌ WRONG", f"Correct: {self.current_answer}\nTry again!")
                self.answer_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("❌ WRONG", f"Correct: {self.current_answer}\nNo points")
                self.displayProblem()
    
    def displayResults(self):
        """Display final results 😊"""
        self.clearScreen()
        canvas = tk.Canvas(self.root, width=600, height=500, bg="#1a1a2e", highlightthickness=0)
        canvas.pack()
        
        # Fireworks
        for _ in range(12):
            x, y = random.randint(100, 500), random.randint(100, 400)
            color = random.choice(["#7a0b0b", "#baae69", "#1A859B", "#2ecc71"])
            for angle in range(0, 360, 45):
                import math
                dx = math.cos(math.radians(angle)) * 1.5
                dy = math.sin(math.radians(angle)) * 1.5
                p = canvas.create_oval(x, y, x+4, y+4, fill=color, outline="")
                self.animate(canvas, p, "firework", dx, dy)
        
        title = canvas.create_text(300, 80, text="🎊 QUIZ COMPLETE! 🎊", 
                                  font=("Arial", 28, "bold"), fill="#7757b8")
        self.animate(canvas, title, "pulse")
        
        canvas.create_oval(200, 140, 400, 240, fill="#16213e", outline="#7ad4e6", width=4)
        canvas.create_text(300, 190, text=f"{self.score}/100", 
                          font=("Arial", 36, "bold"), fill="#1093ad")
        
        # Ranking
        ranks = {90: ("A+", "#59A64F", "🏆"), 80: ("A", "#97d6b1", "🥇"), 
                70: ("B", "#856cb3", "🥈"), 60: ("C", "#784aa7", "🥉")}
        rank, color, emoji = next((v for k, v in ranks.items() if self.score >= k), 
                                  ("D", "#A03939", "📚"))
        
        rank_text = canvas.create_text(300, 260, text=f"{emoji} Rank: {rank} {emoji}", 
                                      font=("Arial", 32, "bold"), fill=color)
        self.animate(canvas, rank_text, "scale")
        
        tk.Button(self.root, text="🔄 PLAY AGAIN", font=("Arial", 14, "bold"), 
                 bg="#0a4872", fg="white", width=14, height=2, relief=tk.FLAT,
                 command=self.displayMenu).place(x=120, y=380)
        tk.Button(self.root, text="👋 QUIT", font=("Arial", 14, "bold"), 
                 bg="#3f797d", fg="white", width=14, height=2, relief=tk.FLAT,
                 command=self.root.quit).place(x=320, y=380)
    
    def animate(self, canvas, item, anim_type, *args):
       
        def pulse(scale=1.0, growing=True):
            if growing:
                scale += 0.02
                growing = scale < 1.15
            else:
                scale -= 0.02
                growing = scale <= 1.0
            try:
                canvas.scale(item, 300, 100, 1.02 if growing else 0.98, 1.02 if growing else 0.98)
                self.root.after(50, lambda: pulse(scale, growing))
            except: pass
        
        def scale(s=0.1):
            if s < 1.0:
                try:
                    canvas.scale(item, 300, 220, 1.1, 1.1)
                    self.root.after(30, lambda: scale(s + 0.1))
                except: pass
        
        def slide(end, current=50):
            if current < end:
                try:
                    coords = canvas.coords(item)
                    canvas.coords(item, coords[0], coords[1], current, coords[3])
                    self.root.after(10, lambda: slide(end, current + 5))
                except: pass
        
        def float():
            try:
                canvas.move(item, random.randint(-1, 1), -2)
                coords = canvas.coords(item)
                if coords[1] < 0:
                    canvas.coords(item, coords[0], 500, coords[2], 505)
                self.root.after(50, float)
            except: pass
        
        def firework(dx, dy, step=0):
            if step < 20:
                try:
                    canvas.move(item, dx, dy)
                    self.root.after(30, lambda: firework(dx, dy, step + 1))
                except: pass
            else:
                try: canvas.delete(item)
                except: pass
        
        animations = {"pulse": pulse, "scale": scale, "slide": lambda: slide(args[0]), 
                     "float": float, "firework": lambda: firework(args[0], args[1])}
        animations[anim_type]()
    
    def clearScreen(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()