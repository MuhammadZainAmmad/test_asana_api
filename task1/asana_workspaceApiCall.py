import requests
import json           
import pandas as pd 


# url = "https://app.asana.com/api/1.0/projects"
# url = "https://app.asana.com/api/1.0/tasks"

def asanaResToCSV(csvName, res):
    '''
        csvName: name of csv file in which data to dump
        res: response of the asana api
    '''
    resDict = json.loads(res.text) # String to dict
    print(resDict)
    df = pd.DataFrame.from_dict(resDict['data'])
    df.to_csv(csvName + '.csv')

headers = {
    "accept": "application/json",
    "authorization": "Bearer 1/1204862582358995:58225b495568b45ac37d588db2fea9a6"
}

workspace = "https://app.asana.com/api/1.0/workspaces"
resWorkspace = requests.get(workspace, headers=headers)
# print(type(resWorkspace.text)) # type ==> 'dict' 
asanaResToCSV('workspace', resWorkspace)


# projects = "https://app.asana.com/api/1.0/projects"
# resProjects = requests.get(workspace, headers=headers)
# print((resProjects.text)) # type ==> 'dict' 