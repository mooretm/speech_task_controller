"""Speech task presentation controller.

    Written by: Travis M. Moore
    Created: 23 Jun, 2022
    Last edited: 28 Sep, 2022
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter.messagebox import askyesno, showinfo, showwarning

# Import data science packages
import numpy as np
import pandas as pd

# Import system packages
import os
import sys

# Import custom modules
from lib import tmsignals as ts
import importlib 
importlib.reload(ts) # Reload custom module on every run
# Menu imports
from menus import mainmenu as menu_main
# Model imports
from models import sessionmodel as m_sesspars
from models import audiomodel as m_audio
from models import csvmodel as m_csv
# View imports
from views import main as v_main
from views import session as v_sess
from views import audio as v_aud
from views import calibration as v_cal


#########
# BEGIN #
#########
class Application(tk.Tk):
    """ Application root window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.withdraw() # Hide window during setup
        self.title("Presentation Controller")

        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Track number of trials
        self.counter = 0

        # Load current session parameters from file
        # Or load defaults if file does not exist yet
        self.sessionpars_model = m_sesspars.SessionParsModel()
        self._load_sessionpars()

        # Load CSV writer model
        self.csvmodel = m_csv.CSVModel(self.sessionpars)

        # Load main view
        #self.main_frame = v_main.MainFrame(self, self.model, self.sessionpars)
        self.main_frame = v_main.MainFrame(self, self.csvmodel, self.sessionpars)
        self.main_frame.grid()

        # Load menus
        menu = menu_main.MainMenu(self)
        self.config(menu=menu)

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileSession>>': lambda _: self._show_session_dialog(),
            '<<FileQuit>>': lambda _: self._quit(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),

            # Session dialog commands
            '<<SessionSubmit>>': lambda _: self._save_sessionpars(),

            # Calibration dialog commands
            '<<PlayCalStim>>': lambda _: self._play_calibration(),
            '<<CalibrationSubmit>>': lambda _: self._calc_level(),

            # Audio dialog commands
            '<<AudioDialogSubmit>>': lambda _: self._save_sessionpars(),

            # Mainframe commands
            '<<SaveRecord>>': lambda _: self._on_save()
        }

        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Center main window
        self.center_window()


    #####################
    # General Functions #
    #####################
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


    def resource_path(self, relative_path):
        """ Get the absolute path to compiled resources
        """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def _quit(self):
        """ Exit the application
        """
        self.destroy()


    ########################
    # Main Frame Functions #
    ########################
    def _on_save(self):
        print('App_145: Calling save record function...')
        self.csvmodel.save_record(self.sessionpars)


    ############################
    # Session Dialog Functions #
    ############################
    def _show_session_dialog(self):
        """ Show session parameter dialog
        """
        print("\nApp_125: Calling session dialog...")
        v_sess.SessionDialog(self, self.sessionpars)


    def _load_sessionpars(self):
        """ Load parameters into self.sessionpars dict 
        """
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create runtime dict from session model fields
        self.sessionpars = dict()
        for key, data in self.sessionpars_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.sessionpars[key] = vartype(value=data['value'])
        print("\nApp_125: Loaded sessionpars model fields into " +
            "running sessionpars dict")


    def _save_sessionpars(self, *_):
        """ Save current runtime parameters to file 
        """
        print("\nApp_156: Calling sessionpar model set and save funcs...")
        for key, variable in self.sessionpars.items():
            self.sessionpars_model.set(key, variable.get())
            self.sessionpars_model.save()


    ##########################
    # Audio Dialog Functions #
    ##########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog
        """
        print("\nApp_166: Calling audio dialog...")
        v_aud.AudioDialog(self, self.sessionpars)


    ################################
    # Calibration Dialog Functions #
    ################################
    def _show_calibration_dialog(self):
        print("\nApp_146: Calling calibration dialog...")
        v_cal.CalibrationDialog(self, self.sessionpars)


    def _calc_level(self):
        """ Calculate and save adjusted presentation level
        """
        # Calculate SLM offset
        print("\nApp_155: Calculating new presentation level...")
        slm_offset = self.sessionpars['SLM Reading'].get() - self.sessionpars['Raw Level'].get()
        # Provide console feedback
        print(f"SLM reading: {self.sessionpars['SLM Reading'].get()}")
        print(f"Raw level: {self.sessionpars['Raw Level'].get()}")
        print(f"SLM offset: {slm_offset}")

        # Calculate new presentation level
        self.sessionpars['Adjusted Presentation Level'].set(
            self.sessionpars['Presentation Level'].get() - slm_offset)
        print(f"New presentation level: " +
            f"{self.sessionpars['Adjusted Presentation Level'].get()}")

        # Save SLM offset and updated level
        self._save_sessionpars()


    def _play_calibration(self):
        """ Load calibration file and present
        """
        # Create calibration audio object
        try:
            # If running from compiled, look in compiled temporary location
            cal_file = self.resource_path('cal_stim.wav')
            cal_stim = m_audio.Audio(cal_file, self.sessionpars['Raw Level'].get())
        except FileNotFoundError:
            # If running from command line, look in assets folder
            cal_file = '.\\assets\\cal_stim.wav'
            cal_stim = m_audio.Audio(cal_file, self.sessionpars['Raw Level'].get())

        # Present calibration stimulus
        cal_stim.play(device_id=self.sessionpars['Audio Device ID'].get(), 
            channels=self.sessionpars['Speaker Number'].get())


if __name__ == "__main__":
    app = Application()
    app.mainloop()
