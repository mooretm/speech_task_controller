""" Model to write data to .csv
"""

############
# IMPORTS  #
############
# Import system packages
import csv
from pathlib import Path
from datetime import datetime
import os


#########
# MODEL #
#########
class CSVModel:
    """ Write provided dictionary to .csv
    """
    def __init__(self, sessionpars):
        self.sessionpars = sessionpars

        # Generate date stamp
        self.datestamp = datetime.now().strftime("%Y_%b_%d_%H%M")

    # # Data dictionary
    # fields = {
    #     "Audio Filename": {'req': True}
    #     }

    
    def save_record(self, data):
        """ Save a dictionary of data to .csv file 
        """
        # Create file name and path
        filename = f"{self.datestamp}_{self.sessionpars['Condition'].get()}_{self.sessionpars['Subject'].get()}.csv"
        self.file = Path(filename)

        # Check for write access to store csv
        file_exists = os.access(self.file, os.F_OK)
        parent_writable = os.access(self.file.parent, os.W_OK)
        file_writable = os.access(self.file, os.W_OK)
        if (
            (not file_exists and not parent_writable) or
            (file_exists and not file_writable)
        ):
            msg = f"Permission denied accessing file: {filename}"
            raise PermissionError(msg)

        # # Combine rating data and session parameters
        # # 1. Create temp sessionpars dict to avoid changing runtime vals
        # # 2. Get actual sessionpars values (not tk controls)
        # temp_sessionpars = dict()
        # for key in self.sessionpars:
        #     temp_sessionpars[key] = self.sessionpars[key].get()

        # # Add rating data to the end of the sessionpars dict
        # temp_sessionpars.update(data)

        # # Reformat dict keys for easy import
        # keys = temp_sessionpars.keys()
        # # Make all lowercase and replace spaces with underscores
        # keys_formatted = [x.lower().replace(' ', '_') for x in keys]

        # # Make a new dictionary with the formatted keys
        # all_data = dict()
        # for idx, key in enumerate(keys):
        #     all_data[keys_formatted[idx]] = temp_sessionpars[key]

        # # Fields to remove from dictionary before saving it
        # all_data.pop('audio_files_path') # Don't care about directory
        # all_data.pop('button_id') # Don't care about last button pressed

        # # Create new field for trailing underscore naming
        # # See naming convention info above
        # # Take everything after the last underscore
        # filename_val = all_data["audio_filename"].split("_")[-1]
        # # Remove .wav file extension
        # filename_val = filename_val[:-4]
        # all_data["filename_value"] = filename_val

        # # Save combined dict to file
        # newfile = not self.file.exists()
        # with open(self.file, 'a', newline='') as fh:
        #     csvwriter = csv.DictWriter(fh, fieldnames=all_data.keys())
        #     if newfile:
        #         csvwriter.writeheader()
        #     csvwriter.writerow(all_data)

        newfile = not self.file.exists()
        with open(self.file, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)
        print("Record successfully saved!")
