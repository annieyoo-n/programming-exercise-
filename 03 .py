
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pathlib, math

FILE = pathlib.Path(r"C:\Users\zulfi\Documents\OneDrive\Desktop\VSC\AS 01\studentMarks.txt")

# Data functions
def load():
    if not FILE.exists(): FILE.write_text("0\n")
    with FILE.open() as f:
        n = int(f.readline())
        rows = [line.strip().split(',') for line in f if line.strip()]
    return [{"id": int(r[0]), "name": r[1], "cw": list(map(int, r[2:5])), "ex": int(r[5])} for r in rows]

def save(studs):
    with FILE.open('w') as f:
        f.write(f"{len(studs)}\n")
        for s in studs: f.write(f"{s['id']},{s['name']},{s['cw'][0]},{s['cw'][1]},{s['cw'][2]},{s['ex']}\n")

def total(s): return sum(s["cw"]) + s["ex"]
def pct(s): return round(total(s)/160*100, 1)
def grade(p): return "A" if p>=70 else "B" if p>=60 else "C" if p>=50 else "D" if p>=40 else "F"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Marks Manager")
        self.geometry("900x600")
        self.configure(bg="#0f0f23")
        self.studs = load()
        self._style()
        self._build_ui()
        self._fade_in()
        self.refresh()

    def _style(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        # Purple/Blue theme
        bg, fg, accent = "#0f0f23", "#e0e0ff", "#9d4edd"
        self.style.configure("Treeview", background="#1a1a35", fieldbackground="#1a1a35", 
                           foreground=fg, borderwidth=0, rowheight=28)
        self.style.map("Treeview", background=[("selected", accent)])
        self.style.configure("TButton", background="#2a2a50", foreground=fg, borderwidth=0, 
                           focuscolor="none", padding=8, font=("Segoe UI", 9))
        self.style.map("TButton", background=[("active", accent)], foreground=[("active", "#fff")])
        self.style.configure("Update.TButton", background="#7209b7", foreground="#fff", padding=10)
        self.style.map("Update.TButton", background=[("active", "#9d4edd")])

    def _build_ui(self):
        # Header
        head = tk.Frame(self, bg="#0f0f23")
        head.pack(fill="x", padx=20, pady=10)
        title = tk.Label(head, text="Student Marks Manager", fg="#9d4edd", bg="#0f0f23", 
                font=("Segoe UI", 24, "bold"))
        title.pack(side="left")
        self._animate_title(title)
        
        # Top buttons 😎
        for txt, cmd in [("View All", self.view_all), ("View One", self.view_one),
                         ("Highest", self.highest), ("Lowest", self.lowest),
                         ("Sort", self.sort_studs), ("Add", self.add_stud), ("Delete", self.del_stud)]:
            btn = ttk.Button(head, text=txt, command=cmd)
            btn.pack(side="left", padx=6)
            self._add_btn_hover(btn)
        
        # Tree 🌲
        wrap = tk.Frame(self, bg="#0f0f23")
        wrap.pack(fill="both", expand=True, padx=20, pady=10)
        cols = ("ID", "Name", "CW", "Exam", "Total", "%", "Grade")
        self.tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90 if c != "Name" else 180)
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.bind("<Motion>", self._hover_row)
        
        # Bottom Update button
        bottom = tk.Frame(self, bg="#0f0f23")
        bottom.pack(fill="x", padx=20, pady=15)
        upd_btn = ttk.Button(bottom, text="🔄 Update Student", command=self.update_stud, 
                            style="Update.TButton")
        upd_btn.pack(side="right")
        self._add_btn_hover(upd_btn, scale=1.05)

    # Animations 🌏
    def _fade_in(self, alpha=0):
        if alpha <= 1:
            self.attributes("-alpha", alpha)
            self.after(20, self._fade_in, alpha + 0.05)

    def _animate_title(self, label, step=0):
        colors = ["#9d4edd", "#c77dff", "#e0aaff", "#c77dff", "#9d4edd"]
        label.config(fg=colors[step % len(colors)])
        self.after(300, self._animate_title, label, step + 1)

    def _add_btn_hover(self, btn, scale=1.02):
        def on_enter(e):
            btn.configure(cursor="hand2")
            btn.state(['active'])
        def on_leave(e):
            btn.state(['!active'])
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _hover_row(self, event):
        item = self.tree.identify_row(event.y)
        if item and hasattr(self, '_last_hover') and item != self._last_hover:
            # Remove hover from previous item
            if self._last_hover:
                tags = list(self.tree.item(self._last_hover, 'tags'))
                if 'hover' in tags:
                    tags.remove('hover')
                self.tree.item(self._last_hover, tags=tags)
        if item:
            # Add hover to current item
            tags = list(self.tree.item(item, 'tags'))
            if 'hover' not in tags:
                tags.append('hover')
            self.tree.item(item, tags=tags)
            self.tree.tag_configure("hover", background="#2a2a50")
            self._last_hover = item

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for s in self.studs:
            vals = (s["id"], s["name"], sum(s["cw"]), s["ex"], total(s), pct(s), grade(pct(s)))
            item = self.tree.insert("", "end", values=vals)
            # Color code by grade
            g = grade(pct(s))
            if g == "A": self.tree.item(item, tags=("excellent",))
            elif g == "F": self.tree.item(item, tags=("failing",))
        self.tree.tag_configure("excellent", foreground="#7fff00")
        self.tree.tag_configure("failing", foreground="#ff6b6b")
        self.title(f"Student Marks – {len(self.studs)} students")

    def view_all(self): self.refresh()

    def view_one(self):
        s = self._selected()
        if s: self._popup("Student Record", "\n".join(self._detail(s)))

    def highest(self):
        if self.studs: self._popup("Highest Score 🏆", "\n".join(self._detail(max(self.studs, key=total))))

    def lowest(self):
        if self.studs: self._popup("Lowest Score", "\n".join(self._detail(min(self.studs, key=total))))

    def sort_studs(self):
        rev = messagebox.askyesno("Sort", "Descending order?")
        self.studs.sort(key=lambda s: pct(s), reverse=rev)
        self.refresh()

    def add_stud(self):
        try:
            sid = simpledialog.askinteger("Add", "ID (1000-9999)", minvalue=1000, maxvalue=9999)
            if sid is None: return
            if any(s["id"]==sid for s in self.studs): 
                messagebox.showerror("Error", "ID already exists")
                return
            name = simpledialog.askstring("Add", "Name")
            if not name: return
            cw = [simpledialog.askinteger("Add", f"CW{i+1} (0-20)", minvalue=0, maxvalue=20) 
                  for i in range(3)]
            ex = simpledialog.askinteger("Add", "Exam (0-100)", minvalue=0, maxvalue=100)
            self.studs.append({"id": sid, "name": name, "cw": cw, "ex": ex})
            self.refresh()
            save(self.studs)
            messagebox.showinfo("Success", f"Added {name} successfully! ✓")
        except: messagebox.showerror("Error", "Invalid input")

    def del_stud(self):
        s = self._selected()
        if s and messagebox.askyesno("Delete", f"Remove {s['name']}?"):
            self.studs.remove(s)
            self.refresh()
            save(self.studs)
            messagebox.showinfo("Deleted", "Student removed successfully")

    def update_stud(self):
        s = self._selected()
        if not s: return
        c = simpledialog.askinteger("Update", "1=Name  2=CW1  3=CW2  4=CW3  5=Exam", 
                                   minvalue=1, maxvalue=5)
        if not c: return
        if c == 1:
            new = simpledialog.askstring("Update", "New name", initialvalue=s["name"])
            if new: s["name"] = new
        else:
            idx = c-2
            key = "cw" if idx < 3 else "ex"
            current = s[key][idx] if key == "cw" else s[key]
            maxval = 20 if key == "cw" else 100
            new = simpledialog.askinteger("Update", f"New value (0-{maxval})", 
                                        minvalue=0, maxvalue=maxval, initialvalue=current)
            if new is not None:
                if key == "cw": s[key][idx] = new
                else: s[key] = new
        self.refresh()
        save(self.studs)
        messagebox.showinfo("Updated", "Changes saved successfully! ✓")

    def _selected(self):
        if not self.tree.selection():
            messagebox.showwarning("Select", "Please select a student")
            return None
        sid = int(self.tree.item(self.tree.selection()[0])["values"][0])
        return next(s for s in self.studs if s["id"] == sid)

    def _detail(self, s):
        p = pct(s)
        return [f"📝 {s['name']} ({s['id']})", f"📚 Coursework: {sum(s['cw'])}/60",
                f"📄 Exam: {s['ex']}/100", f"🎯 Overall: {p}% | Grade: {grade(p)}"]

    def _popup(self, title, text):
        top = tk.Toplevel(self)
        top.title(title)
        top.configure(bg="#0f0f23")
        top.geometry("350x200")
        top.attributes("-alpha", 0)
        tk.Label(top, text=text, fg="#e0e0ff", bg="#0f0f23", justify="left", 
                font=("Segoe UI", 11)).pack(padx=20, pady=30)
        btn = ttk.Button(top, text="Close", command=top.destroy)
        btn.pack(pady=10)
        self._add_btn_hover(btn)
        # Fade in popup
        def fade(a=0):
            if a <= 1:
                top.attributes("-alpha", a)
                top.after(15, fade, a + 0.1)
        fade()

if __name__ == "__main__":

    App().mainloop()
