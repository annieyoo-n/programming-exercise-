import tkinter as tk
import random

class AlexaJokes:
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 Alexa Joke Teller")
        self.root.geometry("700x600")
        self.root.configure(bg="#1a0b2e")
        
        self.jokes = [
            "Why did the chicken cross the road?To get to the other side.",
            "What happens if you boil a clown?You get a laughing stock.",
            "Why don't scientists trust atoms?Because they make up everything.",
            "What do you call a bear with no teeth?A gummy bear.",
            "Why did the scarecrow win an award?He was outstanding in his field.",
            "What do you call fake spaghetti?An impasta.",
            "Why don't eggs tell jokes?They'd crack each other up.",
            "What did the ocean say to the beach?Nothing, it just waved.",
            "Why did the math book look sad?It had too many problems.",
            "What do you call a dinosaur that crashes his car?Tyrannosaurus Wrecks."
        ]
        
        self.current_setup = ""
        self.current_punchline = ""
        self.showing_punchline = False
        self.createUI()
    
    def createUI(self):
        canvas = tk.Canvas(self.root, width=700, height=600, bg="#1a0b2e", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Gradient circles background
        for i in range(5):
            x = random.randint(50, 650)
            y = random.randint(50, 550)
            size = random.randint(100, 200)
            colors = ["#4a148c", "#6a1b9a", "#7b1fa2", "#8e24aa", "#9c27b0"]
            canvas.create_oval(x, y, x+size, y+size, fill=colors[i], outline="", stipple="gray50")
        
        # Title
        canvas.create_text(350, 80, text="🎭 ALEXA JOKE TELLER 🎭", 
                          font=("Arial", 28, "bold"), fill="#bb86fc")
        
        # Input frame
        self.input_frame = tk.Frame(self.root, bg="#2d1b69", bd=3, relief=tk.RAISED)
        self.input_frame.place(x=100, y=150, width=500, height=80)
        
        self.input_entry = tk.Entry(self.input_frame, font=("Arial", 16), bg="#1a0b2e", 
                                    fg="#bb86fc", insertbackground="#bb86fc", justify="center")
        self.input_entry.pack(pady=10, padx=20, fill="x")
        self.input_entry.insert(0, "Type: Alexa tell me a joke")
        self.input_entry.bind('<Return>', lambda e: self.processInput())
        self.input_entry.bind('<FocusIn>', lambda e: self.input_entry.delete(0, tk.END))
        
        tk.Button(self.input_frame, text="ASK", font=("Arial", 12, "bold"), 
                 bg="#7b1fa2", fg="white", command=self.processInput).pack()
        
        # Joke display
        self.joke_frame = tk.Frame(self.root, bg="#2d1b69", bd=3, relief=tk.RAISED)
        self.joke_frame.place(x=80, y=270, width=540, height=220)
        
        self.joke_label = tk.Label(self.joke_frame, text="👋 Hi! Ask me for a joke!", 
                                   font=("Arial", 18), bg="#2d1b69", fg="#bb86fc", 
                                   wraplength=500, justify="center")
        self.joke_label.pack(expand=True)
        
        # Action button
        self.action_btn = tk.Button(self.root, text="", font=("Arial", 14, "bold"),
                                    bg="#6a1b9a", fg="white", width=20, height=2, state=tk.DISABLED)
        self.action_btn.place(x=220, y=510)
        
        # Quit button
        tk.Button(self.root, text="QUIT", font=("Arial", 12, "bold"), 
                 bg="#4a148c", fg="white", width=10, command=self.root.quit).place(x=300, y=555)
    
    def processInput(self):
        user_input = self.input_entry.get().lower()
        if "alexa" in user_input and "joke" in user_input:
            self.tellJoke()
        else:
            self.joke_label.config(text="🤔 Try saying:\n'Alexa tell me a joke'")
        self.input_entry.delete(0, tk.END)
    
    def tellJoke(self):
        joke = random.choice(self.jokes)
        parts = joke.split("?")
        self.current_setup = parts[0] + "?"
        self.current_punchline = parts[1] if len(parts) > 1 else ""
        
        self.joke_label.config(text=f"😄 {self.current_setup}", font=("Arial", 20, "bold"))
        self.action_btn.config(text="SHOW PUNCHLINE", state=tk.NORMAL, command=self.showPunchline)
        self.showing_punchline = False
    
    def showPunchline(self):
        if not self.showing_punchline:
            self.joke_label.config(text=f"🤣 {self.current_punchline}", font=("Arial", 18))
            self.action_btn.config(text="TELL ANOTHER JOKE", command=self.tellJoke)
            self.showing_punchline = True

if __name__ == "__main__":
    root = tk.Tk()
    app = AlexaJokes(root)
    root.mainloop()