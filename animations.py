loadingDots = -1
def loadingAnimation(root, label):
    global loadingDots
    loadingDots += 1
    if loadingDots > 3:
        loadingDots = 0
    label.config(text="Loading" + "." * loadingDots)
    root.after(333, lambda: loadingAnimation(root, label))

previousOpenedButton = None #(previous seen edit button)
def show_button(btn=None, reset=False):
    global previousOpenedButton
    if reset:
        previousOpenedButton = None
    elif previousOpenedButton:
        try:
            previousOpenedButton.place_forget()
        except:
            pass

    if btn:
        previousOpenedButton = btn
        btn.place(relx=0.0, rely=0.0, anchor="nw", x=10, y=10)

def hide_button(event, btn, frame):
    x, y = event.x_root, event.y_root

    fx1 = frame.winfo_rootx()
    fy1 = frame.winfo_rooty()
    fx2 = fx1 + frame.winfo_width()
    fy2 = fy1 + frame.winfo_height()

    if not (fx1 < x < fx2 and fy1 < y < fy2):
        btn.place_forget()

def on_lost_focus(event, textPlace, root):
    pressedWidgetClass = event.widget.winfo_containing(event.x_root, event.y_root).winfo_class()
    if event.widget != textPlace and pressedWidgetClass != "Entry" and pressedWidgetClass != "Text":
        stop_writing(root)

def stop_writing(root):
    root.focus_set()

previousPressed = None
def remember_the_last_pressed(event):
    global previousPressed
    previousPressed = event.widget.winfo_containing(event.x_root, event.y_root)

def add_one_ldp(event, entry, button):  # ldp - lucid dream point | button is a label
    global previousPressed
    try:
        if event.widget.winfo_containing(event.x_root, event.y_root) == button and button == previousPressed:
            previousPressed = None
            try:
                value = int(entry.get())
                if value:
                    value += 1
                    entry.delete(0, "end")
                    entry.insert(0, str(value))
            except ValueError:
                pass
    except:
        pass