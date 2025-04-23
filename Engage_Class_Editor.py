import tkinter as tk
import html  # used to safely escape XML values
from tkinter import filedialog, ttk, messagebox
import re
import os

GROWTH_KEYS = [
    "BaseGrow.Hp", "DiffGrow.Hp", "DiffGrowNormal.Hp", "DiffGrowHard.Hp", "DiffGrowLunatic.Hp",
    "BaseGrow.Str", "DiffGrow.Str", "DiffGrowNormal.Str", "DiffGrowHard.Str", "DiffGrowLunatic.Str",
    "BaseGrow.Magic", "DiffGrow.Magic", "DiffGrowNormal.Magic", "DiffGrowHard.Magic", "DiffGrowLunatic.Magic",
    "BaseGrow.Tech", "DiffGrow.Tech", "DiffGrowNormal.Tech", "DiffGrowHard.Tech", "DiffGrowLunatic.Tech",
    "BaseGrow.Quick", "DiffGrow.Quick", "DiffGrowNormal.Quick", "DiffGrowHard.Quick", "DiffGrowLunatic.Quick",
    "BaseGrow.Luck", "DiffGrow.Luck", "DiffGrowNormal.Luck", "DiffGrowHard.Luck", "DiffGrowLunatic.Luck",
    "BaseGrow.Def", "DiffGrow.Def", "DiffGrowNormal.Def", "DiffGrowHard.Def", "DiffGrowLunatic.Def",
    "BaseGrow.Mdef", "DiffGrow.Mdef", "DiffGrowNormal.Mdef", "DiffGrowHard.Mdef", "DiffGrowLunatic.Mdef",
    "BaseGrow.Phys", "DiffGrow.Phys", "DiffGrowNormal.Phys", "DiffGrowHard.Phys", "DiffGrowLunatic.Phys",
    "BaseGrow.Sight", "DiffGrow.Sight", "DiffGrowNormal.Sight", "DiffGrowHard.Sight", "DiffGrowLunatic.Sight",
    "BaseGrow.Move", "DiffGrow.Move", "DiffGrowNormal.Move", "DiffGrowHard.Move", "DiffGrowLunatic.Move"
]
BASE_KEYS = [
    "Base.Hp", "Base.Str", "Base.Magic", "Base.Tech", "Base.Quick",
    "Base.Luck", "Base.Def", "Base.Mdef", "Base.Phys", "Base.Sight", "Base.Move"
]
LIMIT_KEYS = [
    "Limit.Hp", "Limit.Str", "Limit.Magic", "Limit.Tech", "Limit.Quick",
    "Limit.Luck", "Limit.Def", "Limit.Mdef", "Limit.Phys", "Limit.Sight", "Limit.Move"
]
MISC_KEYS = [
    "MoveType", "StepFrame",
    "WeaponNone", "WeaponSword", "WeaponLance", "WeaponAxe", "WeaponBow",
    "WeaponDagger", "WeaponMagic", "WeaponRod", "WeaponFist", "WeaponSpecial", "WeaponTool",
    "MaxWeaponLevelNone", "MaxWeaponLevelSword", "MaxWeaponLevelLance", "MaxWeaponLevelAxe", "MaxWeaponLevelBow",
    "MaxWeaponLevelDagger", "MaxWeaponLevelMagic", "MaxWeaponLevelRod", "MaxWeaponLevelFist", "MaxWeaponLevelSpecial"
]
ALL_KEYS = GROWTH_KEYS + BASE_KEYS + LIMIT_KEYS + MISC_KEYS

