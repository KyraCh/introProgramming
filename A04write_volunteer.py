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

        self.current_user = 'Volunteer1'
        self.camp_of_user = 'AU1'
        self.functions = 10
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
    
    def count_ref_vol(self):  # what is the purpose of this method?
        '''
        Counts the number of volunteers in each camp and the number of refugees in each camp, after which it updates the camp_database.csv with correct numbers.
        '''
        camp_df = self.camps_db.copy()
        refugee_df = self.refugee_db.copy()
        vol_df = self.vol_db.copy()

        count_vol = vol_df['Camp ID'].value_counts()
        count_ref = refugee_df['Camp ID'].value_counts()

        for i in count_vol.index:
            camp_df.loc[camp_df['Camp ID'] == i,
                        'Number of volunteers'] = count_vol[i]
        for i in count_ref.index:
            camp_df.loc[camp_df['Camp ID'] == i,
                        'Number of refugees'] = count_ref[i]

        self.camps_df = camp_df.copy()
        camp_df.to_csv('camp_database.csv', index=False)

    def write_volunteer(self):
        '''
        Allows admin to create one or more empty volunteer accounts.

        Either manual input can be selected. 
            INPUTS: username, password and camp of volunteer
        Or automatic creation of multiple volunteer accounts from the same camp can be made which have automatically generated usernames in form "Volunteer"+index
            INPUTS: number of volunteers desired, camp of volunteers
        '''
        vol_df = self.vol_db.copy()
        users_df = self.user_db.copy()
        camps_df = self.camps_db.copy()
        users_exist = list(users_df['username'])
        camps_exist = list(camps_df['Camp ID'])
        self.quit = False
        print(100*'=')
        print('Please select how would you like to create a new volunteer profile')
        print('[1] - manual input')
        print('[2] - automatic creation')
        print('[B] to go back')
        print('[Q] to quit')

        def manual():
            counter = 0
            while True:

                def assign_username():
                    global username
                    while True:
                        inpt = input('\nEnter a new username: ')
                        if inpt in users_exist:
                            print('Username taken. Try another.')
                            continue
                        break
                    username = inpt
                    if inpt == 'Q' or inpt == 'B':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    return 1

                def assign_password():
                    global password
                    inpt = input('\nSet a password: ')
                    password = inpt
                    if inpt == 'B':
                        return -1
                    elif inpt == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    else:
                        return 1

                def assign_camp():
                    global camp
                    while True:
                        print('\nSet camp:')
                        print('[1] - View camp summary information')
                        print('[2] - Assign camp')
                        print('[B] to go back')
                        print('[Q] to quit')
                        user_input = input('\nChoose interaction: ')
                        if user_input == '1':
                            print(camps_df)
                        elif user_input == '2':
                            pass
                        elif user_input == 'B' or user_input == 'Q':
                            break
                        else:
                            print('Invalid input.')
                            continue
                        user_input = input('\nEnter camp ID: ')
                        while user_input not in camps_exist:
                            print('Invalid Camp ID.')
                            user_input = input('\nEnter camp ID: ')
                        camp = user_input
                        break

                    if user_input == 'B':
                        return -1
                    elif user_input == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    else:
                        return 1

                inputs = [assign_username, assign_password, assign_camp]

                while counter < len(inputs):
                    counter += inputs[counter]()

                vol_df.loc[len(vol_df.index)] = [
                    username, '', '', '', camp, '']
                users_df.loc[len(users_df.index)] = [
                    username, password, 'volunteer', 'TRUE', '']
                print(users_df.tail(1))
                while True:
                    commit = input('\nCommit changes? [y]/[n] ')
                    if commit == 'y' or commit == 'n':
                        break
                    else:
                        print('Your input is not recognised')
                        continue

                if commit == 'y':
                    self.vol_db = vol_df.copy()
                    self.user_db = users_df.copy()
                    vol_df.to_csv('volunteer_database.csv', index=False)
                    users_df.to_csv('user_database.csv', index=False)
                else:
                    counter = 0
                    continue

                while True:
                    repeat = input(
                        '\nWould you like to create another volunteer? [y]/[n] ')
                    if repeat == 'y' or repeat == 'n':
                        break
                    else:
                        print('Your input is not recognised')
                        continue
                if repeat == 'n':
                    break
                else:
                    counter = 0
                    continue

        def automatic():
            while True:
                while True:
                    no_of_new_users = input(
                        '\nPlease select the number of new volunteers you wish to create: ')
                    try:
                        no_of_new_users = int(no_of_new_users)
                        if no_of_new_users == 'Q':
                            print(100*'=')
                            menu(self.functions)
                            exit()
                    except ValueError:
                        print('Your input needs to be an integer')
                        continue
                    while True:
                        camp = input('\nEnter camp ID: ')
                        if camp not in camps_exist:
                            print('Invalid Camp ID.')
                            continue
                        else:
                            break
                    if camp == 'B':
                        continue
                    elif no_of_new_users == 'Q':
                        menu(self.functions)
                        exit()
                    else:
                        break

                new_usr_index = len(vol_df.index)+1
                for i in range(no_of_new_users):
                    vol_df.loc[len(vol_df.index)] = [
                        'Volunteer'+str(new_usr_index+i), '', '', '', camp, '']
                    users_df.loc[len(users_df.index)] = [
                        'Volunteer'+str(new_usr_index+i), '111', 'volunteer', 'TRUE', '']

                print(users_df.tail(no_of_new_users))
                while True:
                    commit = input('\nCommit changes? [y]/[n] ')
                    if commit == 'y' or commit == 'n':
                        break
                    else:
                        print('Your input is not recognised')
                        continue

                if commit == 'y':
                    self.vol_db = vol_df.copy()
                    self.user_db = users_df.copy()
                    vol_df.to_csv('volunteer_database.csv', index=False)
                    users_df.to_csv('user_database.csv', index=False)
                    break
                else:
                    continue

        while True:
            user_input = input('Choose interaction: ')
            if user_input == '1' or user_input == '2':
                break
            else:
                print('You input is not recognised')
                continue

        if user_input == '1':
            manual()
        else:
            automatic()
        print(100*'=')

def menu(a):
    print('You in menu')
    
tst = test()
tst.write_volunteer()
tst.count_ref_vol()
print(tst.vol_db)
print(tst.camps_db)