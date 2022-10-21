""" Main view
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

import string
import numpy as np


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, csvmodel, sessionpars, listmodel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self.csvmodel = csvmodel
        self.sessionpars = sessionpars
        self.listmodel = listmodel
        self.first = True
        self.counter = -1

        # Set widget display options
        self.myFont = tk.font.nametofont('TkDefaultFont').configure(size=10)
        options = {'padx':10, 'pady':10}

        # Create frames
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, sticky='nsew')

        self.frm_sentence = ttk.LabelFrame(frm_main, text='Sentence:', padding=8, width=500, height=80)
        self.frm_sentence.grid(column=5, columnspan=15, row=5, sticky='nsew', 
            **options)
        self.frm_sentence.grid_propagate(0)

        sep = ttk.Separator(frm_main, orient='vertical')
        sep.grid(column=20, row=5, rowspan=50, sticky='ns')

        self.frm_params = ttk.LabelFrame(frm_main, text="Session Info")
        self.frm_params.grid(column=25, row=5, rowspan=15, sticky='n',**options, ipadx=5, ipady=5)

        # Create label textvariables for updating
        self.subject_var = tk.StringVar(value='Subject: ' + self.sessionpars['Subject'].get())
        self.condition_var = tk.StringVar(value='Condition: ' + self.sessionpars['Condition'].get())
        self.level_var = tk.StringVar(value='Level: ' + str(self.sessionpars['Presentation Level'].get()))
        self.list_var = tk.StringVar(value='List(s): ' + self.sessionpars['List Number'].get())
        self.speaker_var = tk.StringVar(value='Speaker: ' + str(self.sessionpars['Speaker Number'].get()))
        self.trial_var = tk.StringVar(value='Trial: NA of NA')

        # Add traces to label textvariables for automatic syncing
        self.subject_var.trace_add('write', self._update_labels)
        self.condition_var.trace_add('write', self._update_labels)
        self.level_var.trace_add('write', self._update_labels)
        self.list_var.trace_add('write', self._update_labels)
        self.speaker_var.trace_add('write', self._update_labels)
        self.trial_var.trace_add('write', self._update_labels)

        # Plot session info labels
        ttk.Label(self.frm_params, textvariable=self.subject_var).grid(sticky='w')
        ttk.Label(self.frm_params, textvariable=self.condition_var).grid(sticky='w')
        #ttk.Label(self.frm_params, textvariable=self.level_var).grid(sticky='w')
        ttk.Label(self.frm_params, textvariable=self.list_var).grid(sticky='w')
        #ttk.Label(self.frm_params, textvariable=self.speaker_var).grid(sticky='w')
        ttk.Label(self.frm_params, textvariable=self.trial_var).grid(sticky='w')

        # lbl_subject = ttk.Label(self.frm_params, text='Subject: ' + self.sessionpars['Subject'].get()).grid(sticky='w')
        # lbl_subject = ttk.Label(self.frm_params, text=self.subject_var.get()).grid(sticky='w')
        # lbl_condition = ttk.Label(self.frm_params, text='Condition: ' + self.sessionpars['Condition'].get()).grid(sticky='w')
        # lbl_level = ttk.Label(self.frm_params, text='Level: ' + str(self.sessionpars['Presentation Level'].get())).grid(sticky='w')
        # lbl_list = ttk.Label(self.frm_params, text='List(s): ' + str(self.sessionpars['List Number'].get())).grid(sticky='w')
        # lbl_speaker = ttk.Label(self.frm_params, text='Speaker: ' + str(self.sessionpars['Speaker Number'].get())).grid(sticky='w')
        # lbl_trial = ttk.Label(self.frm_params, text=self.trial_cnt.get()).grid(sticky='w')

        # Score buttons
        ttk.Label(frm_main, text='Step (dB)').grid(column=6, row=10, sticky='w')

        self.btn_right = ttk.Button(frm_main, text='Start', command=self._on_right)
        self.btn_right.grid(column=5, row=15, pady=(0,10))

        ent_right = ttk.Entry(frm_main, width=5)
        ent_right.grid(column=6, row=15, sticky='w', pady=(0,10))

        self.btn_wrong = ttk.Button(frm_main, text='Wrong', state='disabled')
        self.btn_wrong.grid(column=5, row=20, pady=(0,10))

        ent_wrong = ttk.Entry(frm_main, width=5)
        ent_wrong.grid(column=6, row=20, sticky='w', pady=(0,10))

        # Create list of labels for displaying words
        self.text_vars = list(string.ascii_lowercase)
        self.word_labels = []
        for idx, letter in enumerate(self.text_vars):
            self.text_vars[idx] = tk.StringVar(value='')
            self.lbl_word = ttk.Label(self.frm_sentence, 
                textvariable=self.text_vars[idx], font=self.myFont)
            self.lbl_word.grid(column=idx, row=0)
            self.word_labels.append(self.lbl_word)

        # Create list of checkbuttons for displaying beneath key words
        self.chk_vars = list(string.ascii_uppercase)
        self.word_chks = []
        for idx in range(0, len(self.text_vars)):
            self.chk_vars[idx] = tk.IntVar(value=0)
            self.chk_word = ttk.Checkbutton(self.frm_sentence, 
                text='', takefocus=0, variable=self.chk_vars[idx])
            self.word_chks.append(self.chk_word)


    def _load_listmodel(self):
        self.audio_df = self.listmodel.audio_df
        self.sentence_df = self.listmodel.sentence_df


    def _on_right(self):
        if self.first == True:
            self._load_listmodel()
            self.first = False
            self.btn_right.config(text='Right')
            self.btn_wrong.config(state='enabled')
        #self.event_generate('<<RightButton>>')
        self._next()


    def _next(self):
        self.counter += 1
        self.trial_var.set(f"Trial {self.counter+1} of {len(self.sentence_df)}")
        
        # Call task functions
        self._score()
        self._reset()
        self._display()


    ################################
    # Score and write data to file #
    ################################
    def _score(self):
        if self.counter != 0:
            print(f"Trial {self.counter}:")
            correct = []
            for idx, value in enumerate(self.chk_vars):
                if value.get() != 0:
                    correct.append(self.words[idx])
            print(' '.join(correct) + '\n')


    #####################################
    # Reset all labels and checkbuttons #
    #####################################
    def _reset(self):
        # Reset word label text
        for val in self.text_vars:
            val.set('')
        # Reset word label font
        for lbl in self.word_labels:
            lbl.config(font=('TkDefaultFont 10'))
        # Hide checkbuttons
        for chk in self.word_chks:
            chk.grid_remove()
        # Reset checkbutton values to 0
        for val in self.chk_vars:
            val.set(0)


    ##################################
    # Display words and checkbuttons #
    ##################################
    def _display(self):
        try:
            # Get next sentence and split into a list of words
            self.words = self.sentence_df.loc[self.counter, 'ieee_text'].split()
            # Remove period from last word
            self.words[-1] = self.words[-1][:-1]

            # Display words and checkboxes
            for idx, word in enumerate(self.words):
                if word.isupper() and word != 'A':
                    # Words
                    self.text_vars[idx].set(word)
                    self.word_labels[idx].config(font=('TkDefaultFont 10 underline'))
                    # Checkboxes
                    self.word_chks[idx].grid(column=idx, row=1)
                else:
                    # Words
                    self.text_vars[idx].set(word)
        except KeyError:
            print("Ran out of sentences!")
            self.text_vars[0].set("Done!")
            self.trial_var.set(f"Trial {len(self.sentence_df)} of {len(self.sentence_df)}")
            self.btn_right.config(state='disabled')
            self.btn_wrong.config(state='disabled')
            return


    def _update_labels(self, *_):
        """ Dummy function required by trace to update parameter labels
        """
        pass


    def _on_save(self):
        print("View_Main_81: Calling save record function...")
        self.event_generate('<<SaveRecord>>')
