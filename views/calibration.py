""" Calibration dialog class
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
class CalibrationDialog(tk.Toplevel):
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        self.withdraw()
        self.focus()
        self.title("Calibration")

        options = {'padx':10, 'pady':10}
        options_small = {'padx':2.5, 'pady':2.5}

        lf_present = ttk.Labelframe(self, text='Presentation Parameters')
        lf_present.grid(column=0, row=0, **options)

        lf_record = ttk.Labelframe(self, text='Save SLM Value')
        lf_record.grid(column=1, row=0, **options)

        # Raw level
        lbl_play = ttk.Label(lf_present, text="Raw Level (dB FS):").grid(
            column=5, row=5, sticky='e', **options_small)
        ent_slm = ttk.Entry(lf_present, textvariable=self.sessionpars['Raw Level'],
            width=6)
        ent_slm.grid(column=10, row=5, sticky='w', **options_small)
 
        # Play calibration stimulus
        lbl_play = ttk.Label(lf_present, text="Calibration Stimulus:").grid(
            column=5, row=10, sticky='e', **options_small)
        btn_play = ttk.Button(lf_present, text="Play", command=self._on_play)
        btn_play.grid(column=10, row=10, sticky='w', **options_small)
        btn_play.focus()

        # SLM Reading 
        lbl_slm = ttk.Label(lf_record, text="SLM Reading (dB):").grid(
            column=5, row=15, sticky='e', **options_small)
        self.ent_slm = ttk.Entry(lf_record, textvariable=self.sessionpars['SLM Reading'],
            width=6, state='disabled')
        self.ent_slm.grid(column=10, row=15, sticky='w', **options_small)

        # Submit button
        self.btn_submit = ttk.Button(lf_record, text="Submit", 
            command=self._on_submit, state='disabled')
        self.btn_submit.grid(column=5, columnspan=10, row=20, **options_small)

        # Center calibration window dialog
        self.center_window()


    def center_window(self):
        # Center window based on new size
        self.update_idletasks()
        #root.attributes('-topmost',1)
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.deiconify()


    def _on_play(self):
        self.parent.event_generate('<<PlayCalStim>>')
        self.btn_submit.config(state='enabled')
        self.ent_slm.config(state='enabled')


    def _on_submit(self):
        print("\nView_Cal_89: Sending save calibration event...")
        self.parent.event_generate('<<CalibrationSubmit>>')
        self.destroy()
