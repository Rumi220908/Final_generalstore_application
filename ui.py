
import customtkinter as ctk
from tkinter import ttk,messagebox
from datetime import datetime
from database import *
import matplotlib.pyplot as plt

OLIVE="#708238"
WHITE="#ffffff"

class StoreApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        init()
        self.title("General Store")
        self.geometry("1400x850")
        self.configure(fg_color=WHITE)

        side=ctk.CTkFrame(self,fg_color="#161616",width=220)
        side.pack(side="left",fill="y")

        body=ctk.CTkFrame(self,fg_color=WHITE)
        body.pack(fill="both",expand=True)

        self.frames={}
        for name in ["Purchase","Sales","Stock","Analytics"]:
            b=ctk.CTkButton(side,text=name,fg_color=OLIVE,
                            command=lambda n=name:self.show(n))
            b.pack(padx=15,pady=15,fill="x")
            f=ctk.CTkFrame(body,fg_color=WHITE)
            self.frames[name]=f

        self.build_form(self.frames["Purchase"],"Purchase")
        self.build_form(self.frames["Sales"],"Sale")
        self.stock_view()
        self.analytics()
        self.show("Purchase")

    def clear(self):
        for f in self.frames.values():
            f.pack_forget()

    def show(self,n):
        self.clear()
        self.frames[n].pack(fill="both",expand=True)

    def build_form(self,frame,action):
        item=ctk.CTkEntry(frame,placeholder_text="Product")
        qty=ctk.CTkEntry(frame,placeholder_text="Quantity")
        price=ctk.CTkEntry(frame,placeholder_text="Price")
        for w in [item,qty,price]:
            w.pack(pady=10,padx=40)

        lbl=ctk.CTkLabel(frame,text="")
        lbl.pack()

        def calc():
            try:
                lbl.configure(text=f"₹ {int(qty.get())*float(price.get())}")
            except: pass

        qty.bind("<KeyRelease>",lambda e:calc())
        price.bind("<KeyRelease>",lambda e:calc())

        def save():
            try:
                now=datetime.now()
                add_tx(item.get().title(),action,int(qty.get()),
                       float(price.get()),
                       now.strftime("%d/%m/%Y"),
                       now.strftime("%H:%M:%S"))
                messagebox.showinfo("Saved","Transaction stored")
            except Exception as e:
                messagebox.showerror("Error",str(e))

        ctk.CTkButton(frame,text=f"Save {action}",
                      fg_color=OLIVE,
                      command=save).pack()

    def stock_view(self):
        f=self.frames["Stock"]
        tree=ttk.Treeview(f,columns=("item","qty"),show="headings")
        tree.heading("item",text="Product")
        tree.heading("qty",text="Stock")
        for r in stock():
            tree.insert("",'end',values=r)
        tree.pack(fill="both",expand=True)

    def analytics(self):
        f=self.frames["Analytics"]
        ctk.CTkLabel(
            f,
            text="Use monthly transactions from SQLite and run graphs locally",
            text_color="black").pack(pady=40)
