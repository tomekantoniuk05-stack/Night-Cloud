import tkinter as tk
from random import randint
from datetime import datetime, date
import calendar

from PIL import ImageTk, Image
from getFiles import *
import animations as anim
from config import *
from textEditor import TextEditor

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

stop = False
def onClose():
    global stop
    stop = True
    loadingRoot.destroy()
loadingRoot.protocol("WM_DELETE_WINDOW", onClose)
#loadingRoot.after(randint(20, 30) * 100, lambda: loadingRoot.destroy())
loadingRoot.destroy()
loadingRoot.mainloop()
if stop:
    sys.exit(0)

###############################################################################################################

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
logo = logo.resize((int(rozmiar_tab_bar / stosunekLogo), rozmiar_tab_bar), Image.Resampling.LANCZOS)
rozmiar_tab_bar += 20
tk_logo = ImageTk.PhotoImage(logo)
logoLabel = tk.Label(tab_bar, image=tk_logo, bg=tab_bar["bg"])
logoLabel.pack(side="left", padx=10)
logoLabel.image = tk_logo

#dodawanie guziczków :)
nazwyZakladek = ["Sleep Journal", "Comunity Posts", "Sleep Calculator", "Exit", "Help", "Credits"] #3 ostatnie będą w odwrotnej kolejności
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
    if name == "Sleep Journal" or name == "Exit":
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

#sleep journal
konentSleepJournal = tk.Frame(content_frame, bg=root["bg"])
konentSleepJournal.pack(fill="both", anchor="center")
kontentZakladek["Sleep Journal"] = konentSleepJournal

konentSnu = tk.Frame(content_frame, bg=root["bg"])
konentSnu.pack(fill="both", anchor="center")
kontentZakladek["Dream"] = konentSnu

dataTeraz = datetime.now()
pierwszyDzienMiesiaca, liczbaDniWMiesiecu = calendar.monthrange(dataTeraz.year, dataTeraz.month)

calendarFrame = tk.Frame(konentSleepJournal, bg=root["bg"])
calendarFrame.place(rely=0.5, relx=0.5, relheight=0.95, relwidth=0.8, anchor="center")

#creating day name display
dniTygodniaFrame = tk.Frame(calendarFrame, bg="firebrick3", height=75)
dniTygodniaFrame.pack(fill="both", side="top")
for dzien in range(0, 7):
    frameStroke = tk.Frame(dniTygodniaFrame, bg="white", height=75)
    frameStroke.pack(expand=True, fill="both", side="left")
    frame = tk.Frame(frameStroke, bg="white")
    frame.place(rely=0.5, relx=0.5, relheight=0.9, relwidth=0.9, anchor="center")
    textLabel = tk.Label(frame, text=DNI_TYGODNIA[dzien], fg="white", bg="purple2", font=("Arial", 15, "bold"))
    textLabel.pack(fill="both", expand=True, anchor="center")

framesOfTheWeeks = []
framesOfDaysStrokes = []
framesOfDays = []
numberOfDayLabel = []
buttonsOfDreams = []
for week in range(1, 7):
    frameTygodnia = tk.Frame(calendarFrame, bg=root["bg"], height=150)
    frameTygodnia.pack(fill="both", side="top", expand=True)
    framesOfTheWeeks.append(frameTygodnia)
    for day in range(1, 8):
        dayFrameStroke = tk.Frame(frameTygodnia, bg="white", height=100)
        dayFrameStroke.pack(expand=True, fill="both", side="left")
        framesOfDaysStrokes.append(dayFrameStroke)
        #to była ramka, teraz pora na zawartość
        dayFrame = tk.Frame(dayFrameStroke, bg=root["bg"])
        dayFrame.place(rely=0.5, relx=0.5, relheight=0.9, relwidth=0.9, anchor="center")
        framesOfDays.append(dayFrame)
        #teraz data
        dayNr = (week-1)*7+day-pierwszyDzienMiesiaca
        dayLabel = tk.Label(dayFrame, text=dayNr, font=("Arial", 16), fg="white", bg=root["bg"])
        dayLabel.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
        numberOfDayLabel.append(dayLabel)
        #teraz guziczki :)
        dreamButton = tk.Button(dayFrame, text="Edit", font=("Arial", 16), fg="white", bg="SlateBlue2", activebackground="RoyalBlue2", bd=0, cursor="hand2", command=lambda day=dayNr: show_tab(None, day))
        #dreamButton.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)
        dayFrame.bind("<Enter>", lambda e, btn=dreamButton: anim.show_button(btn))
        dayFrame.bind("<Leave>", lambda e, btn=dreamButton, frame=dayFrameStroke: anim.hide_button(e, btn, frame))
        buttonsOfDreams.append(dreamButton)
