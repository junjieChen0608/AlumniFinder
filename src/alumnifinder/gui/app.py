# GUI file for LinkedIN People Finder App
# Written by Jared Brown 7/3/17

from sys import platform
from tkinter import *
from tkinter import filedialog as fd

from src.alumnifinder.gui import images

validFileTypes = ("*.xlsx", "*.xls")


# TODO: Implement logger


class App:
    def __init__(self, master):
        self.master = master  # used to access master in other functions
        master.title("UB LinkedIn Alumni People Finder")
        master.resizable(width=False, height=False)
        frame = Frame(master)
        frame.pack()
        frame.config(padx=5, pady=5)
        self.client_entry = {}

        try:
            self.logo = PhotoImage(file=images.logo_path)
            self.errIcon = PhotoImage(file=images.error_icon_path)
        except FileNotFoundError as e:
            raise e

        self.logo = self.logo.subsample(5, 5)
        self.ublogo = Label(frame, image=self.logo)
        self.ublogo.grid(row=0)
        master.tk.call('wm', 'iconphoto', master._w, self.logo)  # sets UB logo as icon

        self.appTitle = Label(frame, text="UB LinkedIn Alumni People Finder")
        self.appTitle.grid(row=0, column=0, columnspan=3)

        # left side; manual option fields
        startRow = 2
        self.leftLabel = Label(frame, text="Enter Search Criteria.")
        self.leftLabel.grid(row=1, columnspan=2)
        self.l1 = Label(frame, text="Geolocation: ")
        self.l2 = Label(frame, text="Job Position/Title: ")
        self.l3 = Label(frame, text="Start Row: ")
        self.l4 = Label(frame, text="End Row: ")
        # self.l5 = Label(frame, text="Major: ")
        # self.l6 = Label(frame, text="Degree: ")
        self.l1.grid(row=startRow, sticky=W)
        self.l2.grid(row=startRow + 1, sticky=W)
        self.l3.grid(row=startRow + 2, sticky=W)
        self.l4.grid(row=startRow + 3, sticky=W)

        self.e1 = Entry(frame)  # geolocation
        self.e2 = Entry(frame)  # job position/title
        self.e3 = Entry(frame)  # start row
        self.e4 = Entry(frame)  # end row
        self.e1.grid(row=startRow, column=1)
        self.e2.grid(row=startRow + 1, column=1)
        self.e3.grid(row=startRow + 2, column=1)
        self.e4.grid(row=startRow + 3, column=1)

        okbtn = Button(frame, text="   OK   ", command=self.ok_button)
        okbtn.grid(row=startRow + 6, columnspan=5, pady=5)
        # end manual option fields

        # right side, file explorer for excel file
        self.rightLabel = Label(frame, text="Search for a document.")
        self.rightLabel.grid(row=1, column=2, padx=5)
        self.rightFilePathEntry = Entry(frame)
        self.rightFilePathEntry.config(state="readonly", width=35)
        self.rightFilePathEntry.grid(row=startRow, column=2, padx=5)
        openFileBtn = Button(frame, text="...", command=self.search_file)
        openFileBtn.grid(row=startRow, column=3)

        self.rightSaveLabel = Label(frame, text="Choose a save location")
        self.rightSaveLabel.grid(row=startRow + 1, column=2, padx=5)
        self.rightSavePathEntry = Entry(frame)

        self.rightSavePathEntry.config(state="readonly", width=35)
        self.rightSavePathEntry.grid(row=startRow + 2, column=2, padx=5)
        saveFileBtn = Button(frame, text="...", command=self.search_save)
        saveFileBtn.grid(row=startRow + 2, column=3)

    # end file input

    def search_save(self):
        save_location = fd.askdirectory(initialdir="/", title="Choose Where to Save")  # returns a string
        if save_location is None:
            print("No file selected")
        else:
            self.rightSavePathEntry.config(state=NORMAL)
            self.rightSavePathEntry.delete(0, last=END)
            self.rightSavePathEntry.insert(0, save_location)
            self.rightSavePathEntry.config(state="readonly")

    def search_file(self):
        file = fd.askopenfile(initialdir="/", title="Select file",  # returns a file
                              filetypes=[("Excel Files", validFileTypes), ("All Files", "*.*")])
        # xlsx
        if file is None:
            print("No File Selected")
        else:
            type = file.name.split('.')
            if type[1] != "xlsx" and type[1] != "xls":
                types = ""
                for x in validFileTypes:
                    if x == validFileTypes[-1]:
                        types += x
                    else:
                        types += x + ", "
                self.error_pop_up("File type invalid.\nValid file types are: " + types)
            else:
                if self.rightSavePathEntry.get() == "":
                    self.set_save_dir(file.name)
                self.rightFilePathEntry.config(state=NORMAL)
                self.rightSavePathEntry.delete(0, last=END)
                self.rightFilePathEntry.insert(0, file.name)
                self.rightFilePathEntry.config(state="readonly")

    # method to set the default save dir when a file is chosen. Sets the same
    # dir that the file is in as default
    def set_save_dir(self, filePath):
        if platform.startswith("linux") or platform.startswith("darwin"):
            pathArr = filePath.split('\\')
        else:
            pathArr = filePath.split('/')

        # this cuts off the file name held at last index of pathAr.
        # the ' - 1' cuts off the last slash from dir name
        endOfDir = len(filePath) - len(pathArr[-1]) - 1

        self.rightSavePathEntry.config(state=NORMAL)
        self.rightSavePathEntry.delete(0, last=END)
        self.rightSavePathEntry.insert(0, filePath[:endOfDir])
        self.rightSavePathEntry.config(state="readonly")

    def error_pop_up(self, text):
        top = Toplevel()
        top.title("Error")
        top.iconphoto(top._w, self.errIcon)
        top.configure(width=100)
        top.resizable(width=False, height=False)
        msg = Message(top, text=text, justify="center")
        msg.configure(width=250, padx=25, pady=25)
        msg.pack()

        # position error in center of root window
        top.update()  # update gets the latest winfo data
        rootX = self.master.winfo_x()
        rootY = self.master.winfo_y()
        rootWidth = self.master.winfo_width()
        rootHeight = self.master.winfo_height()
        topWidth = msg.winfo_width()
        topHeight = msg.winfo_height()
        finalX = rootX + ((rootWidth / 2) - (topWidth / 2))
        finalY = rootY + ((rootHeight / 2) - (topHeight / 2))
        top.geometry("%dx%d+%d+%d" % (topWidth, topHeight, finalX, finalY))

        # grabs focus for top so bottom window can't be interacted with until top is gone
        top.grab_set()
        self.master.wait_window(top)
        top.grab_release()

    def check_path_save(self):
        """Checks file and save path"""
        if self.rightFilePathEntry.get() == '':
            self.error_pop_up("Please choose a file to search from.")
        elif self.rightSavePathEntry.get() == '':
            self.error_pop_up("Please choose a save location.")
        else:
            self.client_entry['geo_location'] = self.e1.get().strip()
            self.client_entry['job_position'] = self.e2.get().strip()

    def check_start_end(self):
        """Checks start and end rows"""
        if self.e3.get().strip() != '' and self.e4.get().strip() == '':
            self.error_pop_up("Please enter an end row.")
        elif self.e3.get().strip() == '' and self.e4.get().strip() != '':
            self.error_pop_up("Please enter a start row.")
        elif self.e3.get().strip() != '' and self.e4.get().strip() != '':
            try:
                self.client_entry['startRow'] = int(self.e3.get().strip())
                self.client_entry['endRow'] = int(self.e4.get().strip())
            except ValueError:
                self.error_pop_up("Please enter a valid integer.")

            # TODO: add more error catching
            if self.client_entry['startRow'] < 0:
                self.error_pop_up("Start row cannot be negative.")
            elif self.client_entry['startRow'] >= 0 and self.client_entry['startRow'] < 2:
                self.error_pop_up("Excel file contains headers, start row cannot be less than 2.")
            elif self.client_entry['endRow'] < 0:
                self.error_pop_up("End row cannot be negative.")
            elif self.client_entry['startRow'] > self.client_entry['endRow']:
                self.error_pop_up("Start row cannot be larger than the end row.")
            elif self.client_entry['endRow'] < self.client_entry['startRow']:
                self.error_pop_up("End row cannot be smaller than the start row.")
        else:
            pass  # start and end rows not being used

    def ok_button(self):
        self.check_path_save()
        self.check_start_end()
        # TODO: finish the rest.