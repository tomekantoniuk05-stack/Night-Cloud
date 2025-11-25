import tkinter as tk
from tkinter import font
from random import randint
from datetime import datetime, date
import calendar
from PIL import ImageTk, Image
import getFiles
from getFiles import *
import animations as anim
from configs import *
from textEditor import TextEditor
from webbrowser import open as openWeb


loadingRoot = tk.Tk()
loadingRoot.withdraw()
loadingRoot.geometry("500x500")
loadingRoot.minsize(500, 500)
loadingRoot.configure(background="grey10")
loadingRoot.iconphoto(False, tk.PhotoImage(file=get_asset("moon.png")))
loadingRoot.title("Night Cloud - Loading")
loadingRoot.resizable(False, False)

logo = Image.open(get_asset("logo.png")).convert("RGBA")
logoWidth, logoHeight = logo.size #for later
logo = logo.resize((500, 284), Image.Resampling.LANCZOS)
tk_logo = ImageTk.PhotoImage(logo)
logoLabel = tk.Label(loadingRoot, image=tk_logo, bg=loadingRoot["bg"])
logoLabel.image = tk_logo
logoLabel.place(relx=0.5, rely=0.5, anchor="center")

loadingLabel = tk.Label(loadingRoot, font=("Arial", 16, "bold"), fg="white", bg=loadingRoot["bg"])
loadingLabel.pack(side="bottom", fill="x", pady=5)
anim.loadingAnimation(loadingRoot, loadingLabel)

loadingRoot.deiconify()
loadingRoot.update()

dreamJournalFolderPath, settings = load_files()
HELP_FILE_PATH = get_asset("Help Support.pdf")

stop = False
def onClose():
    global stop
    stop = True
    loadingRoot.destroy()
loadingRoot.protocol("WM_DELETE_WINDOW", onClose)
loadingRoot.after(randint(20, 35) * 100, lambda: loadingRoot.destroy())
loadingRoot.mainloop()
if stop:
    sys.exit(0)

############################################################################################################### main app

#the actual app
root = tk.Tk()
root.withdraw()
root.geometry("1500x843")
root.configure(background="grey10")
root.iconphoto(False, tk.PhotoImage(file=get_asset("moon.png")))
root.title("Night Cloud")

try:
    root.wm_attributes("-zoomed", True)
except tk.TclError:
    root.state('zoomed')

root.attributes("-fullscreen", True)

#dodawane paska zakładek
tab_bar = tk.Frame(root, bg="grey5", height=125)
tab_bar.pack(side="top", fill="x")
tab_bar.pack_propagate(False)

content_frame = tk.Frame(root, bg=root["bg"])
content_frame.pack(fill="both", expand=True)

root.update()

#adding logo
stosunekLogo = logoHeight / logoWidth
rozmiar_tab_bar = tab_bar.winfo_height() - 20
logo = logo.resize((round(rozmiar_tab_bar / stosunekLogo), rozmiar_tab_bar), Image.Resampling.LANCZOS)
rozmiar_tab_bar += 20
tk_logo = ImageTk.PhotoImage(logo)
logoLabel = tk.Label(tab_bar, image=tk_logo, bg=tab_bar["bg"])
logoLabel.pack(side="left", padx=10)
logoLabel.image = tk_logo

#dodawanie guziczków :)
nazwyZakladek = ["Sleep Journal", "Comunity Posts", "Exit", "Help", "Credits"] #3 ostatnie będą w odwrotnej kolejności
guziczkiZakladek = {}
kontentZakladek = {}
for nazwa in nazwyZakladek:
    btn = tk.Button(tab_bar, text=nazwa, bg=root["bg"], fg="white", font=("Arial", 16), activebackground="violet red", bd=0, cursor="hand2")
    if nazwa != "Help" and nazwa != "Credits" and nazwa != "Exit":
        btn.pack(side="left", padx=10, pady=10)
    else:
        if nazwa == "Exit":
            btn.config(bg="red3", activebackground="red")
            offsetFrame = tk.Frame(tab_bar, bg=root["bg"])
            offsetFrame.pack(side="right", padx=5, pady=5)
        btn.pack(side="right", padx=10, pady=10)
    guziczkiZakladek[nazwa] = btn

