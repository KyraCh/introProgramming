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
    
    def write_camp(self,prev=None):
        '''
        Allows admin to add a news camp to an existing emergency.
        '''
        self.quit = False
        counter = 0
        self.count_ref_vol()
        print('Please provide details of the new camp')
        print('Expected Inputs:\n'+
              '\t>Country\n'+
              '\t>Emergency ID\n'+
              '\t>Camp capacity\n')
        print('[B] to go back')
        print('[Q] to quit')

        while True:
            
            camps_df = self.camps_db.copy()
            emergency_df = self.emergencies_db.copy()
            countries = self.countries_db.to_dict(orient='index')

            def assign_country():
                global country_id
                global country
                while True:
                    country = input("\nEnter country name: ")
                    if country == 'B' or country == 'Q':
                        break
                    if country in countries.keys(): #and country_id in list(emergency_df['Emergency ID']):
                        country_id = countries[country]['Country code']
                        if True in list(emergency_df['Emergency ID'].str.contains('PK', case=False)):
                            break
                    print('Please select country with an existing emergency.')
                if country == 'Q':
                    self.quit = True
                return 1
            
            def assign_emergency():
                global emergency
                emergencies_in_country = emergency_df.loc[emergency_df['Emergency ID'].str.contains(country_id, case=False)]
                if len(emergencies_in_country.index) >= 1:
                    print('\n',emergencies_in_country)
                while True:
                    if len(emergencies_in_country.index) > 1:
                        emergency = input('\nPlease select which emergency you would like to assign your camp to: ')
                        if emergency == 'B' or emergency == 'Q':
                            break
                        if emergency in list(emergencies_in_country['Emergency ID']):
                            break
                        else:
                            print('Please select valid ID.')
                            continue
                    else:
                        emergency = list(emergencies_in_country['Emergency ID'])[0]
                        break
                if emergency == 'B':
                    return -1
                elif emergency == 'Q':
                    self.quit = True
                    return 0
                else:
                    return 1

            def assign_capacity():
                global capacity
                while True:
                    capacity = input("\nEnter maximum camp capacity:")
                    if capacity == 'B' or emergency == 'Q':
                        break
                    if capacity.isdigit()==False:
                        print('Please enter an integer.')
                        continue
                    break
                if capacity == 'B':
                    return -1
                elif capacity == 'Q':
                    self.quit = True
                    return 0
                else:
                    return 1
                
            inputs = [assign_country, assign_emergency, assign_capacity]
                
            while counter < len(inputs):
                counter += inputs[counter]()
                if self.quit == True:
                    break
            if self.quit == True:
                    break

            new_camp_index = len(camps_df.loc[camps_df['Camp ID'].str.contains(emergency, case=False)].index)+1
            new_ID = emergency + '-' + str(new_camp_index)

            camps_df.loc[len(camps_df.index)] = [new_ID, country, '', capacity, emergency, '']

            print(camps_df.tail(1))
            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue
            
            if commit == 'y':
                self.camps_df = camps_df.copy()
                camps_df.to_csv('camp_database.csv', index=False)
                break
            else:
                continue
           
tst = test()
tst.write_camp()