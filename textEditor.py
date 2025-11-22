import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, simpledialog, font
import re
from os.path import exists as path_exists
from os import remove as remove_path

from pyasn1_modules.rfc3280 import poste_restante_address


class TextEditor:
    def __init__(self, root, parent, settings,  file):
        self.root = root
        self.parent = parent

        self.file = file
        self.settings = settings

        self.base_font = font.Font(family="Consolas", size=self.settings["textSize"])

        #rodzic wszystkiego
        self.wysrodkowywacz = tk.Frame(self.parent, width=525, bg=root["bg"], bd=1, relief="groove")
        self.wysrodkowywacz.place(rely=0.5, relx=0.5, relheight=0.95, relwidth=0.8, anchor="center")

        #guziczki :)
        self.toolbar = tk.Frame(self.wysrodkowywacz, bg="grey10", height=30, bd=1, relief="groove")
        self.toolbar.pack(side="top", fill="x")
        self.toolbar.pack_propagate(False)

        self.czcionka = "Consolas"
        self.boldButton = tk.Button(self.toolbar, text="B", font=("Consolas", 14, "bold"), width=3, bd=0, command=self.make_bold, activebackground="grey50", cursor="hand2")
        self.boldButton.pack(side="left", padx=2, pady=2, fill="y")
        self.italicButton = tk.Button(self.toolbar, text="I", font=("Consolas", 14, "italic bold"), width=3, bd=0, command=self.make_italic, activebackground="grey50", cursor="hand2")
        self.italicButton.pack(side="left", padx=2, pady=2, fill="y")
        self.underlineButton = tk.Button(self.toolbar, text="U", font=("Consolas", 14, "underline bold"), width=3, bd=0, command=self.make_underline, activebackground="grey50", cursor="hand2")
        self.underlineButton.pack(side="left", padx=2, pady=2, fill="y")
        self.strikeButton = tk.Button(self.toolbar, text="S", font=("Consolas", 14, "overstrike bold"), width=3, bd=0, command=self.make_strike, activebackground="grey50", cursor="hand2")
        self.strikeButton.pack(side="left", padx=2, pady=2, fill="y")
        tk.Button(self.toolbar, text="Color", font=("Consolas", 14, "bold"), bd=0, command=self.change_color, activebackground="grey50", cursor="hand2").pack(side="right", padx=2, pady=2, fill="y")
        self.sizeButton = tk.Menubutton(self.toolbar, text="Size", font=("Consolas", 14, "bold"), bd=0, activebackground="grey50", cursor="hand2")
        self.sizeButton.pack(side="right", padx=2, pady=2, fill="y")
        self.size_menu = tk.Menu(self.sizeButton, tearoff=0)
        self.sizeButton.config(menu=self.size_menu)
        sizes = [8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]
        for size in sizes:
            if size == self.settings["textSize"]:
                self.size_menu.add_command(label=str(size), font=("Consolas", 10, "bold"), command=lambda s=size: self.change_size(s))
            else:
                self.size_menu.add_command(label=str(size), font=("Consolas", 10), command=lambda s=size: self.change_size(s))
        self.titleEntry = tk.Entry(self.toolbar, font=("Calibri", 14, "bold"), bd=0, justify="center", width=50)
        self.titleEntry.pack(side="right", padx=2, pady=2, fill="both")

        self.titleEntry.bind("<FocusIn>", self.remove_placeholder)
        self.titleEntry.bind("<FocusOut>", self.add_placeholder)

        self.save_button_color = "green3"
        self.saveButton = tk.Button(self.toolbar, text="Save", font=("Consolas", 14, "bold"), width=5, bd=0, command=self.save_file, cursor="hand2", bg=self.save_button_color, activebackground="green2")
        self.saveButton.pack(anchor="center")

        self.root.bind("<Control-b>", lambda e: self.make_bold())
        self.root.bind("<Control-B>", lambda e: self.make_bold())
        self.root.bind("<Control-u>", lambda e: self.make_underline())
        self.root.bind("<Control-U>", lambda e: self.make_underline())

        self.root.bind("<Control-s>", lambda e: self.save_file(True))
        self.root.bind("<Control-S>", lambda e: self.save_file(True))

        self.text = tk.Text(self.wysrodkowywacz, wrap="word", font=self.base_font, bg="grey15", fg="white", insertbackground="white", bd=0)
        self.text.pack(side="left", fill="both", expand=True)

        self.scroll = None
        self.create_scroll()

        self.configure_tags()

        self.open_file()
        self.add_placeholder()

    def add_placeholder(self, event=None):
        if self.titleEntry.get() == "":
            self.titleEntry.insert(0, "Title")
            self.titleEntry.config(fg="grey")

    # Funkcja do usunięcia placeholdera po kliknięciu
    def remove_placeholder(self, event):
        if self.titleEntry.get() == "Title" and self.titleEntry["fg"] == "grey":
            self.titleEntry.delete(0, "end")
            self.titleEntry.config(fg="black")

    def create_scroll(self):
        if self.scroll:
            self.scroll.destroy()
        self.scroll = tk.Scrollbar(self.wysrodkowywacz)
        self.scroll.pack(side="right", fill="y")
        self.text.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.text.yview)
        self.text.bind("<KeyRelease>", lambda e: self.text.see("insert"))

    def configure_tags(self):
        self.text.tag_configure("bold", font=(self.czcionka, self.settings["textSize"], "bold"))
        self.text.tag_configure("italic", font=(self.czcionka, self.settings["textSize"], "italic"))
        self.text.tag_configure("underline", font=(self.czcionka, self.settings["textSize"], "underline"))
        self.text.tag_configure("strike", font=(self.czcionka, self.settings["textSize"], "overstrike"))

    def fix_the_size_menu(self):
        for i in range(self.size_menu.index("end") + 1):
            tekst = self.size_menu.entrycget(i, "label")
            if int(tekst) == self.settings["textSize"]:
                self.size_menu.entryconfig(i, font=("Consolas", 10, "bold"))
            else:
                self.size_menu.entryconfig(i, font=("Consolas", 10))

    #formatowanie
    def apply_tag(self, tag):
        try:
            if not self.check_tag(tag):
                self.text.tag_remove("bold", "sel.first", "sel.last")
                self.text.tag_remove("italic", "sel.first", "sel.last")
                self.text.tag_remove("underline", "sel.first", "sel.last")
                self.text.tag_remove("strike", "sel.first", "sel.last")
                self.text.tag_add(tag, "sel.first", "sel.last")
            else:
                self.text.tag_remove(tag, "sel.first", "sel.last")
        except tk.TclError:
            pass

    def make_bold(self):
        self.apply_tag("bold")

    def make_italic(self):
        self.apply_tag("italic")

    def make_underline(self):
        self.apply_tag("underline")

    def make_strike(self):
        self.apply_tag("strike")

    def change_color(self, entireFile=False, color=None):
        if not color:
            color = colorchooser.askcolor()[1]
        if color:
            try:
                if bool(self.text.tag_ranges("sel")) and not entireFile:
                    for tag in self.text.tag_names():
                        if tag.startswith("color_"):
                            self.text.tag_remove(tag, "sel.first", "sel.last")
                    self.text.tag_configure("color_" + color, foreground=color)
                    self.text.tag_add("color_" + color, "sel.first", "sel.last")
                else:
                    self.text.config(fg=color)
            except tk.TclError:
                pass

    def change_size(self, size):
        self.text.config(font=(self.czcionka, size))
        self.settings["textSize"] = size
        self.configure_tags()
        self.create_scroll()
        self.fix_the_size_menu()

    # --- FUNKCJE PLIKU ---
    def new_file(self):
        self.text.delete(1.0, "end")
        self.file_path = None
        self.root.title("Edytor tekstu PRO")

    def open_file(self):
        if path_exists(self.file):
            with open(self.file, "r", encoding="utf-8") as f:
                content = f.read()

                if content:
                    title = content[:content.find("'")]
                    self.titleEntry.insert(0, title)
                    content = content[len(title)+1:]
                    fgColor = content[:content.find("~")]
                    self.change_color(entireFile=True, color=fgColor)
                    #nie trzeba usuwać koloru, ponieważ program i tak go nie wykryje

                    matches = re.findall(r"<([a-zA-Z][^>]*)>(.*?)</\1", content, flags=re.DOTALL)
                    for tags, txt in matches:
                        start_index = self.text.index("end-1c")
                        end_index = None
                        addColor = False
                        isThereAnyOtherTag = False  #we use it with color
                        for tag in tags.split("|"):
                            if tag == "n":
                                self.text.insert("end", txt)
                                isThereAnyOtherTag = True
                            elif tag.startswith("color_"):
                                color = tag[len("color_"):]
                                self.text.tag_configure("color_" + color, foreground=color)
                                addColor = True
                            else:
                                self.text.insert("end", txt)
                                end_index = self.text.index("end-1c")
                                self.text.tag_add(tag, start_index, end_index)
                                isThereAnyOtherTag = True
                        if addColor:
                            if not isThereAnyOtherTag:
                                self.text.insert("end", txt)
                            if not end_index:
                                end_index = self.text.index("end-1c")
                            self.text.tag_add("color_" + color, start_index, end_index)

    def save_file(self, wasTriggeredByAShortCut=False):
        if wasTriggeredByAShortCut:
            self.saveButton.config(bg="green4")
            self.root.after(250, lambda: self.saveButton.config(bg=self.save_button_color))

        if (self.titleEntry["fg"] != "grey" and self.titleEntry.index("end") != 0) or self.text.index("end-1c") != "1.0":
            with open(self.file, "w", encoding="utf-8") as f:
                if self.titleEntry["fg"] != "grey":
                    f.write(self.titleEntry.get() + "'")
                else:
                    f.write("'")
                f.write(self.text["fg"] + "~")

                start = "1.0"
                end = self.text.index("end-1c")

                while self.text.compare(start, "<", end):
                    current_tags = [x for x in self.text.tag_names(start) if x != "sel"]
                    next_index = self.text.index(f"{start} +1c")

                    while next_index != end and set([x for x in self.text.tag_names(next_index) if x != "sel"]) == set(current_tags):
                        next_index = self.text.index(f"{next_index} +1c")

                    segment_text = self.text.get(start, next_index)

                    if len(current_tags) > 0:
                        sequence = "|".join(current_tags)
                        f.write("<" + sequence + ">" + segment_text + "</" + sequence + ">")
                    else:
                        f.write(f"<n>{segment_text}</n>")

                    start = next_index
        elif path_exists(self.file):
            remove_path(self.file)

    def check_tag(self, tag_name):
        try:
            start = self.text.index("sel.first")
            end = self.text.index("sel.last")
        except tk.TclError:
            return "no_selection"

        current = start
        all_have = True
        while self.text.compare(current, "<", end):
            tags = self.text.tag_names(current)
            if not tag_name in tags:
                all_have = False
                break
            current = self.text.index(f"{current}+1c")  # przejdź do następnego znaku

        return all_have

    def destroy(self):
        self.wysrodkowywacz.destroy()