for name in nazwyZakladek:
    if name == "Sleep Journal" or name == "Exit" or name == "Help":
        continue
    text = "Coming Soon!"
    frame = tk.Frame(content_frame, bg=root["bg"])
    if name != "Credits":
        label = tk.Label(frame, text=text, fg="white", bg=root["bg"], font=("Arial", 20))
        label.place(anchor="center", relx=0.5, rely=0.5)
    kontentZakladek[name] = frame

#credits
createdLabel = tk.Label(kontentZakladek["Credits"], text="Created by:", fg="white", bg=kontentZakladek["Credits"]["bg"], font=("Arial", 36, "bold"))
createdLabel.pack(side="top", pady=5, fill="x")
teamLogo = Image.open(get_asset("Sleepy Triangle.png")).convert("RGBA")
teamLogo = teamLogo.resize((544, 600), Image.Resampling.LANCZOS)
tk_teamLogo = ImageTk.PhotoImage(teamLogo)
teamLogoLabel = tk.Label(kontentZakladek["Credits"], image=tk_teamLogo, bg=kontentZakladek["Credits"]["bg"])
teamLogoLabel.place(relx=0.5, rely=0.5, anchor="center")

#used for later
kontentSnu = tk.Frame(content_frame, bg=root["bg"])
kontentSnu.pack(fill="both", anchor="center")
kontentZakladek["Dream"] = kontentSnu

