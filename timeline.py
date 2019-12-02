import pandas as pd 
import datetime

today = datetime.date.today()

# Initialize notebook.
notebook = pd.DataFrame({'When' : [str(today)], 'What Happened' : ['Started Notebook'], 'Tags' : ["-"]})

# Can set index = to date by appending `index=[str(today)]`; but I don't think it gets treated as a datetime if you do. 

add = pd.DataFrame({'When' : [str(today)], 'What Happened' : ['Started Notebook'], 'Tags' : ["-"]})

notebook = notebook.append(add)

notebook.to_csv('pd_timeline.csv')

# Still to do: 
# - Set up import of the existing csv, etc.
# - Make callable from BASH
# - Set up as part of shut-down script - https://ccm.net/faq/3348-execute-a-script-at-startup-and-shutdown-on-ubuntu