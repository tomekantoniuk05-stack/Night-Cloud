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
    if previousOpenedButton:
        previousOpenedButton.place_forget()
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