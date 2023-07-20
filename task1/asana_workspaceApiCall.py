import requests
import json           
import pandas as pd 
import os

from datetime import datetime
import urllib.parse

def asanaResToCSV(csvName, res):
    '''
        csvName: name of csv file in which data to dump
        res: response of the asana api
    '''
    resDict = json.loads(res.text) # String to dict
    df = pd.DataFrame.from_dict(resDict['data'])
    if not os.path.exists('./fetchedRecords'):
        os.makedirs('./fetchedRecords')
    df.to_csv(f'./fetchedRecords/{csvName}.csv', index= False)

headers = {
    "accept": "application/json",
    "authorization": "Bearer 1/1204862582358995:58225b495568b45ac37d588db2fea9a6"
}

# workspace = "https://app.asana.com/api/1.0/workspaces"
# resWorkspace = requests.get(workspace, headers=headers)
# # print(resWorkspace.text) # type ==> 'dict' 
# asanaResToCSV('workspace', resWorkspace)

projects = "https://app.asana.com/api/1.0/projects"
resProjects = requests.get(projects, headers=headers)
# print((resProjects.text)) # type ==> 'dict' 
asanaResToCSV('projects', resProjects)

# Getting the project ID
resProjectsDict = json.loads(resProjects.text)
projectID = resProjectsDict['data'][0]['gid']
# print(projectID)

# section = f'https://app.asana.com/api/1.0/projects/{projectID}/sections'
# resSection = requests.get(section, headers=headers)
# # print((resSection.text)) # type ==> 'dict' 
# asanaResToCSV('section', resSection)

# ========================================= fetching tasks ===========================================

# tasks = f"https://app.asana.com/api/1.0/tasks?project={projectID}"
# resTasks = requests.get(tasks, headers=headers)
# # print((resTasks.text)) # type ==> 'dict' 
# asanaResToCSV('tasks', resTasks)

current_datetime = datetime.utcnow().isoformat()
encoded_datetime = urllib.parse.quote(current_datetime)
if not os.path.exists('./fetchedRecords/tasks.csv'): # Logic for the first run of etl
    tasks = f"https://app.asana.com/api/1.0/tasks?project={projectID}"
    resTasks = requests.get(tasks, headers=headers) 
    resDict = json.loads(resTasks.text) # String to dict
    df = pd.DataFrame.from_dict(resDict['data'])
    
    # Adding date_created and date_modified columns in fetched df
    df['date_created'] = encoded_datetime
    df['date_modified'] = encoded_datetime
    
    if not os.path.exists('./fetchedRecords'):
        os.makedirs('./fetchedRecords')    
    df.to_csv(f'./fetchedRecords/tasks.csv', index=False)
    print('file created')
else:
    # using previous etl result
    df_tasks = pd.read_csv('./fetchedRecords/tasks.csv')
    print(f'Previous df\n{df_tasks}\n')
    
    last_modified = df_tasks['date_modified'].max()
    
    tasks = f"https://app.asana.com/api/1.0/tasks?project={projectID}&modified_since={last_modified}"
    resTasks = requests.get(tasks, headers=headers) 
    resDict = json.loads(resTasks.text) # String to dict
    df_modifiedTasks = pd.DataFrame.from_dict(resDict['data'])
    print(f'fetched df\n{df_modifiedTasks}\n')
      
    df_tasks['gid'] = df_tasks['gid'].astype(str)
    
    # Adding date_created and date_modified columns in fetched df
    df_modifiedTasks['date_modified'] = encoded_datetime
    df_modifiedTasks = df_modifiedTasks.merge(df_tasks[['gid', 'date_created']], on='gid', how='left')
    df_modifiedTasks['date_created'].fillna(encoded_datetime, inplace=True)
    print(f'processed fetched df\n{df_modifiedTasks}\n')
    
    # merging the two dfs
    df_merged = pd.concat([df_tasks, df_modifiedTasks]).drop_duplicates(subset='gid', keep='last')
    print(f'final df\n{df_merged}\n')
    
    if not os.path.exists('./fetchedRecords'):
        os.makedirs('./fetchedRecords')        
    df_merged.to_csv(f'./fetchedRecords/tasks_modified.csv', index=False)
    print('modified file created')

# resTasksDict = json.loads(resTasks.text)
# tasksList = resTasksDict['data']
# # print(tasksList)

# def taskDetailsToCSV(name, id):
#     task = f"https://app.asana.com/api/1.0/tasks/{id}"
#     resTask = requests.get(task, headers=headers)
#     # print((resTask.text)) # type ==> 'dict' 
#     resDict = json.loads(resTask.text) # String to dict
#     df = pd.json_normalize(resDict['data'], max_level=1)
#     if not os.path.exists('./fetchedRecords/taskDetails'):
#         os.makedirs('./fetchedRecords/taskDetails')
#     df.to_csv(f'./fetchedRecords/taskDetails/{name}.csv', index = False)

# # Checking the id of each task in the multiple tasks response by asana
# count = 0
# for task in tasksList:
#     # print(task['gid'])
#     taskDetailsToCSV(f'task{count}', task['gid'])
#     count += 1

# Understanding the task response
# resTaskDict = json.loads(resTasks.text)
# for item in resTaskDict['data'].keys():
#     print(item)
#     print(resTaskDict['data'][item], end='\n\n')