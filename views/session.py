""" Session parameters dialog
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


#########
# BEGIN #
#########
class SessionDialog(tk.Toplevel):
    """ Dialog for setting session parameters
    """
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        self.withdraw()
        self.title("Session")

        options = {'padx':5, 'pady':5}

        frame = ttk.Labelframe(self, text='Session Information')
        frame.grid(column=0, row=0, padx=10, pady=10)

        # Subject
        ttk.Label(frame, text="Subject:"
            ).grid(row=2, column=0, sticky='e', **options)
        ttk.Entry(frame, width=20, 
            textvariable=self.sessionpars['Subject']
            ).grid(row=2, column=1, sticky='w')
        
        # Condition
        ttk.Label(frame, text="Condition:"
            ).grid(row=3, column=0, sticky='e', **options)
        ttk.Entry(frame, width=20, 
            textvariable=self.sessionpars['Condition']
            ).grid(row=3, column=1, sticky='w')

        # Level
        ttk.Label(frame, text="Presentation Level (dB):"
            ).grid(row=4, column=0, sticky='e', **options)
        ttk.Entry(frame, width=20, 
            textvariable=self.sessionpars['Presentation Level']
            ).grid(row=4, column=1, sticky='w')

        # Directory
        frm_path = ttk.LabelFrame(frame, text="Please select audio file directory")
        frm_path.grid(row=5, column=0, columnspan=2, **options, ipadx=5, ipady=5)
        my_frame = frame
        ttk.Label(my_frame, text="Audio File Path:"
            ).grid(row=5, column=0, sticky='e', **options)
        ttk.Label(my_frame, textvariable=self.sessionpars['Audio Files Path'], 
            borderwidth=2, relief="solid", width=60
            ).grid(row=5, column=1, sticky='w')
        ttk.Button(my_frame, text="Browse", command=self._get_directory
            ).grid(row=6, column=1, sticky='w', pady=(0, 5))

        # Submit button
        btn_submit = ttk.Button(self, text="Submit", command=self._on_submit)
        btn_submit.grid(column=0, columnspan=2, row=10, pady=(0,10))

        # Center the session dialog window
        self.center_window()


    def center_window(self):
        """ Center the root window 
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _get_directory(self):
        # Ask user to specify audio files directory
        self.sessionpars['Audio Files Path'].set(filedialog.askdirectory())


    def _on_submit(self):
        print("\nView_Session_92: Sending save event...")
        self.parent.event_generate('<<SessionSubmit>>')
        self.destroy()
