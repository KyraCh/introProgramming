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

        self.current_user = None
        self.camp_of_user = None
        
        pass
    
    def download_all_data(self):
        
        dataFailure = False

        try: 
            df = pd.read_csv('user_database.csv').set_index('username')
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
            df = pd.read_csv('volunteer_database.csv').set_index('Username')
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
    
    def amend_camp_capacity(self):
        '''
        Allows user to change the capacity of one of the camps. Selection by camp ID.
        '''
        camp_db = self.camps_db.copy()
        print("Select which camp's capacity needs to be altered")
        print('Expected Inputs:\n'+
              '\t>Emergency ID\n')
        print('[B] to go back')
        print('[Q] to quit\n')
        print(camp_db)
        
        while True:
            while True:
                choose_camp = input("\nChoose camp for which you want to edit: ").upper()
                if choose_camp in list(camp_db['Camp ID']) or choose_camp == 'Q':
                    break
                else:
                    print('Please select a valid camp')
                    continue
            if choose_camp == 'Q':
                    break
                
            print(camp_db.loc[camp_db["Camp ID"] == choose_camp])
            
            while True:
                cap = input("\nState new capacity: ")
                if cap == 'B' or cap == 'Q':
                    break
                else:
                    try:
                        cap = int(cap)
                        if cap < int(camp_db.loc[camp_db['Camp ID'] == choose_camp]['Number of refugees']):
                            print('Your new capacity is lower than current number of refugees.')
                            continue
                        else:
                            break
                    except ValueError:
                        print('Your input needs to be an integer')
                        continue
            if cap == 'B':
                continue
            elif cap == 'Q':
                break
            
            camp_db.loc[camp_db['Camp ID'] == choose_camp,'Capacity'] = cap
            print(camp_db.loc[camp_db['Camp ID'] == choose_camp])
            
            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue
            
            if commit == 'y':
                self.camps_db = camp_db.copy()
                camp_db.to_csv('camp_database.csv', index=False)
                break
            else:
                continue
            
tst = test()
tst.amend_camp_capacity()