konentSleepJournal.bind("<Enter>", lambda e: anim.show_button())
dniTygodniaFrame.bind("<Enter>", lambda e: anim.show_button())

#usuwanie pierwszych dni poprzedniego tygodnia
dataPoprzedniegoMiesiaca = dataTeraz
if dataTeraz.month == 1:
    date(dataPoprzedniegoMiesiaca.year - 1, 12, 1)
else:
    dataPoprzedniegoMiesiaca = date(dataPoprzedniegoMiesiaca.year, dataPoprzedniegoMiesiaca.month - 1 , 1)

dlugoscPoprzedniegoMiesiaca = calendar.monthrange(dataPoprzedniegoMiesiaca.year, dataPoprzedniegoMiesiaca.month)[1]
for i in range(0, pierwszyDzienMiesiaca):
    frame = framesOfDaysStrokes.pop(0)
    framesOfDays.pop(0)
    frame.config(bg="grey25")
    numberLabel = numberOfDayLabel.pop(0)
    numberLabel.config(text=dlugoscPoprzedniegoMiesiaca-pierwszyDzienMiesiaca+i+1, fg="grey25")
    buttonsOfDreams.pop(0)
#teraz usuwanie ostatnich dni
for i in range(0, len(framesOfDaysStrokes) - liczbaDniWMiesiecu):
    frame = framesOfDaysStrokes.pop(liczbaDniWMiesiecu)
    framesOfDays.pop(liczbaDniWMiesiecu)
    frame.config(bg="grey25")
    numberLabel = numberOfDayLabel.pop(liczbaDniWMiesiecu)
    numberLabel.config(text=i+1, fg="grey25")
    buttonsOfDreams.pop(liczbaDniWMiesiecu)

framesOfDays[dataTeraz.day - 1].config(bg="maroon2")
for kid in framesOfDays[dataTeraz.day - 1].winfo_children():
    if kid["bg"] == root["bg"]:
        kid.config(bg=framesOfDays[dataTeraz.day - 1]["bg"])

previousOpened = None
textEditorFrame = None
def show_tab(name=None, dreamDay=None):
    global previousOpened
    global textEditorFrame
    if previousOpened == name:
        return
    elif previousOpened == "Dream":
        textEditorFrame.destroy()
        del textEditorFrame
    if name == "Sleep Journal":
        anim.show_button()
    if previousOpened and previousOpened != "Dream":
        guziczkiZakladek[previousOpened].config(bg=root["bg"])
    previousOpened = name or "Dream"
    for f in kontentZakladek.values():
        f.pack_forget()
    if name:
        guziczkiZakladek[name].config(bg="grey20")
        kontentZakladek[name].pack(fill="both", expand=True)
    else:
        #mamy doczynienia ze snem
        textEditorFrame = TextEditor(root, kontentZakladek["Dream"], settings, get_a_nc_file(dataTeraz.strftime("%m-%Y"), dreamDay))
        kontentZakladek["Dream"].pack(fill="both", expand=True)

show_tab("Sleep Journal")

def onClose():
    guziczkiZakladek["Exit"].config(text="Bye!")
    save_settings(settings)
    root.destroy()
root.protocol("WM_DELETE_WINDOW", onClose)

#podpięcie przycisków
for name, btn in guziczkiZakladek.items():
    if name != "Exit":
        btn.config(command=lambda n=name: show_tab(n))
    else:
        btn.config(command=onClose)

#print(get_a_nc_file(dataTeraz.strftime("%m-%Y"), dataTeraz.day))
#
root.deiconify()
root.mainloop()
