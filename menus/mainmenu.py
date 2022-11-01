""" Main Menu class for Speech Task Controller 

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import messagebox

# Import misc packages
import webbrowser
import markdown


#########
# BEGIN #
#########
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
        self.file_menu = tk.Menu(self, tearoff=False)
        self.file_menu.add_command(
            label="Session...",
            command=self._event('<<FileSession>>')
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Quit",
            command=self._event('<<FileQuit>>')
        )
        self.add_cascade(label='File', menu=self.file_menu)

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
        help_menu.add_command(
            label='Help',
            command=self.show_help
        )
        # Add help menu to the menubar
        self.add_cascade(label="Help", menu=help_menu)


    def show_about(self):
        """ Show the about dialog 
        """
        about_message = 'Speech Task Controller'
        about_detail = (
            'Written by: Travis M. Moore\n'
            'Version 2.1.0\n'
            'Created: Jun 23, 2022\n'
            'Last Edited: Nov 2, 2022'
        )
        messagebox.showinfo(
            title='About',
            message=about_message,
            detail=about_detail
        )


    def show_help(self):
        """ Create html help file and display 
            in default browser
        """
        # Read markdown file and convert to html
        with open('README.md', 'r') as f:
            text = f.read()
            html = markdown.markdown(text)

        # Create html file for display
        with open('README.html', 'w') as f:
            f.write(html)

        # Open html file in default browser
        webbrowser.open('README.html')
