""" Main view
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, csvmodel, sessionpars, *args, **kwargs):
    #def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self.csvmodel = csvmodel
        self.sessionpars = sessionpars

        frm_Main = ttk.Frame(self)
        frm_Main.grid(padx=200, pady=300)

        ttk.Label(frm_Main, text="Main app interface goes here").grid()
        ttk.Button(frm_Main, text="Save", command=self._on_save).grid()


    def _on_save(self):
        print("View_Main_33: Calling save record function...")
        self.event_generate('<<SaveRecord>>')
