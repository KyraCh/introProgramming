import pandas as pd
import datetime
import os

class test():
    
    def __init__(self):
        self.user_db = None
        self.vol_db = None
        self.refugee_db = None
        self.camps_db = None
        self.countries_db = None
        self.emergencies_db = None 

        fileCheckError =  self.download_all_data()
        
        if fileCheckError:
            exit()

        self.current_user = 'adm'
        self.camp_of_user = None
        
        pass
    
    def download_all_data(self):
        
        dataFailure = False

        try: 
            df = pd.read_csv('user_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
            df['password'] = df['password'].astype(str)
            self.user_db = df
        except FileNotFoundError:
            user_db = {'username':['admin'],'password':['111'],'role':['admin'],'activated':['TRUE']}
            df = pd.DataFrame(user_db)
            df.set_index('username', inplace=True)
            df['password'] = df['password'].astype(str)
            df.to_csv('user_database.csv')
            self.user_db = df
        except:
            print("System couldn't read your user database file.")
            dataFailure = True 

        try:
            df = pd.read_csv('volunteer_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
            self.vol_db = df
        except FileNotFoundError:
            vol_db = {'Username':[''],'First name':[''],'Second name':[''],'Camp ID':[''],'Avability':[''],'Status':['']}
            df = pd.DataFrame(vol_db)
            df.set_index('Username', inplace=True)
            df.to_csv('volunteer_database.csv')
            self.vol_db = df
        except:
            print("System couldn't read your volunteer database file.")
            dataFailure = True

        try:
            df = pd.read_csv('refugee_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
            self.refugee_db = df
        except FileNotFoundError:
            refugee_db = {'Family ID':[''],'Lead Family Member Name':[''],'Lead Family Member Surname':[''],'Camp ID':[''],'Mental State':[''],'Physical State':[''],'No. Of Family Members':['']}
            df = pd.DataFrame(refugee_db)
            df.set_index('Family ID', inplace=True)
            df.to_csv('refugee_database.csv')
            self.refugee_db = df
        except:
            print("System couldn't read your refugees database file.")
            dataFailure = True

        try:
            df = pd.read_csv('camp_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
            self.camps_db = df
        except FileNotFoundError:
            camps_db = {'Emergency ID':[''],'Type of emergency':[''],'Description':[''],'Location':[''],'Start date':[''],'Close date':[''],'Number of refugees':[''],'Camp ID':[''],'No Of Volounteers':[''],'Capacity':['']}
            df = pd.DataFrame(camps_db)
            df.set_index('Emergency ID', inplace=True)
            df.to_csv('camp_database.csv')
            self.camps_db = df
        except:
            print("System couldn't read your camplist database file.")
            dataFailure = True

        try:
            df = pd.read_csv('emergency_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
            self.emergencies_db = df
        except FileNotFoundError:
            emergencies_db = {'Emergency ID':[''],'Location':[''],'Type':[''],'Description':[''],'Start date':[''],'Close date':['']}
            df = pd.DataFrame(emergencies_db)
            df.set_index('Emergency ID', inplace=True)
            df.to_csv('emergency_database.csv')
            self.emergencies_db = df
        except:
            print("System couldn't read your camplist database file.")
            dataFailure = True
        
        try:
            df = pd.read_csv("countries.csv", index_col = 'Country name')
            self.countries_db = df
        except:
            print("System couldn't read the countries database file.")
            dataFailure = True
        
        return dataFailure
    
    def count_ref_vol(self):
        camp_df = self.camps_db.copy()
        refugee_df = self.refugee_db.copy()
        vol_df = self.vol_db.copy()

        count_vol = vol_df['Camp ID'].value_counts()
        count_ref = refugee_df['Camp ID'].value_counts()

        for i in count_vol.index:
            camp_df.loc[camp_df['Camp ID']==i,'Number of volunteers'] = count_vol[i]
        for i in count_ref.index:
            camp_df.loc[camp_df['Camp ID']==i,'Number of refugees'] = count_ref[i]

        self.camps_df = camp_df.copy()
        camp_df.to_csv('camp_database.csv', index=False)
           
tst = test()
tst.count_ref_vol()