CLASS_NAME_MAP = {
    "MJID_Unknown": "Unknown_不明",
    "MJID_DragonLord": "Dragon Child_神竜ノ子",
    "MJID_DragonKing": "Divine Dragon_神竜ノ王",
    "MJID_ShadowLord": "Fell Child_邪竜ノ子",
    "MJID_ShadowPrincess": "Fell Child_邪竜ノ娘_敵",
    "MJID_ShadowKing": "Fell Monarch (NPC)_邪竜ノ王",
    "MJID_ShadowDragon": "ShadowDragon_邪竜",
    "MJID_AvenirLC": "Avenir_アヴニール下級",
    "MJID_Avenir": "Avenir_アヴニール",
    "MJID_FleurageLC": "Vidame_フロラージュ下級",
    "MJID_Fleurage": "Vidame_フロラージュ",
    "MJID_SuccesseurLC": "Successeur_スュクセサール下級",
    "MJID_Successeur": "Successeur_スュクセサール",
    "MJID_TirailleurLC": "Tireur d'elite_ティラユール下級",
    "MJID_Tirailleur": "Tireur d'elite_ティラユール",
    "MJID_LindwurmLC": "Lindwurm_リンドブルム下級",
    "MJID_Lindwurm": "Lindwurm_リンドブルム",
    "MJID_SleipnirLC": "Sleipnir Rider_スレイプニル下級",
    "MJID_Sleipnir": "Sleipnir Rider_スレイプニル",
    "MJID_PitchforkLC": "Picket_ピッチフォーク下級",
    "MJID_Pitchfork": "Picket_ピッチフォーク",
    "MJID_CupidoLC": "Cupido_クピードー下級",
    "MJID_Cupido": "Cupido_クピードー",
    "MJID_Melusine": "Melusine_メリュジーヌ_味方",
    "MJID_SwordFighter": "Sword Fighter_ソードファイター",
    "MJID_SwordMaster": "Swordmaster_ソードマスター",
    "MJID_BraveHero": "Hero_ブレイブヒーロー",
    "MJID_LanceFighter": "Lance Fighter_ランスファイター",
    "MJID_Halberdier": "Halberdier_ハルバーディア",
    "MJID_RoyalKnight": "Royal Knight_ロイヤルナイト",
    "MJID_AxFighter": "Axe Fighter_アクスファイター",
    "MJID_Berserker": "Berserker_ベルセルク",
    "MJID_Warrior": "Warrior_ウォーリアー",
    "MJID_Archer": "Archer_アーチャー",
    "MJID_Sniper": "Sniper_スナイパー",
    "MJID_BowKnight": "Bow Knight_ボウナイト",
    "MJID_SwordArmor": "Sword Armor_ソードアーマー",
    "MJID_LanceArmor": "Lance Armor_ランスアーマー",
    "MJID_AxArmor": "Axe Armor_アクスアーマー",
    "MJID_General": "General_ジェネラル",
    "MJID_GreatKnight": "Great Knight_グレートナイト",
    "MJID_SwordKnight": "Sword Knight_ソードナイト",
    "MJID_LanceKnight": "Lance Knight_ランスナイト",
    "MJID_AxKnight": "Axe Knight_アクスナイト",
    "MJID_Paladin": "Paladin_パラディン",
    "MJID_WolfKnight": "Wolf Knight_ウルフナイト",
    "MJID_Mage": "Mage_マージ",
    "MJID_Sage": "Sage_セイジ",
    "MJID_MageKnight": "Mage Knight_マージナイト",
    "MJID_Monk": "Martial Monk_モンク",
    "MJID_MasterMonk": "Martial Master_マスターモンク",
    "MJID_HighPriest": "High Priest_ハイプリースト",
    "MJID_SwordPegasus": "Sword Flier_ソードペガサス",
    "MJID_LancePegasus": "Lance Flier_ランスペガサス",
    "MJID_AxPegasus": "Axe Flier_アクスペガサス",
    "MJID_GriffonKnight": "Griffon Rider_グリフォンナイト",
    "MJID_DragonKnight": "Wyvern Knight_ドラゴンナイト",
    "MJID_Thief": "Thief_シーフ",
    "MJID_Dancer": "Dancer_ダンサー",
    "MJID_Barbarian": "Barbarian (NPC)_蛮族",
    "MJID_MorphDragon": "MorphDragon_異形竜",
    "MJID_PhantomDragon": "PhatomDragon_幻影竜",
    "MJID_Villager": "Villager (NPC)_村人",
    "MJID_Emblem": "Emblem_紋章士_ヘクトル_召喚",
    "MJID_ShadowPrincessR": "Fell Child_裏邪竜ノ娘",
    "MJID_ShadowLordR": "Fell Child_裏邪竜ノ子_E5",
    "MJID_ShadowDragonR": "ShadowDragon_E006ラスボス",
    "MJID_Enchant": "Enchanter_エンチャント",
    "MJID_MageCannon": "Mage Cannoneer_マージカノン",
    "MJID_MorphWolf": "MorphWolf_異形狼",
    "MJID_PhantomWolf": "PhantomWolf_幻影狼",
    "MJID_MorphFlyingDragon": "MorphFlyingDragon_異形飛竜",
    "MJID_PhantomFlyingDragon": "PhantomFlyingDragon_幻影飛竜",
    "MJID_AvenirR": "Avenir_アヴニール_E",
    "MJID_FleurageR": "Vidame_フロラージュ_E",
    "MJID_SuccesseurR": "Successeur_スュクセサール_E",
    "MJID_TirailleurR": "Tireur d'elite_ティラユール_E",
    "MJID_LindwurmR": "Lindwurm_リンドブルム_E",
    "MJID_SleipnirR": "Sleipnir Rider_スレイプニル_E",
    "MJID_PitchforkR": "Picket_ピッチフォーク_E",
    "MJID_CupidoR": "Cupido_クピードー_E",
}




