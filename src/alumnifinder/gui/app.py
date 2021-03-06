import tkinter
from tkinter import filedialog as fd

from pandas import ExcelWriter, DataFrame

from src.alumnifinder.excel.handler import Handler
from src.alumnifinder.finder.crawler import Crawler
from src.alumnifinder.gui import images
from src.alumnifinder.utils import jsonwriter as json_writer


class App:
    def __init__(self, master):
        self.master = master  # used to access master in other functions
        master.title("UB LinkedIn Alumni People Finder")
        master.resizable(width=False, height=False)
        frame = tkinter.Frame(master)
        frame.pack()
        frame.config(padx=5, pady=5)
        self.input_file_name = ''
        self.client_entry = {}

        try:
            self.logo = tkinter.PhotoImage(file=images.logo_path)
            self.error_icon = tkinter.PhotoImage(file=images.error_icon_path)
        except FileNotFoundError as e:
            raise e

        self.logo = self.logo.subsample(5, 5)
        self.ub_logo = tkinter.Label(frame, image=self.logo)
        self.ub_logo.grid(row=0)
        master.tk.call('wm', 'iconphoto', master._w, self.logo)  # sets UB logo as icon

        self.app_title = tkinter.Label(frame, text="UB LinkedIn Alumni People Finder")
        self.app_title.grid(row=0, column=0, columnspan=3)

        # left side; manual option fields
        start_row = 2
        self.left_label = tkinter.Label(frame, text="Enter Search Criteria.")
        self.left_label.grid(row=1, columnspan=2)
        self.l1 = tkinter.Label(frame, text="Geolocation: ")
        self.l2 = tkinter.Label(frame, text="Job Position/Title: ")
        self.l3 = tkinter.Label(frame, text="Start Row: ")
        self.l4 = tkinter.Label(frame, text="End Row: ")
        # self.l5 = Label(frame, text="Major: ")
        # self.l6 = Label(frame, text="Degree: ")
        self.l1.grid(row=start_row, sticky=tkinter.W)
        self.l2.grid(row=start_row + 1, sticky=tkinter.W)
        self.l3.grid(row=start_row + 2, sticky=tkinter.W)
        self.l4.grid(row=start_row + 3, sticky=tkinter.W)

        self.e1 = tkinter.Entry(frame)  # geolocation
        self.e2 = tkinter.Entry(frame)  # job position/title
        self.e3 = tkinter.Entry(frame)  # start row
        self.e4 = tkinter.Entry(frame)  # end row
        self.e1.grid(row=start_row, column=1)
        self.e2.grid(row=start_row + 1, column=1)
        self.e3.grid(row=start_row + 2, column=1)
        self.e4.grid(row=start_row + 3, column=1)

        ok_button = tkinter.Button(frame, text="   OK   ", command=self.ok_button)
        ok_button.grid(row=start_row + 6, columnspan=5, pady=5)
        # end manual option fields

        # right side, file explorer for excel file
        self.right_lable = tkinter.Label(frame, text="Search for a document.")
        self.right_lable.grid(row=1, column=2, padx=5)
        self.right_file_path_entry = tkinter.Entry(frame)
        self.right_file_path_entry.config(state="readonly", width=35)
        self.right_file_path_entry.grid(row=start_row, column=2, padx=5)
        open_file_button = tkinter.Button(frame, text="...", command=self.search_file)
        open_file_button.grid(row=start_row, column=3)

        self.right_save_label = tkinter.Label(frame, text="Choose a save location")
        self.right_save_label.grid(row=start_row + 1, column=2, padx=5)
        self.right_save_path_entry = tkinter.Entry(frame)

        self.right_save_path_entry.config(state="readonly", width=35)
        self.right_save_path_entry.grid(row=start_row + 2, column=2, padx=5)
        save_file_button = tkinter.Button(frame, text="...", command=self.search_save)
        save_file_button.grid(row=start_row + 2, column=3)
    # end file input

        self.launch_username_password_input()

    def launch_username_password_input(self):
        self.up_top = tkinter.Toplevel()
        self.up_top.title("Enter Credentials")
        self.up_top.iconphoto(self.up_top._w, self.logo)
        self.up_top.resizable(width=False, height=False)
        # this overrides what normally happens when the 'X' button is pressed
        # the reason we want to do this is because normally if a user presses the 'X'
        # button it allows them to skip password and username entering and access
        # the program without a username and password. This would cause problems
        # so we want to override the 'X' button to kill the entire program
        # when it is pressed
        # lambda allows for an argument to be passed
        self.up_top.protocol('WM_DELETE_WINDOW',self.xbutton_pressed)
        message = tkinter.Label(self.up_top, text="Enter username and password for dummy account.")
        message.configure(padx=5, pady=5)
        message.grid(row=0,column=0,columnspan=3)
        username_label = tkinter.Label(self.up_top, text="Username:")
        password_label = tkinter.Label(self.up_top, text="Password:")
        username_label.grid(row=1,column=0)
        password_label.grid(row=2,column=0)
        self.username_entry = tkinter.Entry(self.up_top,width=35)
        self.password_entry = tkinter.Entry(self.up_top,show="*",width=35)
        self.username_entry.grid(row=1,column=1,columnspan=2, padx=5, pady=5)
        self.password_entry.grid(row=2,column=1,columnspan=2, padx=5, pady=5)
        ok_btn = tkinter.Button(self.up_top,text=" OK ",command=self.username_password_ok)
        self.show_password_toggle = tkinter.Button(self.up_top,text="Show Password",command=self.show_password)
        self.showing_password = False;
        ok_btn.grid(row=3,column=2,padx=5,pady=5)
        self.show_password_toggle.grid(row=3,column=0,columnspan=2,padx=5,pady=5)

        # position error in center of root window
        self.up_top.update()  # update gets the latest winfo data
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()
        self.up_top_width = self.up_top.winfo_width()
        self.up_top_height = self.up_top.winfo_height()
        final_x = root_x + ((root_width / 2) - (self.up_top_width / 2))
        final_y = root_y + ((root_height / 2) - (self.up_top_height / 2))
        self.up_top.geometry("%dx%d+%d+%d" % (self.up_top_width, self.up_top_height, final_x, final_y))

        # grabs focus for self.up_top so bottom window can't be interacted with until self.up_top is gone
        self.up_top.grab_set()

    def xbutton_pressed(self):
        self.master.destroy()

    def username_password_ok(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if username == '':
            self.error_pop_up("Username cannot be empty")
            self.up_top.grab_release()
        elif password == '':
            self.error_pop_up("Password cannot be empty")
            self.up_top.grab_release()
        else:
            #TODO store username and password to creds.json
            json_writer.store_creds(username, password)
            self.up_top.destroy()

    def show_password(self):
        if(self.showing_password):
            self.password_entry.configure(show="*")
            self.show_password_toggle.configure(text="Show Password")
        else:
            self.password_entry.configure(show="")
            self.show_password_toggle.configure(text="Hide Password")
        self.showing_password = not self.showing_password

    def search_save(self):
        save_location = fd.askdirectory(initialdir="/", title="Choose Where to Save")  # returns a string
        if save_location is None:
            print("No file selected")
        else:
            self.right_save_path_entry.config(state=tkinter.NORMAL)
            self.right_save_path_entry.delete(0, last=tkinter.END)
            self.right_save_path_entry.insert(0, save_location)
            self.right_save_path_entry.config(state="readonly")

    def search_file(self):
        valid_file_types = ("*.xlsx", "*.xls")
        file = fd.askopenfile(initialdir="/", title="Select file",  # returns a file
                              filetypes=[("Excel Files", valid_file_types), ("All Files", "*.*")])
        # xlsx
        if file is None:
            print("No File Selected")
        else:
            file_extension = file.name.split('.')
            if file_extension[1] != "xlsx" and file_extension[1] != "xls":
                types = ""
                for x in valid_file_types:
                    if x == valid_file_types[-1]:
                        types += x
                    else:
                        types += x + ", "
                self.error_pop_up("File type invalid.\nValid file types are: " + types)
            else:
                if self.right_save_path_entry.get() == "":
                    self.set_save_dir(file.name)
                self.right_file_path_entry.config(state=tkinter.NORMAL)
                self.right_save_path_entry.delete(0, last=tkinter.END)
                self.right_file_path_entry.delete(0, last=tkinter.END)
                self.right_file_path_entry.insert(0, file.name)
                self.right_file_path_entry.config(state="readonly")
                # parse input file name from the absolute path
                self.input_file_name = file_extension[0].split('/')[-1]

    # method to set the default save dir when a file is chosen. Sets the same
    # dir that the file is in as default
    def set_save_dir(self, file_path):
        path_arr = file_path.split('/')

        # this cuts off the file name held at last index of pathAr.
        # the ' - 1' cuts off the last slash from dir name
        end_of_dir = len(file_path) - len(path_arr[-1]) - 1

        self.right_save_path_entry.config(state=tkinter.NORMAL)
        self.right_save_path_entry.delete(0, last=tkinter.END)
        self.right_save_path_entry.insert(0, file_path[:end_of_dir])
        self.right_save_path_entry.config(state="readonly")

    def get_output_frame(self, columns: list) -> DataFrame:
        """generate a pandas DataFrame to write search result

        Returns:
            pandas DataFrame
        """
        output_frame = DataFrame(data='', index=[0], columns=columns)
        return output_frame

    def save_file(self, output_frame: DataFrame, columns: list, start=None, end=None) -> None:
        """Format the DataFrame and save it as Excel file

         Args:
             output_frame(pandas DataFrame): the instance of DataFrame that used by the crawler
        """
        save_file_name = ''
        if start and end:
            save_file_name += '/' + str(start) + '_to_' + str(end) + '_' + self.input_file_name + '.xlsx'
        else:
            save_file_name += '/all_range_' + self.input_file_name + '.xlsx'

        writer = ExcelWriter(self.right_save_path_entry.get() + save_file_name, engine='xlsxwriter')
        output_frame.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        workbook.set_size(2800, 1200)
        worksheet = writer.sheets['Sheet1']
        worksheet.set_zoom(100)
        size = len(columns)
        worksheet.set_column('A:'+chr(ord('A')+size-1), 25)
        writer.save()

    def error_pop_up(self, text):
        top = tkinter.Toplevel()
        top.title("Error")
        top.iconphoto(top._w, self.error_icon)
        top.configure(width=100)
        top.resizable(width=False, height=False)
        message = tkinter.Message(top, text=text, justify="center")
        message.configure(width=250, padx=25, pady=25)
        message.pack()

        # position error in center of root window
        top.update()  # update gets the latest winfo data
        root_x = self.master.winfo_x()
        root_y = self.master.winfo_y()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()
        top_width = message.winfo_width()
        top_height = message.winfo_height()
        final_x = root_x + ((root_width / 2) - (top_width / 2))
        final_y = root_y + ((root_height / 2) - (top_height / 2))
        top.geometry("%dx%d+%d+%d" % (top_width, top_height, final_x, final_y))

        # grabs focus for top so bottom window can't be interacted with until top is gone
        top.grab_set()
        self.master.wait_window(top)
        top.grab_release()

    def check_path_save(self, file_path: str, save_path: str) -> bool:
        """Checks file and save path"""
        if not file_path:
            self.error_pop_up("Please choose a file to search from.")
            return False
        elif not save_path:
            self.error_pop_up("Please choose a save location.")
            return False
        else:
            return True

    def check_start_end(self, start_row: str, end_row: str) -> bool:
        """Checks start and end rows"""
        if start_row and not end_row:
            self.error_pop_up("Please enter an end row.")
            return False
        elif not start_row and end_row:
            self.error_pop_up("Please enter a start row.")
            return False
        elif start_row and end_row:
            try:
                start = int(start_row)
            except ValueError:
                self.error_pop_up("Please enter a valid integer.")
                return False
            try:
                end = int(end_row)
            except ValueError:
                self.error_pop_up("Please enter a valid integer.")
                return False

            if start < 0:
                self.error_pop_up("Start row cannot be negative.")
                return False
            elif 0 <= start < 2:
                self.error_pop_up("Excel file contains headers, start row cannot be less than 2.")
                return False
            elif end < 0:
                self.error_pop_up("End row cannot be negative.")
                return False
            elif start > end:
                self.error_pop_up("Start row cannot be larger than the end row.")
                return False
            elif end < start:
                self.error_pop_up("End row cannot be smaller than the start row.")
                return False
            else:
                return True
        else:
            return True  # start and end rows not being used

    def is_int(self, start_row: str, end_row: str) -> bool:
        """Checks correct types"""
        try:
            int(start_row)
            int(end_row)
            return True
        except ValueError:
            return False

    def ok_button(self):
        if self.check_path_save(file_path=self.right_file_path_entry.get(), save_path=self.right_save_path_entry.get()):
            start_row = self.e3.get().strip()
            end_row = self.e4.get().strip()
            if self.check_start_end(start_row=start_row, end_row=end_row):  # XNOR check with start/end rows
                self.client_entry["geolocation"] = self.e1.get().strip()
                self.client_entry["job_position"] = self.e2.get().strip()
                if self.is_int(start_row=start_row, end_row=end_row):  # start/end both specified
                    self.client_entry["start_row"] = int(start_row)
                    self.client_entry["end_row"] = int(end_row)
                    start_row = self.client_entry["start_row"]
                    end_row = self.client_entry["end_row"]
                    self.ok_button_helper(start_row=start_row, end_row=end_row)
                else:  # start/end both empty
                    self.ok_button_helper()

    def ok_button_helper(self, start_row=None, end_row=None) -> None:
        excel = Handler(excel_file=self.right_file_path_entry.get(), start=start_row, end=end_row)

        columns = ['ROW_NUMBER', 'ID_NUMBER','KEYWORD', 'FULL_NAME_ON_LINKEDIN', 'JOB_TITLE', 'COMPANY_NAME',
                   'COMPANY_LOCATION', 'PROFILE_LINK', 'ACCURACY_SCORE']
        output_frame = self.get_output_frame(columns)
        c = Crawler(input_data=excel.divided_data, output_data=output_frame, **self.client_entry)
        c.crawl_linkedin()
        self.save_file(output_frame, columns, start=start_row, end=end_row)