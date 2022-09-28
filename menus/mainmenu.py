""" Main Menu class for Presentation Controller 
"""

# Import GUI packages
import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Menu):
    """ Main Menu
    """
    # Find parent window and tell it to 
    # generate a callback sequence
    def _event(self, sequence):
        def callback(*_):
            root = self.master.winfo_toplevel()
            root.event_generate(sequence)
        return callback


    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # File menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(
            label="Session...",
            command=self._event('<<FileSession>>')
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>')
        )
        self.add_cascade(label='File', menu=file_menu)

        # Tools menu
        tools_menu = tk.Menu(self, tearoff=False)
        tools_menu.add_command(
            label='Audio Settings...',
            command=self._event('<<ToolsAudioSettings>>')
        )
        tools_menu.add_command(
            label='Calibration...',
            command=self._event('<<ToolsCalibration>>')
        )
        # Add Tools menu to the menubar
        self.add_cascade(label="Tools", menu=tools_menu)

        # Help menu
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(
            label='About',
            command=self.show_about
        )
        # Add help menu to the menubar
        self.add_cascade(label="Help", menu=help_menu)


    def show_about(self):
        """ Show the about dialog """
        about_message = 'Presentation Controller'
        about_detail = (
            'Written by: Travis M. Moore\n'
            'Version 2.0.0\n'
            'Created: Jun 23, 2022\n'
            'Last Edited: Sep 28, 2022'
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )
