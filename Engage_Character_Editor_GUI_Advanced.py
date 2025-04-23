
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re

GROWTH_KEYS = [
    "Grow.Hp", "Grow.Str", "Grow.Magic", "Grow.Tech", "Grow.Quick",
    "Grow.Luck", "Grow.Def", "Grow.Mdef", "Grow.Phys", "Grow.Sight", "Grow.Move"
]
BASE_KEYS = [
    "OffsetN.Hp", "OffsetN.Str", "OffsetN.Magic", "OffsetN.Tech", "OffsetN.Quick",
    "OffsetN.Luck", "OffsetN.Def", "OffsetN.Mdef", "OffsetN.Phys", "OffsetN.Sight", "OffsetN.Move"
]
LIMIT_KEYS = [
    "Limit.Hp", "Limit.Str", "Limit.Magic", "Limit.Tech", "Limit.Quick",
    "Limit.Luck", "Limit.Def", "Limit.Mdef", "Limit.Phys", "Limit.Sight", "Limit.Move"
]
OTHER_KEYS = ["Level", "InternalLevel", "SupportCategory", "SkillPoint",  "Attrs"]
ALL_KEYS = GROWTH_KEYS + BASE_KEYS + LIMIT_KEYS + OTHER_KEYS

class PersonDataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Fire Emblem Engage Character Editor")
        self.data = []
        self.text = ""
        self.current_index = 0
        self.entries = {}
        self.build_ui()

    def build_ui(self):
        tk.Button(self.root, text="Open .txt File", command=self.load_file).pack(pady=5)
        self.char_selector = ttk.Combobox(self.root, state="readonly")
        self.char_selector.bind("<<ComboboxSelected>>", self.on_character_selected)
        self.char_selector.pack(pady=5)


        display_names = {
            "Grow.Quick": "Grow.Speed",
            "OffsetN.Quick": "OffsetN.Speed",
            "Limit.Quick": "Limit.Speed",
            "Grow.Tech": "Grow.Dexterity",
            "OffsetN.Tech": "OffsetN.Dexterity",
            "Limit.Tech": "Limit.Dexterity",
            "Grow.Mdef": "Grow.Resistance",
            "OffsetN.Mdef": "OffsetN.Resistance",
            "Limit.Mdef": "Limit.Resistance",
            "Grow.Phys": "Grow.Build",
            "OffsetN.Phys": "OffsetN.Build",
            "Limit.Phys": "Limit.Build",
            "Grow.Sight": "Grow.Vision",
            "OffsetN.Sight": "OffsetN.Vision",
            "Limit.Sight": "Limit.Vision",
            "Grow.Move": "Grow.Movement",
            "OffsetN.Move": "OffsetN.Movement",
            "Limit.Move": "Limit.Movement"
        }

        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, fill='both', expand=True)

        self.tabs = {}
        for category, keys in {
            "Growths": GROWTH_KEYS,
            "Base Stats": BASE_KEYS,
            "Limits": LIMIT_KEYS,
            "Other": OTHER_KEYS
        }.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=category)
            self.tabs[category] = frame
            for key in keys:
                row = tk.Frame(frame)
                row.pack(fill="x", pady=2)
                tk.Label(row, text=display_names.get(key, key), width=20, anchor="w").pack(side="left")
                
                entry = tk.Entry(row)
                entry.pack(side="right", expand=True, fill="x")
                self.entries[key] = entry


        tk.Button(self.root, text="Save Changes", command=self.save_changes).pack(pady=5)
        tk.Button(self.root, text="Save to File", command=self.write_to_file).pack(pady=5)

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            self.text = f.read()
        self.file_path = path
        self.data = []
        pattern = re.compile(r'<Param[^<>]*?/>', re.DOTALL)
        for match in pattern.finditer(self.text):
            block = match.group()
            if "Pid=" not in block:
                continue
            attrs = dict(re.findall(r'(\w+(?:\.\w+)*)="([^"]*)"', block))
            pid = attrs.get("Pid", "")
            if not pid:
                continue
            attrs["__original"] = block
            attrs["__span"] = match.span()
            self.data.append(attrs)
        if self.data:
            self.char_selector["values"] = [entry.get("Name", entry.get("Pid", f"Character {i}")) for i, entry in enumerate(self.data)]
            self.char_selector.current(0)
            self.show_character(0)
        else:
            self.char_selector["values"] = []
            messagebox.showerror("Error", "No characters found in the file.")

    def on_character_selected(self, event):
        name = self.char_selector.get()
        for i, entry in enumerate(self.data):
            if name == entry.get("Name", entry.get("Pid", f"Character {i}")):
                self.show_character(i)
                break

    def show_character(self, index):
        self.current_index = index
        char = self.data[index]
        for key in ALL_KEYS:
            widget = self.entries.get(key)
            if widget:
                widget.delete(0, tk.END)
                widget.insert(0, char.get(key, ""))

    def save_changes(self):
        char = self.data[self.current_index]
        for key in ALL_KEYS:
            char[key] = self.entries[key].get()
        parts = [f'{k}="{v}"' for k, v in char.items() if not k.startswith("__")]
        new_block = "    <Param " + " ".join(parts) + " />"
        start, end = char["__span"]
        self.text = self.text[:start] + new_block + self.text[end:]
        char["__original"] = new_block
        char["__span"] = (start, start + len(new_block))

    def write_to_file(self):
        if not self.file_path:
            return
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(self.text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonDataEditor(root)
    root.mainloop()