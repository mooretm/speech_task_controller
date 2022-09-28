""" Model for storing session parameters 
"""

############
# IMPORTS  #
############
# Import system packages
import csv
from pathlib import Path
from datetime import datetime
import os

# Import data science packages
import numpy as np
import pandas as pd

# Import data handling packages
import json
from glob import glob


#########
# MODEL #
#########
class SessionParsModel:
    # Define dictionary items
    fields = {
        'Subject': {'type': 'str', 'value': '999'},
        'Condition': {'type': 'str', 'value': 'Quiet'},
        'Presentation Level': {'type': 'float', 'value': 65},
        'Speaker Number': {'type': 'int', 'value': 1},
        'Audio Files Path': {'type': 'str', 'value': 'Please select a path'},
        'Audio Device ID': {'type': 'int', 'value': 999},
        'Raw Level': {'type': 'float', 'value': -50},
        'SLM Reading': {'type': 'float', 'value': 70},
        'Adjusted Presentation Level': {'type': 'float', 'value': -50}
    }

    def __init__(self):
        # Create session parameters file
        filename = 'speech_task_pars.json'

        # Store settings file in user's home directory
        self.filepath = Path.home() / filename

        # Load settings file
        self.load()


    def load(self):
        """ Load session parameters from file
        """
        # If the file doesn't exist, abort
        print("Models_Session_53: Checking for parameter file...")
        if not self.filepath.exists():
            return

        # Open the file and read in the raw values
        print("Models_Session_59: File found - reading raw values from " +
            "parameter file...")
        with open(self.filepath, 'r') as fh:
            raw_values = json.load(fh)

        # Don't implicitly trust the raw values: only get known keys
        print("Models_Session_65: Loading vals into sessionpars model " +
            "if they match model keys")
        # Populate session parameter dictionary
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value


    def save(self):
        """ Save current session parameters to file 
        """
        # Write to JSON file
        print("Models_Session_78: Writing session pars from model to file...")
        with open(self.filepath, 'w') as fh:
            json.dump(self.fields, fh)


    def set(self, key, value):
        """ Set a variable value """
        print("Models_Session_85: Setting sessionpars model " +
            "fields with running vals...")
        if (
            key in self.fields and 
            type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")
