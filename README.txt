########################
2022-10-31 Version 2.0.1
########################
Minor bug fixes:
  1. Last used level was reloaded as starting level
     when restarting app without using session 
     dialog (which assigns new_db_lvl according to 
     entered level.
  2. Directory browser dialog title now states the 
     type of path it wants (e.g., "Audio File 
     Directory").
  3. Removed messagebox on startup without a saved 
     parameters file. Instead, the sentence label
     provides instructions. 
  4. No longer have to restart when stimulus paths
     and/or audio id weren't given before clicking
     START button.


########################
2022-10-28 Version 2.0.0
########################
Complete refactoring of code to OOP. New logic for 
handling word display and scoring. More flexible 
calibration dialog. 


########################
2022-06-08 Version 1.1.1
########################
Bug fix. Corrected issue where presentation level 
changes lagged behind the user-indicated level while 
in adaptive mode. 


########################
2022-06-07 Version 1.1.0
########################
Major feature addition. Added "audiometer-like" controls 
that allow for increasing/decreasing level on a per trial 
basis. Essentially provides manual adaptive functionality. 


########################
2022-06-06 Version 1.0.0
########################
Initial release. A GUI-based speech presentation controller. 
Ability to run the task at a specified level. 
