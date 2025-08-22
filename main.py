import ctypes
import json
import sys, os
import tkinter as tk
import random
import threading
from tkinter import ttk
from PIL import Image, ImageTk

def resource_path(relative_path):
    """ Get absolute path to resource (works for dev and PyInstaller .exe) """
    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("som.example.Dictionary")



# Constants
dictionaryDatabaseLink = "https://raw.githubusercontent.com/Nafisa41/Dictionary--English-to-Bangla-/master/Database/E2Bdatabase.json"
radix = 128
mod = 100000000003
primeForPrimaryHash = 103643


# ------------------ Dictionary Logic ------------------
class Dictionary:
    def __init__(self):
        self.words = []
        self.wordCount = 0
        self.hashtable = []
        self.hashtablekeys = []
        self.primaryHashA = None
        self.primaryHashB = None
        self.init()

    def init(self):
        self.hashtable = [[] for _ in range(primeForPrimaryHash)]
        self.hashtablekeys = [[] for _ in range(primeForPrimaryHash)]

    def calculateKeyvalue(self, element):
        value = 0
        for ch in element:
            value = ((value * radix) % mod + ord(ch)) % mod
        return value

    def calculateHashvalue(self, key):
        return (self.primaryHashA * key + self.primaryHashB) % primeForPrimaryHash

    def creatingPrimaryHashTable(self):
        self.init()
        self.primaryHashA = random.randint(1, mod - 1)
        self.primaryHashB = random.randint(0, mod - 1)
        for i, word in enumerate(self.words):
            key = self.calculateKeyvalue(word["en"])
            hashvalue = self.calculateHashvalue(key)
            self.hashtable[hashvalue].append(i)

    def creatingSecondaryHashTable(self):
        for i in range(primeForPrimaryHash):
            if len(self.hashtable[i]) == 1:
                self.hashtablekeys[i] = [1, 0, 1]
            elif len(self.hashtable[i]) > 1:
                self.calculateValueofABM(self.hashtable[i], i)

    def calculateValueofABM(self, wordarr, idx):
        m = len(wordarr) ** 2
        while True:
            arr = [-1] * m
            a = random.randint(1, mod - 1)
            b = random.randint(0, mod - 1)
            flag = True
            for word_idx in wordarr:
                key = self.calculateKeyvalue(self.words[word_idx]["en"])
                hashv = ((a * key) % mod + b) % mod
                hashv = hashv % m
                if arr[hashv] == -1:
                    arr[hashv] = word_idx
                else:
                    flag = False
                    break
            if flag:
                self.hashtablekeys[idx] = [a, b, m]
                self.hashtable[idx] = arr
                break

    def search(self, word):
        word = word.strip().lower()
        if not word:
            return None
        key = self.calculateKeyvalue(word)
        phash = self.calculateHashvalue(key)
        if not self.hashtablekeys[phash]:
            return None
        a, b, m = self.hashtablekeys[phash]
        hashv = ((a * key) % mod + b) % mod
        hashv = hashv % m
        i = self.hashtable[phash][hashv]
        if i >= 0 and self.words[i]["en"] == word:
            return self.words[i]["bn"]
        return None


