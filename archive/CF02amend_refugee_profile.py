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

        self.current_user = 'admin'
        self.camp_of_user = 'admin'
        self.functions = 10
        
        pass
    
    
    def download_all_data(self):

        dataFailure = False

        try:
            df = pd.read_csv('user_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('', inplace=True)
            df['password'] = df['password'].astype(str)
            self.user_db = df
        except FileNotFoundError:
            user_db = {'username': ['admin'], 'password': [
                '111'], 'role': ['admin'], 'activated': ['TRUE'], 'email': ['hemtest11@gmail.com']}
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
            df.fillna('', inplace=True)
            self.vol_db = df
        except FileNotFoundError:
            vol_db = {'Username': [''], 'First name': [''], 'Second name': [
                ''], 'Camp ID': [''], 'Avability': [''], 'Status': ['']}
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
            df.fillna('', inplace=True)
            self.refugee_db = df
        except FileNotFoundError:
            refugee_db = {'Family ID': [''], 'Lead Family Member Name': [''], 'Lead Family Member Surname': [
                ''], 'Camp ID': [''], 'Mental State': [''], 'Physical State': [''], 'No. Of Family Members': ['']}
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
            df.fillna('', inplace=True)
            self.camps_db = df
        except FileNotFoundError:
            camps_db = {'Emergency ID': [''], 'Type of emergency': [''], 'Description': [''], 'Location': [''], 'Start date': [
                ''], 'Close date': [''], 'Number of refugees': [''], 'Camp ID': [''], 'No Of Volounteers': [''], 'Capacity': ['']}
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
            df.fillna('', inplace=True)
            self.emergencies_db = df
        except FileNotFoundError:
            emergencies_db = {'Emergency ID': [''], 'Location': [''], 'Type': [
                ''], 'Description': [''], 'Start date': [''], 'Close date': ['']}
            df = pd.DataFrame(emergencies_db)
            df.set_index('Emergency ID', inplace=True)
            df.to_csv('emergency_database.csv')
            self.emergencies_db = df
        except:
            print("System couldn't read your camplist database file.")
            dataFailure = True

        try:
            df = pd.read_csv("countries.csv", index_col='Country name')
            self.countries_db = df
        except:
            print("System couldn't read the countries database file.")
            dataFailure = True

        return dataFailure

    def amend_refugee_profile(self): # This is a mess. Must be redone - Fedor
        '''
        Interactive method which allows one to amend information about a refugee.
        ### TRY THE METHODS-IN-A-LIST TECHNIQUE. ###
        '''
        while True:
            list_of_refugees = self.refugee_db.copy()
            camps_df = self.camps_db.copy()
            print(100*'=')
            print('\nPlease select which refugee profile you would like to ammend\n')
            print('[B] to go back')
            print('[Q] to quit\n')
            
            if self.current_user == 'admin':
                print(list_of_refugees)
            else:
                print(list_of_refugees.loc[list_of_refugees['Camp ID']==self.camp_of_user])
                
            iD = input('\nPlease choose Family ID you would like to ammend: ')
            if iD.upper() == 'Q' or iD.upper() == 'B':
                print(100*'=')
                menu(self.functions)
                exit()
            if iD not in list(list_of_refugees['Family ID']):
                print('Please enter valid Family ID')
                continue

            while True:
                print(f'\nPlease Choose which values you would like to ammend for family {iD}.')
                print('Input indices corresponding to value you wish to ammend separated by commas ",".')
                print('eg: "1,2" for amending "Lead Family Member Name" and "Lead Family Member Surname".\n')
                print('[1] - "Lead Family Member Name"')
                print('[2] - "Lead Family Member Surname"')
                print('[3] - "Camp of Refugee"')
                print('[4] - "Mental State"')
                print('[5] - "Physical State"')
                print('[6] - "No. Of Family Members"\n')
                counter = 0
                while True:
                    inpt = input('Indices: ')
                    if inpt.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    elif inpt.upper() == 'B':
                        self.amend_refugee_profile()
                    try:
                        operations = [int(i) for i in inpt.split(',')]
                    except:
                        print('Please input valid indices\n')
                        continue
                    check = [not (i < 1 or i > 6) for i in operations]
                    if any(i is False for i in check):
                        print('Please input valid indices\n')
                        continue
                    break

                while counter < len(operations):
                    i = operations[counter]
                    if i == 3:
                        print('\n',camps_df)

                    change = input(f'\nPlease select new value for {list_of_refugees.columns[i]}: ')
                    
                    if change.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    elif change.upper() == 'B':
                        if counter == 0:
                            print('BUIG BRUH')
                            break
                        counter -= 1
                        continue
                    
                    if i == 3:
                        camps = []
                        for i in list(list_of_refugees['Family ID']):
                            for chr in i:
                                if chr.isalpha():
                                    temp = i.index(chr)
                                    camps.append(i[temp:])
                                    break
                        if change in camps:
                            index = []
                            for i in list(list_of_refugees.loc[list_of_refugees['Camp ID']==change]['Family ID']):
                                for chr in i:
                                    if chr.isalpha():
                                        temp = i.index(chr)
                                        index.append(i[:temp])
                                        break
                                new_index = str(int(max(index))+1)
                            
                            list_of_refugees.loc[list_of_refugees['Family ID'] == iD,'Family ID']  = new_index + change
                            iD = new_index + change
                            counter += 1
                            continue
                        else:
                            list_of_refugees.loc[list_of_refugees['Family ID'] == iD,'Family ID'] = '1' + change
                            iD = '1' + change
                            counter += 1
                            continue
                    counter += 1
                    list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0], list_of_refugees.columns[i]] = change
                if change.upper() == 'B':
                    continue
                break
            
            print('\n')
            print(list_of_refugees.loc[list_of_refugees['Family ID'] == iD])

            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue

            if commit == 'y':
                self.refugee_db = list_of_refugees.copy()
                list_of_refugees.to_csv('refugee_database.csv', index=False)
                break
            else:
                continue

def menu(a):
    print('THIS IS MENU')
    
tst = test()
tst.amend_refugee_profile()