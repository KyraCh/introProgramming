import pandas as pd

def users0(self):
    try:
        pd.read_csv('user_database.csv')
    except FileNotFoundError:
        new = {'username':['admin'],'password':['111'],'role':['admin'],'activated':['TRUE']}
        df = pd.DataFrame(new)
        df.set_index('username', inplace=True)
        df.to_csv('user_database.csv')
    else:
        print("System couldn'd read your user data base file. Please ensure everything is fine")
    pass

def users():
    try:
        pd.read_csv('user_database.csv')
    except FileNotFoundError:
        new = {'username':['admin'],'password':['111'],'role':['admin'],'activated':['TRUE']}
        df = pd.DataFrame(new)
        df.set_index('username', inplace=True)
        df.to_csv('user_database.csv')
    else:
        print("System couldn'd read your user data base file. Please ensure everything is fine")
    pass