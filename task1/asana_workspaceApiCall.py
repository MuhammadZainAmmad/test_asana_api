import requests
import json           
import pandas as pd 

def asanaResToCSV(csvName, res):
    '''
        csvName: name of csv file in which data to dump
        res: response of the asana api
    '''
    resDict = json.loads(res.text) # String to dict
    df = pd.DataFrame.from_dict(resDict['data'])
    df.to_csv(csvName + '.csv')

headers = {
    "accept": "application/json",
    "authorization": "Bearer 1/1204862582358995:58225b495568b45ac37d588db2fea9a6"
}

workspace = "https://app.asana.com/api/1.0/workspaces"
resWorkspace = requests.get(workspace, headers=headers)
print(resWorkspace.text) # type ==> 'dict' 
asanaResToCSV('workspace', resWorkspace)

projects = "https://app.asana.com/api/1.0/projects"
resProjects = requests.get(projects, headers=headers)
print((resProjects.text)) # type ==> 'dict' 
asanaResToCSV('projects', resProjects)

# Getting the project ID
resProjectsDict = json.loads(resProjects.text)
projectID = resProjectsDict['data'][0]['gid']
# print(projectID)

section = f'https://app.asana.com/api/1.0/projects/{projectID}/sections'
resSection = requests.get(section, headers=headers)
print((resSection.text)) # type ==> 'dict' 
asanaResToCSV('section', resSection)

tasks = f"https://app.asana.com/api/1.0/tasks?project={projectID}"
resTasks = requests.get(tasks, headers=headers)
print((resTasks.text)) # type ==> 'dict' 
asanaResToCSV('tasks', resTasks)