#sleep journal
framesOfTheWeeks = []
framesOfDaysStrokes = []
framesOfDays = []
numberOfDayLabel = []
buttonsOfDreams = []
dreamTitles = []
kontentSleepJournal = None
lucidEntry = None
dataTeraz = None
dreamTitleFont = font.Font(family="Arial", size=15, weight="bold")
def create_sleep_journal_tab():
    global kontentSleepJournal
    global framesOfTheWeeks
    global framesOfDaysStrokes
    global framesOfDays
    global numberOfDayLabel
    global buttonsOfDreams
    global dreamTitles
    global dataTeraz
    global lucidEntry
    global dreamTitleFont

    if kontentSleepJournal:
        settings["lucidPoints"] = lucidEntry.get()
        kontentSleepJournal.destroy()
        root.update_idletasks()
        framesOfTheWeeks = []
        framesOfDaysStrokes = []
        framesOfDays = []
        numberOfDayLabel = []
        buttonsOfDreams = []
        dreamTitles = []

    kontentSleepJournal = tk.Frame(content_frame, bg=root["bg"])
    kontentZakladek["Sleep Journal"] = kontentSleepJournal

    dataTeraz = datetime.now()
    if settings["year"] != 0:
        dataTeraz = dataTeraz.replace(year=settings["year"])
    if settings["month"] != 0:
        dataTeraz = dataTeraz.replace(month=settings["month"])
    pierwszyDzienMiesiaca, liczbaDniWMiesiecu = calendar.monthrange(dataTeraz.year, dataTeraz.month)

    calendarFrame = tk.Frame(kontentSleepJournal, bg=root["bg"])

    # creating day name display
    dniTygodniaFrame = tk.Frame(calendarFrame, bg="firebrick3", height=75)
    dniTygodniaFrame.pack(fill="both", side="top")
    for dzien in range(0, 7):
        frameStroke = tk.Frame(dniTygodniaFrame, bg="white", height=75)
        frameStroke.pack(expand=True, fill="both", side="left")
        frame = tk.Frame(frameStroke, bg="white")
        frame.place(rely=0.5, relx=0.5, relheight=0.9, relwidth=0.9, anchor="center")
        textLabel = tk.Label(frame, text=DNI_TYGODNIA[dzien], fg="white", bg="purple2", font=("Arial", 15, "bold"))
        textLabel.pack(fill="both", expand=True, anchor="center")

    for week in range(1, 7):
        frameTygodnia = tk.Frame(calendarFrame, bg=root["bg"], height=150)
        frameTygodnia.pack(fill="both", side="top", expand=True)
        framesOfTheWeeks.append(frameTygodnia)
        for day in range(1, 8):
            dayFrameStroke = tk.Frame(frameTygodnia, bg="white", height=100)
            dayFrameStroke.pack(expand=True, fill="both", side="left")
            framesOfDaysStrokes.append(dayFrameStroke)
            # to była ramka, teraz pora na zawartość
            dayFrame = tk.Frame(dayFrameStroke, bg=root["bg"])
            dayFrame.place(rely=0.5, relx=0.5, relheight=0.9, relwidth=0.9, anchor="center")
            framesOfDays.append(dayFrame)
            # teraz data
            dayNr = (week - 1) * 7 + day - pierwszyDzienMiesiaca
            dayLabel = tk.Label(dayFrame, text=dayNr, font=("Arial", 16), fg="white", bg=root["bg"])
            dayLabel.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
            numberOfDayLabel.append(dayLabel)
            # teraz guziczki :)
            dreamButton = tk.Button(dayFrame, text="Edit", font=("Arial", 16), fg="white", bg="SlateBlue2",
                                    activebackground="RoyalBlue2", bd=0, cursor="hand2",
                                    command=lambda day=dayNr: show_tab(None, day))
            dayFrame.bind("<Enter>", lambda e, btn=dreamButton: anim.show_button(btn))
            dayFrame.bind("<Leave>", lambda e, btn=dreamButton, frame=dayFrameStroke: anim.hide_button(e, btn, frame))
            buttonsOfDreams.append(dreamButton)
            # teraz tytuł snu
            dreamTitle = tk.Label(dayFrame, font=dreamTitleFont, fg="white", bg=dayFrame["bg"])
            savedFile = get_a_nc_file(dataTeraz.strftime("%m-%Y"), dayNr)
            dreamTitle.place(relx=0.033, rely=0.57, relwidth=0.94, relheight=0.4)

            def change_the_font(defaultTitle, label, customFont=None, italic=False):
                labelWidht = label.winfo_width()
                if labelWidht == 1:
                    root.update()
                    root.after(5, lambda t=defaultTitle, l=label, c=customFont, i=italic: change_the_font(t, label, customFont, i))
                    return
                if not customFont:
                    if italic:
                        customFont = font.Font(family=dreamTitleFont["family"], size=dreamTitleFont["size"] - 2, weight=dreamTitleFont["weight"], slant="italic")
                    else:
                        customFont = font.Font(family=dreamTitleFont["family"], size=dreamTitleFont["size"], weight=dreamTitleFont["weight"])
                if customFont.measure(defaultTitle) > labelWidht:
                    while customFont["size"] > 9:
                        customFont.config(size=customFont["size"]-1)
                        if customFont.measure(defaultTitle) <= labelWidht:
                            label.config(font=customFont, text=defaultTitle)
                            return
                    i = 0
                    title = ""
                    while customFont.measure(title) <= labelWidht:
                        i += 1
                        title = defaultTitle[:i] + "..."
                    defaultTitle = defaultTitle[:i-1] + "..."

                label.config(font=customFont, text=defaultTitle)

            if os.path.exists(savedFile):
                with open(savedFile, "r", encoding="utf-8") as f:
                    title = f.read().split("'")[0]
                if title:
                    root.update()
                    root.after(5, lambda t=title, label=dreamTitle: change_the_font(t, label))
                else:
                    root.update()
                    root.after(5, lambda t=title, label=dreamTitle: change_the_font("no title", label, italic=True))

    kontentSleepJournal.bind("<Enter>", lambda e: anim.show_button())
    dniTygodniaFrame.bind("<Enter>", lambda e: anim.show_button())

    # usuwanie pierwszych dni poprzedniego tygodnia
    dataPoprzedniegoMiesiaca = dataTeraz
    if dataTeraz.month == 1:
        date(dataPoprzedniegoMiesiaca.year - 1, 12, 1)
    else:
        dataPoprzedniegoMiesiaca = date(dataPoprzedniegoMiesiaca.year, dataPoprzedniegoMiesiaca.month - 1, 1)

    dlugoscPoprzedniegoMiesiaca = calendar.monthrange(dataPoprzedniegoMiesiaca.year, dataPoprzedniegoMiesiaca.month)[1]
    for i in range(0, pierwszyDzienMiesiaca):
        frame = framesOfDaysStrokes.pop(0)
        framesOfDays.pop(0)
        frame.config(bg="grey25")
        numberLabel = numberOfDayLabel.pop(0)
        numberLabel.config(text=dlugoscPoprzedniegoMiesiaca - pierwszyDzienMiesiaca + i + 1, fg="grey25")
        buttonsOfDreams.pop(0)
    # teraz usuwanie ostatnich dni
    for i in range(0, len(framesOfDaysStrokes) - liczbaDniWMiesiecu):
        frame = framesOfDaysStrokes.pop(liczbaDniWMiesiecu)
        framesOfDays.pop(liczbaDniWMiesiecu)
        frame.config(bg="grey25")
        numberLabel = numberOfDayLabel.pop(liczbaDniWMiesiecu)
        numberLabel.config(text=i + 1, fg="grey25")
        buttonsOfDreams.pop(liczbaDniWMiesiecu)

    #the current day
    if settings["month"] == 0 and settings["year"] == 0:
        framesOfDays[dataTeraz.day - 1].config(bg="maroon2")
        for kid in framesOfDays[dataTeraz.day - 1].winfo_children():
            if kid["bg"] == root["bg"]:
                kid.config(bg=framesOfDays[dataTeraz.day - 1]["bg"])

    calendarFrame.place(rely=0.5, relx=0.5, relheight=0.95, relwidth=0.8, anchor="center")

    #lucid points
    lucidEntryFrame = tk.Frame(kontentSleepJournal, bg=root["bg"])
    lucidEntryFrame.place(relx=0.905, rely=0.917, relwidth=0.1, relheight=0.0567)

    root.update()
    def create_lucid_points():
        global lucidEntry

        frameHeight = lucidEntryFrame.winfo_height()
        if frameHeight == 1:
            root.update()
            root.after(5, create_lucid_points)
            return
        frameHeight /= 1.2
        frameHeight = round(frameHeight)
        pointsIcon = Image.open(get_asset("lucid points icon.png")).convert("RGBA")
        width, height = pointsIcon.size
        ratio = height / width
        pointsIcon = pointsIcon.resize((round(frameHeight / ratio), frameHeight), Image.Resampling.LANCZOS)
        tk_points = ImageTk.PhotoImage(pointsIcon)
        pointsLabel = tk.Label(lucidEntryFrame, image=tk_points, bg=lucidEntryFrame["bg"], cursor="hand2")
        pointsLabel.image = tk_points
        pointsLabel.pack(side="left", anchor="center")

        lucidEntry = tk.Entry(lucidEntryFrame, font=("Arial", 28, "bold"), fg="white", bg=lucidEntryFrame["bg"], bd=0)
        lucidEntry.insert(0, settings["lucidPoints"])

        root.bind("<Button-1>", lambda e, entry=lucidEntry, root=root: (anim.on_lost_focus(e, entry, root), anim.remember_the_last_pressed(e)))
        root.bind("<ButtonRelease-1>", lambda e, entry=lucidEntry, button=pointsLabel: anim.add_one_ldp(e, lucidEntry, button))
        lucidEntry.bind("<Return>", lambda e, root=root: anim.stop_writing(root))

        lucidEntry.pack(side="left", anchor="center", expand=True, fill="y", padx=2)

    root.after(5, create_lucid_points)

    #creating date Label
    dateLabelHitbox = tk.Label(kontentSleepJournal, bg=root["bg"])
    dateLabelHitbox.place(relx=0.01, rely=0.025, relwidth=0.08, relheight=0.1)

    yearHitbox = tk.Label(dateLabelHitbox, bg="grey15")
    yearHitbox.place(relx=0.5, rely=0.49, relwidth=1, relheight=0.5, anchor="s")

    monthHitbox = tk.Label(dateLabelHitbox, bg="grey15")
    monthHitbox.place(relx=0.5, rely=0.51, relwidth=1, relheight=0.5, anchor="n")

    dateButtonsHitbox = tk.Label(kontentSleepJournal, bg="grey15")
    dateButtonsHitbox.place(relx=0.011, rely=0.13, relwidth=0.078, relheight=0.04)

    root.update()
    yearLabel = None
    monthLabel = None
    def add_content_to_date_label():
        global yearLabel, monthLabel

        frameHeight = yearHitbox.winfo_height()
        if frameHeight == 1:
            root.update()
            root.after(5, add_content_to_date_label)
            return

        arrowImage = Image.open(get_asset("arrow.png")).convert("RGBA")
        arrowWidth, arrowHeight = arrowImage.size
        arrowRatio = arrowHeight / arrowWidth
        arrowImage = arrowImage.resize((round(frameHeight / arrowRatio / 1.1), round(frameHeight / 1.1)), Image.Resampling.LANCZOS)
        forward_arrow = ImageTk.PhotoImage(arrowImage)
        back_arrow = ImageTk.PhotoImage(arrowImage.rotate(180))

        def modifyTheYear(modification):
            yearLabel.config(text=int(yearLabel["text"])+modification) #pls don't push it to its limits :(
            if yearLabel["text"] == "0":
                modifyTheYear(-1)

        def modifyTheMonth(modification):
            txt = str(int(monthLabel["text"])+modification)
            if len(txt) < 2:
                txt = "0" + txt
            monthLabel.config(text=txt)
            if int(monthLabel["text"]) <= 0:
                modifyTheYear(-1)
                modifyTheMonth(12)
            elif int(monthLabel["text"]) > 12:
                modifyTheYear(1)
                modifyTheMonth(-12)

        forwardYearButton = tk.Button(yearHitbox, bg=yearHitbox["bg"], activebackground=yearHitbox["bg"], image=forward_arrow, bd=0, cursor="hand2", command=lambda: modifyTheYear(1))
        forwardYearButton.image = forward_arrow
        forwardYearButton.pack(side="right", anchor="n", padx=2, fill="y")
        backYearButton = tk.Button(yearHitbox, bg=yearHitbox["bg"], activebackground=yearHitbox["bg"], image=back_arrow, bd=0, cursor="hand2", command=lambda: modifyTheYear(-1))
        backYearButton.image = back_arrow
        backYearButton.pack(side="left", anchor="n", padx=2, fill="y")
        yearLabel = tk.Label(yearHitbox, bg=yearHitbox["bg"], text=dataTeraz.year, fg="white", font=("Arial", 12, "bold"))
        yearLabel.pack(side="left", anchor="center", padx=2, fill="both", expand=True)

        txt = str(dataTeraz.month)
        if len(txt) < 2:
            txt = "0" + txt
        forwardMonthButton = tk.Button(monthHitbox, bg=monthHitbox["bg"], activebackground=monthHitbox["bg"], image=forward_arrow, bd=0, cursor="hand2", command=lambda: modifyTheMonth(1))
        forwardMonthButton.image = forward_arrow
        forwardMonthButton.pack(side="right", anchor="n", padx=2, fill="y")
        backMonthButton = tk.Button(monthHitbox, bg=monthHitbox["bg"], activebackground=monthHitbox["bg"], image=back_arrow, bd=0, cursor="hand2", command=lambda: modifyTheMonth(-1))
        backMonthButton.image = back_arrow
        backMonthButton.pack(side="left", anchor="n", padx=2, fill="y")
        monthLabel = tk.Label(monthHitbox, bg=monthHitbox["bg"], text=txt, fg="white", font=("Arial", 12, "bold"))
        monthLabel.pack(side="left", anchor="center", padx=2, fill="both", expand=True)

        #for better effects I put the "Accept & Reset" buttons in this function
        def save_the_date():
            dateRN = datetime.now()
            global yearLabel, monthLabel
            settings["year"] = yearLabel["text"] # this is already int
            if settings["year"] == dateRN.year:
                settings["year"] = 0
            settings["month"] = int(monthLabel["text"])
            if settings["month"] == dateRN.month:
                settings["month"] = 0
            create_sleep_journal_tab()
            kontentSleepJournal.pack(fill="both", expand=True)

        def reset_the_date():
            settings["year"] = 0
            settings["month"] = 0
            dateRN = datetime.now()
            yearLabel.config(text=dateRN.year)
            txt = str(dateRN.month)
            if len(txt) < 2:
                txt = "0" + txt
            monthLabel.config(text=txt)
            save_the_date()

        controlButtonsFont = font.Font(family="Arial", size=14, weight="bold")
        goButton = tk.Button(dateButtonsHitbox, bg="green2", activebackground="green3", cursor="hand2", activeforeground="white", text="Go", font=controlButtonsFont, fg="white", bd=0, command=save_the_date)
        goButton.pack(side="right", anchor="center", padx=2, fill="y", expand=True)
        resetButton = tk.Button(dateButtonsHitbox, bg= "DarkOrchid1", fg="white", activebackground="DarkOrchid3", activeforeground="white", text="Reset", font=controlButtonsFont, cursor="hand2", bd=0, command=reset_the_date)
        resetButton.pack(side="left", anchor="center", padx=2, fill="y", expand=True)

    root.after(5, add_content_to_date_label)

