import pandas as pd

class test():
    def __init__(self):
        pass
        
    def download_all_docs(self):
        try: 
            df = pd.read_csv('user_database.csv').set_index('username')
            df['password'] = df['password'].astype(str)
            users_dict = df.to_dict(orient='index')
            self.user_data = df
        except FileNotFoundError:
            users_dict = {'username':['admin'],'password':['111'],'role':['admin'],'activated':['TRUE']}
            df = pd.DataFrame(users_dict)
            df.set_index('username', inplace=True)
            df['password'] = df['password'].astype(str)
            df.to_csv('user_database.csv')
            users_dict = df.to_dict(orient='index')
            self.user_data = df
        except:
            print("System couldn't read your user database file.")
        pass

        try:
            df = pd.read_csv('VolounteersData.csv').set_index('Username')
            #df['First name '] = df['First name '].astype(str)
            vol_dict = df.to_dict(orient='index')
            self.vol_data = df
        except FileNotFoundError:
            vol_dict = {'Username':[''],'First name':[''],'Second name':[''],'Camp ID':[''],'Avability':[''],'Status':['']}
            df = pd.DataFrame(vol_dict)
            df.set_index('Username', inplace=True)
            df.to_csv('VolounteersData.csv')
            self.vol_data = df
        except:
            print("System couldn't read your volunteer database file.")
        pass

        try:
            df = pd.read_csv('RefugeeList.csv')
            list_of_refugee = df.to_dict(orient='index')
            self.list_of_refugee = df

        except FileNotFoundError:
            list_of_refugee = {'Family ID':[''],'Lead Family Member Name':[''],'Lead Family Member Surname':[''],'Camp ID':[''],'Mental State':[''],'Physical State':[''],'No. Of Family Members':['']}
            df = pd.DataFrame(list_of_refugee)
            df.set_index('Family ID', inplace=True)
            df.to_csv('RefugeeList.csv')
            list_of_refugee = df.to_dict(orient='index')
            self.list_of_refugee = df
        try:
            df = pd.read_csv('camplist.csv')
            self.list_of_camps = df

        except FileNotFoundError:
            list_of_camps = {'Emergency ID':[''],'Type of emergency':[''],'Description':[''],'Location':[''],'Start date':[''],'Close date':[''],'Number of refugees':[''],'Camp ID':[''],'No Of Volounteers':[''],'Capacity':['']}
            df = pd.DataFrame(list_of_camps)
            df.set_index('Emergency ID', inplace=True)
            df.to_csv('camplist.csv')
            list_of_camps = df.to_dict(orient='index')
            self.list_of_camps = df

        try:
            #read camp summary information
            camps_df = pd.read_csv("camp_database.csv", index_col = 'Camp ID')
            #read list of existing camps
            camps_exist = list(camps_df.index)
        except FileNotFoundError:
            print('System could not read your camp database file.')
        except:
            print('An error occured.')
        

if __name__ == '__main__':
    
    a = test()
    a.users_login()