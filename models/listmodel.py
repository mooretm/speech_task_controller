""" Class for storing list of audio files.
"""

###########
# Imports #
###########
# Import GUI packages
from tkinter import messagebox

# Import data science packages
import pandas as pd

# Import system packages
import os
from glob import glob


#########
# BEGIN #
#########
class StimulusList:
    """ Get audio files and trailing underscore values 
    """

    def __init__(self, sessionpars):
        # Initialize
        self.sessionpars = sessionpars

        # Call functions in order
        self._get_list_nums()
        self._get_sentences()
        self._get_audio_files()


    def _get_list_nums(self):
        # Get list numbers as integers
        self.lists = self.sessionpars['List Number'].get().split()
        self.lists = [int(val) for val in self.lists]


    def _get_audio_files(self):
        ###############
        # Audio Files #
        ###############
        # Check whether audio directory exists
        print("Models_listmodel_33: Checking for audio files dir...")
        if not os.path.exists(self.sessionpars['Audio Files Path'].get()):
            print("Models_listmodel_35: Not a valid audio files directory!")
            messagebox.showerror(
                title='Directory Not Found!',
                message="Cannot find the audio file directory!\n" +
                "Please choose another file path."
            )
        # If a valid directory has been given, 
        # get the audio file paths and names
        glob_pattern = os.path.join(self.sessionpars['Audio Files Path'].get(), '*.wav')
        # Create audio paths dataframe
        self.audio_df = pd.DataFrame(glob(glob_pattern), columns=['path'])
        self.audio_df['file_num'] = self.audio_df['path'].apply(lambda x: x.split(os.sep)[-1][:-4])
        self.audio_df['file_num'] = self.audio_df['file_num'].astype(int)
        self.audio_df = self.audio_df.sort_values(by=['file_num'])
        self.audio_df = self.audio_df.loc[self.audio_df['file_num'].isin(self.sentence_df['sentence_num'])].reset_index()
        print(self.audio_df)
        print("Models_list_model_47: Audio list dataframe loaded into listmodel")


    def _get_sentences(self):
        ##################
        # Sentence Files #
        ##################
        # Check whether sentence directory exists
        print("Models_listmodel_54: Checking for sentences dir...")
        if not os.path.exists(self.sessionpars['Sentence File Path'].get()):
            print("Models_listmodel_56: Not a valid 'sentences' file directory!")
            messagebox.showerror(
                title='Directory Not Found!',
                message="Cannot find the 'sentence' file directory!\n" + 
                "Please choose another file path."
            )
        # If a valid directory has been given, 
        # get a list of sentence files
        glob_pattern = os.path.join(self.sessionpars['Sentence File Path'].get(), '*.csv')
        sentence_file = glob(glob_pattern)
        # Check to make sure there's only one file in the directory
        if len(sentence_file) > 1:
            messagebox.showwarning(
                title="Too Many Files!",
                message="Multiple sentence files found - taking the first one."
            )
        # Read sentence file into dataframe
        s = pd.read_csv(sentence_file[0])
        # Get sentences for specified list numbers
        self.sentence_df = s.loc[s['list_num'].isin(self.lists)].reset_index()
        print(self.sentence_df)
        print("Models_listmodel_80: Sentence list dataframe loaded into listmodel")
