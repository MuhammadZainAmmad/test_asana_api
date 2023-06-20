import requests

workspace = "https://app.asana.com/api/1.0/workspaces"
# url = "https://app.asana.com/api/1.0/projects"
# url = "https://app.asana.com/api/1.0/tasks"

headers = {
    "accept": "application/json",
    "authorization": "Bearer 1/1204862582358995:58225b495568b45ac37d588db2fea9a6"
}

resWorkspace = requests.get(workspace, headers=headers)

# print(type(resWorkspace.text)) # type ==> 'dict' 

import json           
import pandas as pd 
resDict = json.loads(resWorkspace.text) # String to dict
df = pd.DataFrame.from_dict(resDict['data'])
df.to_csv('workspace.csv')