display_names = {
    "Quick": "Speed", "Tech": "Dexterity", "Mdef": "Resistance", "Phys": "Build",
    "Sight": "Vision", "Move": "Movement",
    "WeaponSword": "Weapon: Sword",
    "WeaponLance": "Weapon: Lance",
    "WeaponAxe": "Weapon: Axe",
    "WeaponBow": "Weapon: Bow",
    "WeaponDagger": "Weapon: Dagger",
    "WeaponMagic": "Weapon: Magic",
    "WeaponRod": "Weapon: Staff",
    "WeaponFist": "Weapon: Arts",
    "WeaponSpecial": "Weapon: Special",
    "WeaponTool": "Weapon: Tool"
}

def label_name(key):
    parts = key.split(".")
    if len(parts) == 2:
        category, stat = parts
        return f"{category} {display_names.get(stat, stat)}"
    return display_names.get(key, key)

class JobClassEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Fire Emblem Engage Class Editor")
        self.root.geometry("900x880")
        self.data = []
        self.text = ""
        self.current_index = 0
        self.entries = {}
        self.show_all = True
        self.name_map = {}  # Maps display name -> actual Name ID
        self.build_ui()
        self.modified = False


    def build_ui(self):
        tk.Button(self.root, text="Open .txt File", command=self.load_file, font=("Segoe UI", 10)).pack(pady=5)

        

        self.class_selector = ttk.Combobox(self.root, state="readonly", width=80, font=("Segoe UI", 10))
        self.class_selector.bind("<<ComboboxSelected>>", self.on_class_selected)
        self.class_selector.pack(pady=5)

        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, fill='both', expand=True)

        self.tabs = {}
        for category, keys in {
            "Growths": [],
            "Base Stats": BASE_KEYS,
            "Limits": LIMIT_KEYS,
            "Misc": MISC_KEYS
        }.items():
            container = tk.Frame(notebook)
            canvas = tk.Canvas(container, bg="#2e2e2e", highlightthickness=0)
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#2e2e2e")

            scrollable_frame.bind(
                "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            container.pack(fill="both", expand=True)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            frame = scrollable_frame
            notebook.add(container, text=category)
            self.tabs[category] = frame

            if category == "Growths":
                headers = ["Stat", "Enemy Growth", "Player Growth", "Enemy: Normal", "Enemy: Hard", "Enemy: Lunatic"]
                header_row = tk.Frame(frame, bg="#2e2e2e")
                header_row.pack(fill="x", pady=2)
                column_widths = [15, 15, 15, 15, 15, 15]
                for i, header in enumerate(headers):
                    width = column_widths[i] if i < len(column_widths) else 18
                    anchor = "w"
                    tk.Label(header_row, text=header, width=width, anchor=anchor, bg="#2e2e2e", fg="white", font=("Segoe UI", 10)).pack(side="left", padx=1)

                stats = ["Hp", "Str", "Magic", "Tech", "Quick", "Luck", "Def", "Mdef", "Phys", "Sight", "Move"]
                for stat in stats:
                    row = tk.Frame(frame, bg="#2e2e2e")
                    row.pack(fill="x", pady=1)
                    tk.Label(row, text=display_names.get(stat, stat), width=15, anchor="w", bg="#2e2e2e", fg="white").pack(side="left")
                    for prefix in ["BaseGrow", "DiffGrow", "DiffGrowNormal", "DiffGrowHard", "DiffGrowLunatic"]:
                        key = f"{prefix}.{stat}"
                        entry = tk.Entry(row, bg="#3a3a3a", fg="white", insertbackground="white", highlightbackground="#555", highlightcolor="#777", font=("Segoe UI", 10), width=15)
                        entry.bind("<KeyRelease>", lambda e, k=key: self.on_field_change(k))
                        entry.pack(side="left", padx=1)
                        self.entries[key] = entry
            else:
                for key in keys:
                    row = tk.Frame(frame, bg="#2e2e2e")
                    row.pack(fill="x", pady=2)
                    tk.Label(row, text=label_name(key), width=25, anchor="w", bg="#2e2e2e", fg="white", font=("Segoe UI", 10)).pack(side="left")

                    if key.startswith("Weapon"):
                        var = tk.IntVar()
                        checkbox = tk.Checkbutton(row, variable=var, anchor="w", bg="#2e2e2e", fg="white", selectcolor="#2e2e2e", font=("Segoe UI", 10))
                        checkbox.pack(side="left")
                        self.entries[key] = var
                    elif key.startswith("MaxWeaponLevel"):
                        entry = tk.Entry(row, bg="#3a3a3a", fg="white", insertbackground="white", highlightbackground="#555", highlightcolor="#777", font=("Segoe UI", 10), width=10)
                        entry.pack(side="right", expand=True, fill="x")
                        self.entries[key] = entry
                    elif key == "MoveType":
                        options = [
                            ("1", "Infantry"),
                            ("2", "Cavalry"),
                            ("3", "Flying"),
                            ("4", "Dragon")
                        ]
                        move_vals = [v[1] for v in options]
                        move_map = {v[1]: v[0] for v in options}
                        combo = ttk.Combobox(row, values=move_vals, state="readonly", width=12)
                        combo.pack(side="left")
                        self.entries[key] = (combo, move_map)
                    else:
                        entry = tk.Entry(row, bg="#3a3a3a", fg="white", insertbackground="white", highlightbackground="#555", highlightcolor="#777", font=("Segoe UI", 10), width=10)
                        entry.bind("<KeyRelease>", lambda e, k=key: self.on_field_change(k))
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
            if "Jid=" not in block:
                continue
            attrs = dict(re.findall(r'(\w+(?:\.\w+)*|\w+)="([^"]*)"', block))
            name = attrs.get("Name", "")
            if not name:
                continue
            attrs["__original"] = block
            attrs["__span"] = match.span()
            self.data.append(attrs)
        self.refresh_dropdown()

    def refresh_dropdown(self):
        if not self.data:
            return
        enemy_only_prefixes = [
            "MJID_Morph", "MJID_Phantom", "MJID_Shadow", "MJID_DragonKing", "MJID_DragonLord", "MJID_Emblem", "MJID_FellDragon", "MJID_Rescue"
        ]
        self.filtered_data = self.data
        display_list = []
        self.name_map = {}
        for i, entry in enumerate(self.filtered_data):
            internal_name = entry.get("Name", f"Class {i}")
            true_display_name = CLASS_NAME_MAP.get(internal_name, internal_name)
            true_display_name = CLASS_NAME_MAP.get(internal_name, internal_name)
            if re.search(r"(LC|_LC|R|_R|Enemy|_Enemy)$", internal_name):
                if not true_display_name.endswith("(NPC)"):
                    true_display_name += " (NPC)"
            display_name = true_display_name
            self.name_map[display_name] = internal_name
            display_list.append(display_name)

            # Sort list alphabetically
            display_list.sort(key=lambda x: x.lower())

            # Pin "Unknown" class to the top (but don't auto-select it)
            unknown_display = None
            for name, internal in self.name_map.items():
                if internal == "MJID_Unknown":
                    unknown_display = name
                    break

            if unknown_display and unknown_display in display_list:
                display_list.remove(unknown_display)
                display_list.insert(0, unknown_display)

            self.class_selector["values"] = display_list

            # Don't auto-select anything
            self.class_selector.set("")



        if display_list:
            self.class_selector.current(0)
            self.show_class(0)
        else:
            self.class_selector.set("")

    def on_class_selected(self, event):
        selected_display = self.class_selector.get()

        if self.modified:
            if not messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Are you sure you want to switch classes without saving?"):
                # Cancel switch: revert combobox to previous selection
                prev_display_name = None
                for name, internal in self.name_map.items():
                    if self.filtered_data[self.current_index].get("Name") == internal:
                        prev_display_name = name
                        break
                if prev_display_name:
                    self.class_selector.set(prev_display_name)
                return

        # Proceed with selection
        internal_name = self.name_map.get(selected_display, selected_display)
        for i, entry in enumerate(self.filtered_data):
            if internal_name == entry.get("Name") or entry.get("Name") in selected_display:
                self.show_class(i)
                break


    def show_class(self, index):
        self.current_index = index
        job = self.filtered_data[index]
        self.original_values = job.copy()
        for key in ALL_KEYS:
            widget = self.entries.get(key)
            if widget is None:
                continue
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, job.get(key, ""))
            elif isinstance(widget, tk.IntVar):
                widget.set(1 if job.get(key, "0") == "1" else 0)
            elif isinstance(widget, tuple) and isinstance(widget[0], ttk.Combobox):
                combo, move_map = widget
                val = job.get(key)
                if val is None:
                    continue
                label = next((label for label, value in move_map.items() if value == val), val)
                combo.set(label)
            elif isinstance(widget, ttk.Combobox):
                val = job.get(key)
                if val is not None:
                    widget.set(val)
                # Reset color coding on load
        self.original_values = job.copy()
        for key in ALL_KEYS:
            widget = self.entries.get(key)
            if isinstance(widget, tk.Entry):
                try:
                    new_val = int(job.get(key, "0"))
                    orig_val = int(self.original_values.get(key, "0"))
                except ValueError:
                    widget.config(bg="#3a3a3a")
                    continue

                if new_val > orig_val:
                    widget.config(bg="#2e4e2e")
                elif new_val < orig_val:
                    widget.config(bg="#4e2e2e")
                else:
                    widget.config(bg="#3a3a3a")
        self.modified = False


    def save_changes(self):
        job = self.filtered_data[self.current_index]
        for key in ALL_KEYS:
            val = self.entries[key]
            if isinstance(val, tk.Entry):
                job[key] = val.get()
            elif isinstance(val, tk.IntVar):
                job[key] = str(val.get())
            elif isinstance(val, ttk.Combobox):
                if isinstance(self.entries[key], tuple):
                    combo, move_map = self.entries[key]
                    job[key] = move_map.get(combo.get(), "0")
                else:
                    job[key] = val.get()
        parts = []
        for k, v in job.items():
            if not k.startswith("__"):
                safe_v = html.escape(v, quote=True)  # escape &, <, >, and "
                parts.append(f'{k}="{safe_v}"')
        new_block = "    <Param " + " ".join(parts) + " />"
        start, end = job["__span"]
        self.text = self.text[:start] + new_block + self.text[end:]
        job["__original"] = new_block
        job["__span"] = (start, start + len(new_block))
        self.modified = False


    def write_to_file(self):
        if not self.file_path:
            return

        updated_text = self.text

        for entry in self.data:
            original_text = entry["__original"]
            start, end = entry["__span"]

            modified_parts = []
            for k in entry:
                if not k.startswith("__"):
                    safe_v = html.escape(entry[k], quote=True)
                    modified_parts.append(f'{k}="{safe_v}"')

            new_text = "    <Param " + " ".join(modified_parts) + " />"

            if new_text != original_text:
                # Refresh the span in updated_text to avoid offset issues
                original_span_text = updated_text[start:end]
                if original_span_text != original_text:
                    # Search for actual block again in case span is outdated
                    search_pattern = re.escape(original_text)
                    found_match = re.search(search_pattern, updated_text)
                    if found_match:
                        start, end = found_match.span()
                    else:
                        continue  # skip broken entry

                updated_text = updated_text[:start] + new_text + updated_text[end:]
                entry["__original"] = new_text
                entry["__span"] = (start, start + len(new_text))

        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(updated_text)

        self.text = updated_text

    def on_field_change(self, key):
        widget = self.entries.get(key)
        if not isinstance(widget, tk.Entry):
            return

        original = self.original_values.get(key, "")
        try:
            new_val = int(widget.get())
            original_val = int(original) if original != "" else 0
        except ValueError:
            widget.config(bg="#3a3a3a")  # reset for non-numeric
            return

        if new_val > original_val:
            widget.config(bg="#2e4e2e")  # green-ish
        elif new_val < original_val:
            widget.config(bg="#4e2e2e")  # red-ish
        else:
            widget.config(bg="#3a3a3a")  # unchanged

        self.modified = True



if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#2e2e2e")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#2e2e2e")
    style.configure("TLabel", background="#2e2e2e", foreground="white")
    style.configure("TCheckbutton", background="#2e2e2e", foreground="white")
    style.configure("TButton", background="#444", foreground="white")
    style.configure("TNotebook", background="#2e2e2e")
    style.configure("TNotebook.Tab", background="#444", foreground="white")
    style.map("TNotebook.Tab", background=[("selected", "#666")])
    app = JobClassEditor(root)
    def on_close():
        if app.modified:
            if not messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Exit anyway?"):
                return
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()
