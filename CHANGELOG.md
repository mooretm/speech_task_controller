#**Change Log**

---

## v2.0.1  

Date: 31 Oct, 2022 

### Minor Bug Fixes
1. Last used level was reloaded as starting level when restarting app without using session dialog (which assigns new_db_lvl according to entered level).
2. Directory browser dialog title now states the type of path it wants (e.g., "Audio File Directory").
3. Removed messagebox on startup without a saved parameters file. Instead, the sentence label provides instructions.
4. No longer have to restart when stimulus paths and/or audio id weren't given before clicking the START button.
<br>
<br>

---

## v2.0.0

Date: 28 Oct, 2022

### Major Changes
1. Complete refactoring of code to OOP. 
2. New logic for handling word display and scoring. 
3. More flexible calibration and session dialogs. 
<br>
<br>

---

## v1.1.1

Date: 08 Jun, 2022

### Minor Bug Fixes
1. Corrected issue where presentation level changes lagged behind the user-indicated level while in adaptive mode. 
<br>
<br>

---

## v1.1.0

Date: 07 Jun, 2022

### Major Feature Added
1. Added "audiometer-like" controls that allow for increasing/decreasing level on a per trial basis. Essentially provides manual adaptive functionality. 
<br>
<br>

---

## v1.0.0

Date: 06 Jun, 2022

### Initial Release
1. A GUI-based speech presentation controller with the ability to run the task at a specified presentation level. 
<br>
<br>
