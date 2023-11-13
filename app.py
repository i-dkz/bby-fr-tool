import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
import pd
import ttkbootstrap as tkb
from ttkbootstrap.constants import *

def main():
    root = tkb.Window(themename="darkly")
    root.iconbitmap(r'bby.ico')
    t1 = TranslatorApp()
    t1.create_layout(root)
    root.mainloop()

class TranslatorApp:
    def __init__(self):
        self.filename_var = ctk.StringVar()
        self.radio_var = tk.IntVar(value=0)
        self.total_rows = 0

    def create_layout(self, root):
        root.title("Translation Tool")
        root.geometry("1000x600")
        root.resizable(False, False)

        frame = ctk.CTkFrame(root)
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        label_frame = tkb.Frame(frame)
        label_frame.place(relx=0.006, rely=0.01, relwidth=0.2, relheight=0.98)

        label = tkb.Label(master=label_frame, text="File", bootstyle="DEFAULT")
        label.place(relx=0.055, rely=0.01)

        # StringVar to store the filename
        filename = tkb.Entry(label_frame, textvariable=self.filename_var)
        filename.place(relx=0.05, rely=0.05, relwidth=0.9)

        browse_button = tkb.Button(
            label_frame,
            text="Browse",
            command=self.browse_file,
            bootstyle="LIGHT",
        )
        browse_button.place(relx=0.5, rely=0.11, relwidth=0.44)

        radiobutton_1 = tkb.Radiobutton(
            label_frame,
            text="Entire SKU",
            command=self.radiobutton_event,
            variable=self.radio_var,
            value=1,
            bootstyle="secondary-outline-toolbutton",
        )
        radiobutton_2 = tkb.Radiobutton(
            label_frame,
            text="Word by Word",
            command=self.radiobutton_event,
            variable=self.radio_var,
            value=2,
            bootstyle="secondary-outline-toolbutton",
        )
        radiobutton_1.place(relx=0.05, rely=0.18)
        radiobutton_2.place(relx=0.45, rely=0.18)
        print(self.radio_var.get())
        # checkbutton = tkb.Checkbutton(label_frame, bootstyle="round-toggle")
        # checkbutton.place(relx=.5, rely=0.18)

        run = tkb.Button(label_frame, text="Run", command=self.run)
        run.place(relx=0.05, rely=0.24, relwidth=0.9)

        self.progress = tkb.Progressbar(label_frame, mode='determinate', bootstyle="INFO")
        self.progress.place(relx=0.05, rely=0.3, relwidth=0.9)

        cols = ('SKU', 'DESCRIPTION', 'TRANSLATION')

        self.table = tkb.Treeview(frame, bootstyle="SECONDARY", columns=cols, show="headings")
        self.table.heading("SKU", text="SKU")
        self.table.column("SKU", width=20, anchor=CENTER)
        self.table.heading("DESCRIPTION", text="DESCRIPTION")
        self.table.heading("TRANSLATION", text="TRANSLATION")
        self.table.place(relx=0.215, rely=0.01, relwidth=0.78, relheight=0.98)



    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.filename_var.set(file_path)
            print("Selected file:", file_path)

    def run(self):
        if self.radio_var.get() == 0:
            mb = tkb.dialogs.Messagebox.ok("Please choose a translation mode")
            return
        else:
            translator = pd.BBYTranslator(callback_function=self.update_treeview, row_callback=self.update_total_rows)
            
            try: 

                translator.read_file(self.filename_var.get(), self.radio_var.get())

            except:
                mb = tkb.dialogs.Messagebox.ok("Please choose a file")

    def update_treeview(self, data_to_print):
        sku, description, translation = data_to_print
        self.table.insert('', tkb.END, values=(sku, description, translation))
        self.table.yview_moveto(1.0)
        self.table.update_idletasks()

    def update_total_rows(self, row, total_rows):
        percentage_completion = ((row + 1) / total_rows * 100) / 2
        self.progress['value'] = percentage_completion
        self.progress.update_idletasks()


if __name__ == "__main__":
    main()
