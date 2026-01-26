import customtkinter as ctk
import ctksidebar

def collapse(*args):
    print("collapse")
    side.configure(width=50)

def expand(*args):
    print("expand")
    side.configure(width=200)

def collapse_or_expand(*args):
    global collapsed
    print("collapse_or_expand")
    if collapsed:
        side.configure(width=200)
        collapsed = False
    else:
        side.configure(width=50)
        collapsed = True


collapsed=False
app=ctk.CTk()
app.geometry("500x500")
navigator=ctksidebar.CTkSidebarNavigation(app,width=200)
side=navigator.sidebar
navigator.pack(fill="both", expand=True)
#items={"home":side.add_item(text="", id="hi",command=collapse)}
ctk.CTkButton(side,command=collapse_or_expand,text="///").pack(side="top")
navigator.pack_propagate(False)
side.pack_propagate(False)

app.mainloop()