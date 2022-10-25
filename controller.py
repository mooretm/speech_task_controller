""" Presentation controller

    Written by: Travis M. Moore
    Created: 23 Jun, 2022
    Last edited: 25 Oct, 2022
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk

# Import system packages
import os
import sys
from tkinter import messagebox

# Import data science packages
import numpy as np
import pandas as pd

# Import custom modules
from lib import tmsignals as ts
import importlib 
importlib.reload(ts) # Reload custom module on every run
# Menu imports
from menus import mainmenu as menu_main
# Model imports
from models import sessionmodel as m_sesspars
from models import audiomodel as m_audio
from models import listmodel as m_list
from models import csvmodel as m_csv
from models import scoremodel as m_score
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

        # Root window settings
        self.withdraw() 
        self.title("Presentation Controller")
        self.resizable(False, False)

        # Dictionary to track values per trial
        # Used to calculate summary stats
        self.tracker = {
            'Level': [], # Adjusted presentation levels
            'PC Word': [], # Number of words correct
            'PC Custom': [], # Outcomes (right/wrong; 1/0)
        }
        

        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Track number of trials
        self.counter = -1
        self.first = True

        # Load session parameters
        self.sessionpars_model = m_sesspars.SessionParsModel()
        self._load_sessionpars()

        # Load CSV writer model
        self.csvmodel = m_csv.CSVModel(self.sessionpars)

        # Load list model
        self.listmodel = m_list.StimulusList(self.sessionpars)
        self.listmodel.load()

        # Load score model
        self.scoremodel = m_score.ScoreModel()

        # Load main view
        self.main_frame = v_main.MainFrame(self, self.scoremodel, 
            self.sessionpars, self.listmodel)
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
            '<<SubmitResponse>>': lambda _: self._on_main_submit(),
            '<<MainDone>>': lambda _: self._main_done()
            #'<<SaveRecord>>': lambda _: self._on_save()
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


    # Passing entire listmodel to main to deal with
    # Don't need actual list values in controller 
    #def _load_listmodel(self):
    #    self.audio_df = self.listmodel.audio_df
    #    self.sentence_df = self.listmodel.sentence_df


    ########################
    # Main Frame Functions #
    ########################
    def _on_main_submit(self):
        # Provide feedback to the console
        print(f"\nTrial {self.scoremodel.fields['Trial']}:")
        print(f"Correct: {self.scoremodel.fields['Words Correct']}")
        print(f"Incorrect: {self.scoremodel.fields['Words Incorrect']}")
        print(f"Outcome code: {self.scoremodel.fields['Outcome']}\n")

        # Track values for summary at end
        self.tracker['Level'] = self.sessionpars['Presentation Level'].get()
        self.tracker['PC Word'].append(self.scoremodel.fields['Num Words Correct'])
        self.tracker['PC Custom'].append(self.scoremodel.fields['Outcome'])

        print(self.tracker)


        # Call save function
        self._on_save()
        
        
    def _on_save(self):
        """ Format values and send to csv model
        """
        # Get tk variable values from sessionpars
        data = dict()
        for key in self.sessionpars:
            data[key] = self.sessionpars[key].get()

        # Only write specific sessionpars to file
        drop_list = ['Speaker Number', 'Audio Files Path', 
            'Sentence File Path', 'Audio Device ID', 'Calibration File']
        [data.pop(e) for e in drop_list]

        # Combine sessionpars dict and scoremodel dict for writing
        data.update(self.scoremodel.fields)
        print(data)

        # Save data
        print('App_146: Calling save record function...')
        self.csvmodel.save_record(data)


    def _main_done(self):
        # Calculate some descriptive statistics for display
        num_possible_words = len(self.scoremodel.fields['Words Correct'].split()) + len(self.scoremodel.fields['Words Incorrect'].split())
        print(f'Words per sentence: {num_possible_words}')
        print(f"Total words correct: {np.sum(self.tracker['PC Word'])}")

        snr50 = round(np.mean(self.tracker['Level']), 2)
        pc_word = round((np.sum(self.tracker['PC Word']) / (len(self.tracker['PC Custom'] * num_possible_words))) * 100, 2)
        pc_custom = round((np.sum(self.tracker['PC Custom']) / len(self.tracker['PC Custom'])) * 100, 2)

        messagebox.showinfo(
            title='Done!',
            message='Summary',
            detail=f'SNR 50: {snr50} dB\n' +
                f'Percent Correct (Word): {pc_word}%\n' +
                f'Percent Correct (Custom): {pc_custom}%'
        )

        self.quit()


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

        self.main_frame.subject_var.set('Subject: ' + self.sessionpars['Subject'].get())
        self.main_frame.condition_var.set('Condition: ' + self.sessionpars['Condition'].get())
        #self.main_frame.level_var.set('Level: ' + self.sessionpars['Presentation Level'].get())
        self.main_frame.list_var.set('List(s): ' + self.sessionpars['List Number'].get())
        #self.main_frame.speaker_var.set('Speaker: ' + str(self.sessionpars['Speaker Number'].get()))
        self.main_frame.trial_var.set('Trial: NA of NA')

        # Load in the audio and sentence files
        self.listmodel.load()


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
        # Check for default calibration stimulus request
        if self.sessionpars['Calibration File'].get() == 'cal_stim.wav':
            # Create calibration audio object
            try:
                # If running from compiled, look in compiled temporary location
                cal_file = self.resource_path('cal_stim.wav')
                cal_stim = m_audio.Audio(cal_file, self.sessionpars['Raw Level'].get())
            except FileNotFoundError:
                # If running from command line, look in assets folder
                cal_file = '.\\assets\\cal_stim.wav'
                cal_stim = m_audio.Audio(cal_file, self.sessionpars['Raw Level'].get())
        else: # Custom calibration file was provided
            print("Reading provided calibration file...")
            cal_stim = m_audio.Audio(self.sessionpars['Calibration File'].get(), 
                self.sessionpars['Raw Level'].get())

        # Present calibration stimulus
        cal_stim.play(device_id=self.sessionpars['Audio Device ID'].get(), 
            channels=self.sessionpars['Speaker Number'].get())


if __name__ == "__main__":
    app = Application()
    app.mainloop()
