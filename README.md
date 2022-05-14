[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Versions

1.0 (Depreciated)
-Functionally complete but feature lacking with a .txt based database.

1.5 (Depreciated)
-Swapped the .txt database with proper SQL db.
-Implemented list function to view all patients.

1.6 (Depreciated)
- Added list functionality for when multiple patients have the same last name. 

2.0 (Current)
- Added comment functionality. 

This is a sample project that I have worked on that is able to take inputs for a new patient and store it in a SQL database then locate patients in the database to display their data. 

Future Updates in order of planned implementation: 
- SQL upgrade. ### finished ####
- Tests.
- ORM.
- Time stamped notes under patients file. #### finished 5/14 ####
- Ability to list all patients and select from a list. ### finished ###
- Edit existing patients.
- Improve search functionality by removing case sensitivity for names and allow spaces in names.



Known issues being worked on:
- Patients who have the same last name cannot be differentiated. ### fixed 5/9/21 ###
- Sex not being displayed correctly. ### fixed ###
- Name case sensitivity search errors.
- Two part names (eg: James Junior) will cause errors due to search functionality of the database.


Here is a demo of the project ver 1.0, new demo will be updated after more features are implemented.

![](https://github.com/Nakadie/python_projects/blob/main/Projects/Hospital%20tool/Demo.gif)