# ------------------ Premium Tkinter UI ------------------
class DictionaryApp:
    def __init__(self, root):
        self.dictionary = Dictionary()
        self.root = root
        self.root.title("English ↔ বাংলা Dictionary")
        self.root.geometry("600x600")
        self.root.configure(bg="#1e1e2f")  # Dark background
        try:
            root.iconbitmap(resource_path(r"icons/icon.ico"))
        except Exception as e:
            pass
        
        # --- Load icons ---
        label_img = Image.open(resource_path(r"icons/label.png")).resize((40, 40))
        self.label_icon = ImageTk.PhotoImage(label_img)
        
        search_img = Image.open(resource_path(r"icons/search.png")).resize((40, 40))
        self.search_icon = ImageTk.PhotoImage(search_img)

        # --- Top Title ---
        top_frame = tk.Frame(root, bg="#1e1e2f")
        top_frame.pack(pady=10)  

        title2 = tk.Label(
            top_frame, image=self.label_icon,
            font=("Segoe UI", 20, "bold"), bg="#1e1e2f", fg="#00d9ff"
        )
        title2.pack(side="left", padx=10, pady=15)

        title1 = tk.Label(
            top_frame, text="English → বাংলা Dictionary",
            font=("Segoe UI", 20, "bold"), bg="#1e1e2f", fg="#00d9ff"
        )
        title1.pack(side="left", pady=15)

        # --- Search Frame ---
        search_frame = tk.Frame(root, bg="#1e1e2f")
        search_frame.pack(pady=10)

        self.entry = tk.Entry(
            search_frame, width=30, font=("Segoe UI", 14),
            bg="#2d2d44", fg="white", insertbackground="white", border=1,
        )
        self.entry.pack(side="left", padx=10, ipady=6)

        self.search_btn = tk.Button(
            search_frame, image=self.search_icon, command=self.search_word,
            font=("Segoe UI", 12, "bold"), bg="#1e1e2f", fg="black",
            relief="flat", padx=15, pady=5, activebackground="#00b0d9",
            state="disabled"
        )
        self.search_btn.pack(side="left")

        # --- Result Frame (with scrollable Text) ---
        result_frame = tk.Frame(root, bg="#1e1e2f")
        result_frame.pack(pady=20, fill="both", expand=True)

        self.result_text = tk.Text(
            result_frame,
            font=("Segoe UI", 16, "bold"),
            bg="#252538", fg="yellow", wrap="word",
            relief="flat", height=10
        )
        self.result_text.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)

        # make result area read-only
        self.result_text.bind("<Key>", lambda e: "break")
        self.result_text.bind("<MouseWheel>", lambda e: self.result_text.yview_scroll(-1*(e.delta//120), "units"))

        # --- Error Label ---
        self.error_label = tk.Label(
            root, text="", font=("Segoe UI", 12, "bold"),
            bg="#1e1e2f", fg="red"
        )
        self.error_label.pack(pady=5)

        # --- Popup suggestion window ---
        self.suggestion_window = None
        self.listbox = None

        # --- Start background thread for dictionary loading ---
        threading.Thread(target=self.load_dictionary, daemon=True).start()

        # --- Bind Keys ---
        self.entry.bind("<Return>", lambda event: self.search_word())
        self.entry.bind("<KeyRelease>", self.show_suggestions)
        self.root.bind("<Button-1>", self.on_click_outside)


    def on_click_outside(self, event):
        
        if self.suggestion_window and self.suggestion_window.winfo_exists():
            widget = event.widget
            
            if widget not in (self.entry, self.listbox):
                self.hide_suggestions()
                
    def load_dictionary(self):
        try:
            # Load from bundled path
            file_path = resource_path("Database/E2Bdatabase.json")
            with open(file_path, "r", encoding="utf-8") as f:
                words = json.load(f)

            self.dictionary.words = words
            self.dictionary.wordCount = len(words)
            self.dictionary.creatingPrimaryHashTable()
            self.dictionary.creatingSecondaryHashTable()
            self.search_btn.config(state="normal")
        except Exception as e:
            
            self.result_text.config(state="normal")   
            self.result_text.delete(1.0, tk.END)     
            self.result_text.insert(tk.END, f"❌ Failed to load dictionary\n{e}")
            self.result_text.tag_config("error", foreground="red")  
            self.result_text.tag_add("error", "1.0", "end")
            self.result_text.config(state="disabled") 
            
    def search_word(self, e=None):
        text = self.entry.get().strip().lower()
        if not text:
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "❌ Please type something!")
            self.result_text.config(fg="red", state="disabled")
            return

        words = text.split()
        translated_words = []

        for word in words:
            meaning = self.dictionary.search(word)
            if meaning:
                translated_words.append(meaning)
            else:
                translated_words.append(f"[{word}]")

        translated_sentence = " ".join(translated_words)

        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, translated_sentence)
        self.result_text.config(fg="#00ff99", state="disabled")

        self.hide_suggestions()


    def show_suggestions(self, event=None):
        if event and event.keysym in ("Up", "Down", "Return", "Escape"):
            return

        text = self.entry.get().strip().lower()
        if not text or not self.dictionary.words:
            self.hide_suggestions()
            return

        matches = [w["en"] for w in self.dictionary.words if w["en"].startswith(text)]

        if not matches:
            self.hide_suggestions()
            return

        matches_sorted = sorted(set(matches))   
        if text in matches_sorted:
            matches_sorted.remove(text)
        suggestions = [text] + matches_sorted   

        # Create popup if not exists
        if not self.suggestion_window or not self.suggestion_window.winfo_exists():
            self.suggestion_window = tk.Toplevel(self.root)
            self.suggestion_window.overrideredirect(True)
            self.suggestion_window.config(bg="#2d2d44")

            frame = tk.Frame(self.suggestion_window, bg="#2d2d44")
            frame.pack()

            self.listbox = tk.Listbox(
                frame, width=30, height=8, font=("Segoe UI", 12),
                bg="#2d2d44", fg="white", relief="flat", highlightthickness=1,
                selectbackground="#00d9ff", selectforeground="black",
                activestyle="none"
            )
            self.listbox.pack(side="left", fill="both")

            style = ttk.Style()
            style.theme_use("clam") 
            style.configure("Vertical.TScrollbar",
                            gripcount=0,
                            background="#1aa6f1",     # scrollbar background
                            darkcolor="#1aa6f1",      # darker border color
                            lightcolor="#1aa6f1",     # lighter border color
                            troughcolor="#3e3eca", # track color
                            bordercolor="#2626b7",
                            arrowcolor="#2929a3")  # hide arrows by blending

            # Remove the arrow buttons → only the slider/thumb remains
            style.layout("Vertical.TScrollbar",
                        [('Vertical.Scrollbar.trough',
                        {'children': [('Vertical.Scrollbar.thumb',
                                        {'expand': '1', 'sticky': 'nswe'})],
                            'sticky': 'ns'})])

            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.listbox.yview,
                                    style="Vertical.TScrollbar")
            scrollbar.pack(side="right", fill="y")
            self.listbox.config(yscrollcommand=scrollbar.set)

            self.listbox.bind("<MouseWheel>", lambda e: self.listbox.yview_scroll(-1*(e.delta//120), "units"))
            self.listbox.bind("<Return>", self.fill_entry)
            self.listbox.bind("<Escape>", lambda e: self.hide_suggestions())
            self.entry.bind("<Down>", lambda e: self.move_selection("down"))
            self.entry.bind("<Up>", lambda e: self.move_selection("up"))
            self.entry.bind("<Escape>", lambda e: self.hide_suggestions())
            self.entry.bind("<Return>", self.handle_enter)

        # ✅ Update listbox
        self.listbox.delete(0, tk.END)
        for s in suggestions:
            self.listbox.insert(tk.END, s)

        # Place popup below entry
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        self.suggestion_window.geometry(f"+{x}+{y}")

        # Always select first by default
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(0)
        self.listbox.activate(0)

    def handle_enter(self, event=None):
        if self.suggestion_window and self.suggestion_window.winfo_exists():
            self.fill_entry()   # pick suggestion
        else:
            self.search_word()  # search directly

    def hide_suggestions(self, event=None):
        if self.suggestion_window and self.suggestion_window.winfo_exists():
            self.suggestion_window.destroy()
            self.suggestion_window = None
            self.listbox = None
        self.entry.focus_set()

    def move_selection(self, direction):
        if not self.listbox:
            return
        cur = self.listbox.curselection()
        if not cur:
            idx = 0
        else:
            idx = cur[0]
            if direction == "down":
                idx = (idx + 1) % self.listbox.size()
            elif direction == "up":
                idx = (idx - 1) % self.listbox.size()

        # ✅ Update selection
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(idx)
        self.listbox.activate(idx)

        # ✅ Ensure highlighted item is visible (scrolls if needed)
        self.listbox.see(idx)

    def fill_entry(self, event=None):
        if not self.listbox or not self.listbox.curselection():
            return
        selected = self.listbox.get(self.listbox.curselection())
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected)
        self.search_word()


def main():
    
    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("som.example.Dictionary")


    root = tk.Tk()
    try:
        root.iconbitmap(resource_path(r"icons/icon.ico"))

    except Exception as e:
        pass

    app = DictionaryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
