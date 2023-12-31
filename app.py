from customtkinter import CTkFrame
import pd
import sys
import ttkbootstrap as tkb
from tkinter import filedialog
from ttkbootstrap.constants import *


def main():
    t1 = TranslatorApp()


class TranslatorApp:
    """
    TranslatorApp Class - TKinter interface
    """

    def __init__(self):
        """
        Initializer method for TranslatorApp Class
        """
        self.root = tkb.Window(themename="darkly")
        self.root.bind("<Escape>", self.quit)
        self.root.iconbitmap(r"bby.ico")
        self.root.iconbitmap(r"bby.ico")
        self.filename_var = tkb.StringVar()
        self.short_filename_var = tkb.StringVar()
        self.char_limit_entry = tkb.StringVar()
        self.radio_var = tkb.IntVar(value=0)
        self.char_limit = tkb.IntVar()
        self.total_rows = 0
        self.completion = 0
        self.create_layout()
        self.root.mainloop()

    def quit(self, event):
        """Quit method terminates the program

        Args:
            event (tkinter.Event): When Escape Key is pressed
        """
        print(event)    
        sys.exit()

    def create_layout(self):
        """
        Method to create the layout for the TKinter interface
        """
        self.root.title("Translation Tool")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        frame = CTkFrame(self.root)
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        dark_frame = tkb.Frame(frame)
        dark_frame.place(relx=0.006, rely=0.01, relwidth=0.215, relheight=0.98)

        label_frame = tkb.Labelframe(dark_frame, text="SKU Translation")
        label_frame.place(relx=0.03, rely=0.01, relheight=0.5, relwidth=0.94)

        label = tkb.Label(master=label_frame, text="Input File", bootstyle="DEFAULT")
        label.place(relx=0.055, rely=0.01)

        filename = tkb.Entry(label_frame, textvariable=self.filename_var)
        filename.place(relx=0.05, rely=0.1, relwidth=0.9)

        browse_button = tkb.Button(
            label_frame,
            text="Browse",
            command=lambda: self.browse_file("translation"),
            bootstyle="LIGHT",
        )
        browse_button.place(relx=0.5, rely=0.25, relwidth=0.44)

        radiobutton_1 = tkb.Radiobutton(
            label_frame,
            text="Entire SKU",
            variable=self.radio_var,
            value=1,
            bootstyle="secondary-outline-toolbutton",
        )
        radiobutton_2 = tkb.Radiobutton(
            label_frame,
            text="Word by Word",
            variable=self.radio_var,
            value=2,
            bootstyle="secondary-outline-toolbutton",
        )
        radiobutton_1.place(relx=0.05, rely=0.4)
        radiobutton_2.place(relx=0.45, rely=0.4)

        run = tkb.Button(label_frame, text="Run", command=self.run)
        run.place(relx=0.05, rely=0.55, relwidth=0.9)

        self.progress = tkb.Progressbar(
            label_frame, mode="determinate", bootstyle="INFO"
        )
        self.progress.place(relx=0.05, rely=0.7, relwidth=0.9)

        self.completion_label = tkb.Label(
            label_frame, text=f"Completed: {self.completion}%"
        )
        self.completion_label.place(relx=0.05, rely=0.76)

        self.file_saved_label = tkb.Label(label_frame, text="File location:")
        self.file_saved_label.place(relx=0.05, rely=0.87)

        self.file_saved_entry = tkb.Entry(label_frame, state="readonly")
        self.file_saved_entry.place(relx=0.45, rely=0.85, relwidth=0.5)

        shortener_label_frame = tkb.Labelframe(dark_frame, text="Description shortener")
        shortener_label_frame.place(relx=0.03, rely=0.52, relheight=0.23, relwidth=0.94)

        short_label = tkb.Label(
            master=shortener_label_frame, text="Input File", bootstyle="DEFAULT"
        )
        short_label.place(relx=0.055, rely=0.01)

        short_filename = tkb.Entry(shortener_label_frame, textvariable=self.short_filename_var)
        short_filename.place(relx=0.05, rely=0.2, relwidth=0.7)

        short_browse_button = tkb.Button(
            shortener_label_frame,
            text="...",
            command= lambda: self.browse_file("shorten"),
            bootstyle="LIGHT",
        )
        short_browse_button.place(relx=0.8, rely=0.2, relwidth=0.15)

        short_char_label = tkb.Label(
            master=shortener_label_frame, text="Chars", bootstyle="DEFAULT"
        )
        short_char_label.place(relx=0.05, rely=0.5)

        short_scale = tkb.Scale(
            shortener_label_frame, from_=0, to=255, variable=self.char_limit
        )
        short_scale.place(relx=0.25, rely=0.525, relwidth=0.7)



        self.short_char_entry = tkb.Entry(
            shortener_label_frame, textvariable=self.char_limit_entry
        )
        self.short_char_entry.place(relx=0.05, rely=0.7, relwidth=0.2)

        self.short_char_entry.insert(0, str(self.char_limit.get()))

        self.char_limit.trace_add("write", self.update_entry)

        shorten = tkb.Button(
            shortener_label_frame, text="Shorten", command=self.shorten
        )
        shorten.place(relx=0.3, rely=0.7, relwidth=0.64)

        word_translator_frame = tkb.Labelframe(dark_frame, text="Translate a word")
        word_translator_frame.place(relx=0.03, rely=0.76, relheight=0.23, relwidth=0.94)

        cols = ("SKU", "DESCRIPTION", "TRANSLATION")

        self.table = tkb.Treeview(
            frame, bootstyle="SECONDARY", columns=cols, show="headings"
        )
        self.table.heading("SKU", text="SKU")
        self.table.column("SKU", width=20, anchor=CENTER)
        self.table.heading("DESCRIPTION", text="DESCRIPTION")
        self.table.heading("TRANSLATION", text="TRANSLATION")
        self.table.place(relx=0.225, rely=0.01, relwidth=0.768, relheight=0.98)

    def update_entry(self, *args):
        self.short_char_entry.delete(0, tkb.END)  # Clear the entry
        self.short_char_entry.insert(0, str(self.char_limit.get()))

    def browse_file(self, id):
        """
        Browse file method is triggered when the browse button is pressed and updates the class variable filename_var
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            if id == "translation":
                self.filename_var.set(file_path)
                print("Selected file:", file_path)
            elif id == "shorten":
                self.short_filename_var.set(file_path)

    def run(self):
        """
        Run method is triggered when the run button is pressed.

        Contains some error handling if the translation mode is not selected and if there is no file selected
        """
        if self.radio_var.get() == 0:
            mb = tkb.dialogs.Messagebox.ok("Please choose a translation mode")
            return
        else:
            translator = pd.BBYTranslator(
                callback_function=self.update_treeview,
                row_callback=self.update_total_rows,
            )

            try:
                directory = translator.read_file(
                    self.filename_var.get(), self.radio_var.get()
                )
                self.file_saved_entry.configure(state="normal")
                self.file_saved_entry.delete(0, tkb.END)
                self.file_saved_entry.insert(0, f"{directory}")
            except:
                mb = tkb.dialogs.Messagebox.ok("Please choose a file")


    def shorten(self):
        if not (0 <= int(self.char_limit_entry.get()) <= 255):
            mb = tkb.dialogs.Messagebox.ok("Enter a value between 0 and 255")

        else:
            try:
                translator = pd.BBYTranslator(
                    callback_function=self.update_treeview,
                    row_callback=self.update_total_rows,
                )

                translator.read_file(self.short_filename_var.get(),3)
            except:
                mb = tkb.dialogs.Messagebox.ok("Please choose a file")

    def update_treeview(self, data_to_print):
        """Callback method for the BBYTranslator Class to update the treeview after each iteration

        Args:
            data_to_print (list): List of values to enter into the treeview
        """
        sku, description, translation = data_to_print
        self.table.insert("", tkb.END, values=(sku, description, translation))
        self.table.yview_moveto(1.0)
        self.table.update_idletasks()

    def update_total_rows(self, row, total_rows):
        """Callback method for the BBYTranslator Class to update the progress bar after each iteration

        Args:
            row (integer): the current row
            total_rows (integer): the total number of rows in the excel file
        """
        percentage_completion = ((row + 1) / total_rows * 100) / 2
        self.progress["value"] = percentage_completion
        if percentage_completion > 100:
            percentage_completion = 100
        self.completion_label["text"] = f"Completed: {percentage_completion:.0f}%"
        self.progress.update_idletasks()


if __name__ == "__main__":
    main()