previousOpened = None
textEditorClass = None
def show_tab(name=None, dreamDay=None):
    global previousOpened
    global textEditorClass

    if previousOpened == name:
        return
    elif previousOpened == "Dream":
        textEditorClass.destroy()
        del textEditorClass
        textEditorClass = None

    if name == "Sleep Journal":
        anim.show_button(reset=True)
        create_sleep_journal_tab()
    if previousOpened and previousOpened != "Dream":
        guziczkiZakladek[previousOpened].config(bg=root["bg"])
    if name:
        guziczkiZakladek[name].config(bg="grey20")
        kontentZakladek[name].pack(fill="both", expand=True)
    else:
        #mamy doczynienia ze snem
        textEditorClass = TextEditor(root, kontentZakladek["Dream"], settings, get_a_nc_file(dataTeraz.strftime("%m-%Y"), dreamDay))
        kontentZakladek["Dream"].pack(fill="both", expand=True)

    if previousOpened:
        kontentZakladek[previousOpened].pack_forget()
    previousOpened = name or "Dream"

show_tab("Sleep Journal")

def onClose():
    if textEditorClass:
        if guziczkiZakladek["Exit"]["text"] != NOT_SAVED_EXIT_TEXT and textEditorClass.hasMadeAnyModyfications:
            guziczkiZakladek["Exit"].config(bg="red4", text=NOT_SAVED_EXIT_TEXT, activebackground="red4")
            root.after(5000, lambda: guziczkiZakladek["Exit"].config(bg="red3", text="Exit", activebackground="red3"))
            return
    guziczkiZakladek["Exit"].config(text="Bye!")
    settings["lucidPoints"] = lucidEntry.get()
    save_settings(settings)
    root.destroy()
    getFiles.delete_empty_directors()
root.protocol("WM_DELETE_WINDOW", onClose)

#podpięcie przycisków
for name, btn in guziczkiZakladek.items():
    if name == "Help":
        btn.config(command=lambda: openWeb(HELP_FILE_PATH))
    elif name == "Exit":
        btn.config(command=onClose)
    else:
        btn.config(command=lambda n=name: show_tab(n))

root.deiconify()
root.mainloop()
