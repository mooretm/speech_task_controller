""" Main view for speech task controller.

    Written by: Travis M. Moore
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Import text packages
import string # for creating alphabet list

# Import custom modules
from models import audiomodel as a


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, scoremodel, sessionpars, listmodel, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self.scoremodel = scoremodel
        self.sessionpars = sessionpars
        self.listmodel = listmodel
        #self.first = True
        self.counter = 0
        self.outcome = None

        # Set widget display options
        self.myFont = tk.font.nametofont('TkDefaultFont').configure(size=10)
        options = {'padx':10, 'pady':10}


        #################
        # Create frames #
        #################
        # Main content frame
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, sticky='nsew')

        # Words and checkbuttons frame
        self.frm_sentence = ttk.LabelFrame(frm_main, text='Sentence:', 
            padding=8, width=500, height=80)
        self.frm_sentence.grid(column=5, columnspan=15, row=5, sticky='nsew', 
            **options)
        self.frm_sentence.grid_propagate(0)

        # Vertical separator for session info
        sep = ttk.Separator(frm_main, orient='vertical')
        sep.grid(column=20, row=5, rowspan=50, sticky='ns')

        # Session info frame
        self.frm_params = ttk.LabelFrame(frm_main, text="Session Info")
        self.frm_params.grid(column=25, row=5, rowspan=15, sticky='n',
            **options, ipadx=5, ipady=5)


        #######################
        # Session info labels #
        #######################
        # Create session info label textvariables for updating
        self.subject_var = tk.StringVar(
            value='Subject: ' + self.sessionpars['Subject'].get())
        self.condition_var = tk.StringVar(
            value='Condition: ' + self.sessionpars['Condition'].get())
        #self.level_var = tk.StringVar(
        #    value='Level: ' + str(self.sessionpars['Presentation Level'].get()))
        self.list_var = tk.StringVar(
            value='List(s): ' + self.sessionpars['List Number'].get())
        self.speaker_var = tk.StringVar(
            value='Speaker: ' + str(self.sessionpars['Speaker Number'].get()))
        self.trial_var = tk.StringVar(value='Trial: NA of NA')

        # Add traces to label textvariables for automatic syncing
        self.subject_var.trace_add('write', self._update_labels)
        self.condition_var.trace_add('write', self._update_labels)
        #self.level_var.trace_add('write', self._update_labels)
        self.list_var.trace_add('write', self._update_labels)
        self.speaker_var.trace_add('write', self._update_labels)
        #self.trial_var.trace_add('write', self._update_labels)

        # Plot session info labels
        # Subject
        ttk.Label(self.frm_params, 
            textvariable=self.subject_var).grid(sticky='w')
        # Condition
        ttk.Label(self.frm_params, 
            textvariable=self.condition_var).grid(sticky='w')
        # Level
        #ttk.Label(self.frm_params, 
        #   textvariable=self.level_var).grid(sticky='w')
        # Speaker number
        ttk.Label(self.frm_params, 
           textvariable=self.speaker_var).grid(sticky='w')
         # List number(s)  
        ttk.Label(self.frm_params, 
            textvariable=self.list_var).grid(sticky='w')
        # Trial number
        ttk.Label(self.frm_params, 
            textvariable=self.trial_var).grid(sticky='w')


        #################
        # User controls #
        #################
        # "Start" button
        self.btn_start = ttk.Button(frm_main, text='Start',
            command=self._on_start)
        self.btn_start.grid(column=7, row=15, rowspan=2)

        # "Right" button
        self.btn_right = ttk.Button(frm_main, text='Right', state='disabled', 
            command=self._on_right)
        self.btn_right.grid(column=5, row=15, pady=(0,10))

        # "Wrong" button
        self.btn_wrong = ttk.Button(frm_main, text='Wrong', state='disabled',
            command=self._on_wrong)
        self.btn_wrong.grid(column=5, row=20, pady=(0,10))

        # "Right" step size entry
        self.right_var = tk.DoubleVar(value=0.0)
        ent_right = ttk.Entry(frm_main, textvariable=self.right_var, width=5)
        ent_right.grid(column=6, row=15, sticky='w', pady=(0,10))

        # "Wrong" step size entry
        self.wrong_var = tk.DoubleVar(value=0.0)
        ent_wrong = ttk.Entry(frm_main, textvariable=self.wrong_var, width=5)
        ent_wrong.grid(column=6, row=20, sticky='w', pady=(0,10))

        # Level step size label
        ttk.Label(frm_main, text='Step (dB)').grid(column=6, row=10, 
            sticky='w')


        ##########################
        # Words and checkbuttons #
        ##########################
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


    #####################
    # General functions #
    #####################
    def _load_listmodel(self):
        """ Load in current stimulus lists from listmodel
        """
        self.audio_df = self.listmodel.audio_df
        self.sentence_df = self.listmodel.sentence_df


    def _update_labels(self, *_):
        """ Dummy function required by trace to update parameter labels
        """
        pass


    ####################
    # Button functions #
    ####################
    def _on_start(self):
        """ Display/present first trial
        """
        # Clean up buttons
        self.btn_start.grid_remove()
        self.btn_right.config(state='enabled')
        self.btn_wrong.config(state='enabled')

        # Load stimulus lists
        self._load_listmodel()

        # Update trial label
        self.trial_var.set(f"Trial {self.counter+1} of {len(self.sentence_df)}")

        # Display first sentence and present first audio file
        self._display()
        self._play()


    def _on_wrong(self):
        """ Update outcome to incorrect. 
            Call remaining task functions. 
        """
        # Set response outcome to incorrect (0)
        # Based on "wrong" button click
        self.outcome = 0

        # Call series of task functions (same as _on_right)
        self._next2()


    def _on_right(self):
        """ Update outcome to correct.
            Call remaining task functions. 
        """
        # Set response outcome to correct (1)
        # Based on "right" button click
        self.outcome = 1

        # Call series of task functions (same as _on_wrong)
        self._next2()


    ###########################
    # Task process controller #
    ###########################
    def _next2(self):
        """ Control the order of operations after right/wrong 
            buttons have assigned response outcome.
        """
        # Score responses
        self._score()
        # Reset word labels and checkbuttons
        self._reset()
        # Set new level based on right/wrong step size
        self._adjust_level()
        # Calculate raw value to achieve new level
        self._get_level()
        # Update trial counter
        self.counter += 1
        # Update trial label
        self.trial_var.set(f"Trial {self.counter+1} of {len(self.sentence_df)}")
        # Display new word labels and checkbuttons
        self._display()
        self._play()


    ###################
    # Audio functions #
    ###################
    def _adjust_level(self):
        """ Apply right/wrong step size to presentation level
            based on response outcome.
        """
        if self.outcome == 1:
            # Apply step size offset to presentation level
            self.sessionpars['Presentation Level'].set(
                self.sessionpars['Presentation Level'].get() - self.right_var.get()
            )
        elif self.outcome == 0:
            # Apply step size offset to presentation level
            self.sessionpars['Presentation Level'].set(
                self.sessionpars['Presentation Level'].get() + self.wrong_var.get()
                )
        else:
            messagebox.showerror(
                title="Uh oh!",
                message="Something went wrong setting the level! Aborting!"
            )
            self.quit()


    def _get_level(self):
        """ Send event to controller to calculate new 
            raw level for the updated presentation level.
        """
        self.event_generate('<<GetLevel>>')


    def _play(self):
        """ Load next audio file and present it.
        """
        try:
            # Create audio object
            audio = a.Audio(self.audio_df.iloc[self.counter]['path'], 
                self.sessionpars['new_raw_lvl'].get())
            # Present audio
            audio.play(
                device_id=self.sessionpars['Audio Device ID'].get(),
                channels=self.sessionpars['Speaker Number'].get()
                )
        except KeyError:
            print("Audio file does not exist!")


    ##################################
    # Display words and checkbuttons #
    ##################################
    def _display(self):
        """ Display each word. Display checkbutton beneath 
            each key word (capitalized). Underline each 
            key word.
        """
        try:
            # Get next sentence and split into a list of words
            self.words = self.sentence_df.loc[
                self.counter, 'ieee_text'].split()
            # Remove period from last word
            self.words[-1] = self.words[-1][:-1]

            # Display words and checkboxes
            for idx, word in enumerate(self.words):
                if word.isupper() and word != 'A':
                    # Words
                    self.text_vars[idx].set(word)
                    self.word_labels[idx].config(
                        font=('TkDefaultFont 10 underline'))
                    # Checkboxes
                    self.word_chks[idx].grid(column=idx, row=1)
                else:
                    # Words
                    self.text_vars[idx].set(word)
        except KeyError:
            print("Out of sentences!")
            self.text_vars[0].set("Done!")
            self.trial_var.set(f"Trial {len(self.sentence_df)} of " +
                f"{len(self.sentence_df)}")
            self.btn_right.config(state='disabled')
            self.btn_wrong.config(state='disabled')
            self.event_generate('<<MainDone>>')
            return


    ################################
    # Store correct response words #
    ################################
    def _score(self):
        """ Get words marked correct and incorrect, update 
            scoremodel, and send event to controller.
        """
        # Don't try scoring on first click (start)
        #if self.counter != 0:
            # Get correct words
        correct = []
        for idx, value in enumerate(self.chk_vars):
            if value.get() != 0:
                #print(f" Correct: {self.words[idx]}")
                correct.append(self.words[idx])

        # Get incorrect words
        # Exclude correct words from list of words
        incorrect = list(set(self.words).difference(correct))
        # Only take capitalized words
        incorrect = [word for word in incorrect if word.isupper()]
        # Remove 'A' if it exists
        try:
            incorrect.remove('A')
        except ValueError:
            # There was no 'A' in the list
            pass

        # Update scoremodel with values
        self.scoremodel.fields['Words Correct'] = ' '.join(correct)
        self.scoremodel.fields['Num Words Correct'] = len(self.scoremodel.fields['Words Correct'].split())
        self.scoremodel.fields['Words Incorrect'] = ' '.join(incorrect)
        self.scoremodel.fields['Trial'] = self.counter + 1
        self.scoremodel.fields['Outcome'] = self.outcome

        # Send event to controller to write response to file
        self.event_generate('<<SubmitResponse>>')


    #####################################
    # Reset all labels and checkbuttons #
    #####################################
    def _reset(self):
        """ Reset all word labels and checkbuttons to default 
            values for next trial.
        """
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
