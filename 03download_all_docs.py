import pandas as pd

class test():
    def __init__(self):
        self.user_data = None
        self.vol_data = None
        self.list_of_refugee = None
        self.list_of_camps = None
        self.camps_df = None
        pass
        
    def download_all_docs(self):

        try: 
            df = pd.read_csv('user_database.csv').set_index('username')
            df['password'] = df['password'].astype(str)
            #users_dict = df.to_dict(orient='index')
            self.user_data = df
        except FileNotFoundError:
            users_dict = {'username':['admin'],'password':['111'],'role':['admin'],'activated':['TRUE']}
            df = pd.DataFrame(users_dict)
            df.set_index('username', inplace=True)
            df['password'] = df['password'].astype(str)
            df.to_csv('user_database.csv')
            #users_dict = df.to_dict(orient='index')
            self.user_data = df
        except:
            print("System couldn't read your user database file.")

        try:
            df = pd.read_csv('VolounteersData.csv').set_index('Username')
            #vol_dict = df.to_dict(orient='index')
            self.vol_data = df
        except FileNotFoundError:
            vol_dict = {'Username':[''],'First name':[''],'Second name':[''],'Camp ID':[''],'Avability':[''],'Status':['']}
            df = pd.DataFrame(vol_dict)
            df.set_index('Username', inplace=True)
            df.to_csv('VolounteersData.csv')
            self.vol_data = df
        except:
            print("System couldn't read your volunteer database file.")

        try:
            df = pd.read_csv('RefugeeList.csv')
            #list_of_refugee = df.to_dict(orient='index')
            self.list_of_refugee = df
        except FileNotFoundError:
            list_of_refugee = {'Family ID':[''],'Lead Family Member Name':[''],'Lead Family Member Surname':[''],'Camp ID':[''],'Mental State':[''],'Physical State':[''],'No. Of Family Members':['']}
            df = pd.DataFrame(list_of_refugee)
            df.set_index('Family ID', inplace=True)
            df.to_csv('RefugeeList.csv')
            #list_of_refugee = df.to_dict(orient='index')
            self.list_of_refugee = df
        except:
            print("System couldn't read your refugees database file.")

        try:
            df = pd.read_csv('camplist.csv')
            self.list_of_camps = df
        except FileNotFoundError:
            list_of_camps = {'Emergency ID':[''],'Type of emergency':[''],'Description':[''],'Location':[''],'Start date':[''],'Close date':[''],'Number of refugees':[''],'Camp ID':[''],'No Of Volounteers':[''],'Capacity':['']}
            df = pd.DataFrame(list_of_camps)
            df.set_index('Emergency ID', inplace=True)
            df.to_csv('camplist.csv')
            #list_of_camps = df.to_dict(orient='index')
            self.list_of_camps = df
        except:
            print("System couldn't read your camplist database file.")

        try:
            df = pd.read_csv("camp_database.csv", index_col = 'Camp ID')
            self.camps_df = df
            #camps_exist = list(self.camps_df.index)
        except FileNotFoundError:
            camps_df = {'Camp ID':[''],'Location':[''],'Number of volunteers':[''],'Capacity':[''],'Current Emergency':[''],'Number of refugees':['']}
            df = pd.DataFrame(camps_df)
            df.set_index('Camp ID', inplace=True)
            df.to_csv('camplist.csv')
            #camps_df = df.to_dict(orient='index')
            self.camps_df = df
        except:
            print("System couldn't read your camp database file.")
        
if __name__ == '__main__':
    
    a = test()
    a.download_all_docs()