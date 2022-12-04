import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import os


class CentralFunctions():

    def __init__(self):
        self.user_db = None
        self.vol_db = None
        self.refugee_db = None
        self.camps_db = None
        self.countries_db = None
        self.emergencies_db = None

        fileCheckError = self.download_all_data()

        if fileCheckError:
            exit()

        self.current_user = None
        self.camp_of_user = None

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
                '111'], 'role': ['admin'], 'activated': ['TRUE']}
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

    def save(self, dataFrame, fileName):
        try:
            dataFrame.to_csv(f"{fileName}", index=False)
            return True
        except PermissionError:
            return False

    def users_login(self):

        users_dict = self.user_db.copy().set_index('username').to_dict(orient='index')
        vol_dict = self.vol_db.copy().set_index('Username').to_dict(orient='index')

        while True:
            username = input('Please input your username: ').strip()
            password = input('Please input your password: ').strip()

            if username not in users_dict:
                print('Username is incorrect.')
            elif password != users_dict[username]['password']:
                print('Password is incorrect.')
            elif not users_dict[username]['activated']:
                print('Account not activated. Please contact your admin.')
            else:
                break

        self.current_user = username

        if username == 'admin':
            self.current_user = 'adm'
            self.camp_of_user = 'adm'
            print(f'Welcome Back admin\n')
        else:
            name = vol_dict[username]['First name']
            self.camp_of_user = vol_dict[username]['Camp ID']
            print(f'Welcome back {name}\n')

    def create_profile(self):
        '''
        Interactive method which allows to add new family to the list
        '''

        while True:
            name = input("State name of family's lead member: ")
            surname = input("State surname of the family: ")
            if not name.isalpha() or not surname.isalpha():
                print("You can't use numbers for this input. Try again ")
            else:
                break

        mental_state = input("Describe the mental state of the family: ")
        physical_state = input("Describe the physical state of the family: ")

        while True:
            try:
                no_of_members = int(
                    input("Type the number of family members: "))
                break
            except ValueError:
                print("It has to be an integer")
                continue

        campID = self.camp_of_user
        count_camps = self.refugee_db[self.refugee_db["Camp ID"]
                                      == self.camp_of_user]['Camp ID'].value_counts().values[0]
        family_id = str(count_camps + 1) + self.camp_of_user

        self.refugee_db.loc[len(self.refugee_db)] = [
            family_id, name, surname, self.camp_of_user, mental_state, physical_state, no_of_members]

        self.refugee_db.to_csv("refugee_db.csv", index=False)
        self.save(self.refugee_db, 'refugee_database.csv')

    def call_camps(self):
        # need to add 7,8,9
        print("Choose 1 if you want to see the list of all camps")
        print("Choose 2 if you want to see the total number of camps")
        print("Choose 3 if you want to see the number of volunteers in each camp")
        print("Choose 4 if you want to see the number of refugees in each camp")
        print("Choose 5 if you want to see the capacity by camp")
        print("Choose 6 if you want to see the number of camps in each area")
        print("Choose 7 if you want to see the number of active camps")
        print("Choose 8 if you want to see the number of inactive camps")
        print("Choose 9 if you want to see the number of camps by emergency type")
        print("Choose Quit if you want exit this summary")

        while True:

            user_input = input("Choose interaction: ")

            if user_input == '1':
                print("See camp list: \n", self.camps_db)
            elif user_input == "2":
                print("Number of camps: ", len(self.camps_db.index))
            elif user_input == "3":
                print("Number of volunteers per camp: \n",
                      self.vol_db.groupby(by=self.vol_db['Camp ID']).size())
            elif user_input == "4":
                print("Number of refugees per camp: \n",
                      self.refugee_db.groupby(by=self.refugee_db['Camp ID']).size())
            elif user_input == "5":
                print("Capacity by camp: \n", self.camps_db['Capacity'])
            elif user_input == "6":
                print("Camps in each area: \n", self.camps_db.groupby(
                    by=self.camps_db['Location']).size())
            else:
                break

    def amend_refugee_profile(self):
        '''
        Interactive method which allows one to amend information about a refugee.
        '''
        list_of_refugees = self.refugee_db.copy()

        print('AMEND REFUGEE PROFILE')
        print('-'*25)
        print("Type 'q' to quit the process at any moment (progress won't be saved)")

        while True:
            iD = input('\nPlease choose Family ID you would like to ammend: ')
            if iD == 'q':
                break
            if iD not in list(list_of_refugees['Family ID']):
                print('Please enter valid Family ID')
                continue
            if self.current_user == 'vol':
                if iD[-2:] != self.camp_of_user:
                    print('Please choose a refugee from your camp')
                    continue
            print('\n')
            print('-'*25)
            print(
                f'Please Choose which values you would like to ammend for family {iD}.')
            print(
                'Input indices corresponding to value you wish to ammend separated by commas ",".')
            print(
                'eg: "1,2" for amending "Lead Family Member Name" and "Lead Family Member Surname".\n')
            print('[1] - "Lead Family Member Name"')
            print('[2] - "Lead Family Member Surname"')
            print('[3] - "Camp ID"')
            print('[4] - "Mental State"')
            print('[5] - "Physical State"')
            print('[6] - "No. Of Family Members"\n')

            while True:
                ops = input('Indices: ')
                if ops == 'q':
                    break
                try:
                    ops = [int(i) for i in ops.split(',')]
                except:
                    print('Please input valid indices\n')
                    continue
                check = [not (i < 1 or i > 6) for i in ops]
                if any(i is False for i in check):
                    print('Please input valid indices\n')
                    continue
                break

            if ops == 'q':
                break

            for i in ops:
                change = input(
                    f'\nPlease select new value for {list_of_refugees.columns[i]}: ')
                if change == 'q':
                    list_of_refugees = self.refugee_db
                    break
                if i == 3:
                    if change in [i[1:] for i in list(list_of_refugees['Family ID'])]:
                        new_index = str(
                            max([int(i[0]) for i in list(list_of_refugees['Family ID']) if change in i])+1)
                        list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID']
                                                                   == iD][0], 'Family ID'] = new_index + change
                        iD = new_index + change
                    else:
                        list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID']
                                                                   == iD][0], 'Family ID'] = '1' + change
                        iD = '1' + change

                list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID']
                                                           == iD][0], list_of_refugees.columns[i]] = change

            if change == 'q':
                break

            print('\n')
            print(list_of_refugees.loc[list_of_refugees['Family ID'] == iD])

            if input('\nCommit changes? y/n ') == 'n':
                continue
            else:
                if not self.save(list_of_refugees, 'refugee_database.csv'):
                    print(
                        'The file is currently opened. Please close the file to save.')

                    # not convinced this is the most efficient way to go about this --> open to feedback
                    while not self.save(list_of_refugees, 'refugee_database.csv'):
                        pass
                print('Changes commited')

            self.refugee_db = list_of_refugees
            break

    def count_ref_vol(self):
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


class Admin(CentralFunctions):

    def __init__(self, current_user, camp_of_user):
        CentralFunctions.__init__(self,)
        self.functions = {"1": {'method': self.create_emergency,      'message': '[1] - Add new Emergency', },
                          "2": {'method': self.close_emergency,       'message': '[2] - Close Emergency', },
                          "3": {'method': self.call_camps,            'message': '[3] - See camp info', },
                          "4": {'method': self.write_camp,            'message': '[4] - Add new camp', },
                          "5": {'method': self.amend_camp_capacity,   'message': '[5] - Amend capacity of a camp', },
                          "6": {'method': self.write_volunteer,       'message': '[6] - Add new volunteer(s) profile(s)', },
                          "7": {'method': self.create_profile,        'message': '[7] - Create refugee profile', },
                          "8": {'method': self.amend_refugee_profile, 'message': '[8] - Amend refugee profile', }}
        self.current_user = current_user
        self.camp_of_user = camp_of_user

    def create_emergency(self):
        '''
        Allows user to create emergency by requesting country of emergencym type of emergency, description and start date.
        Automatically assigns emergency ID and upon commit adds new emergency to emergency_database.csv 
        '''
        print(100*'=')
        print('Please input information about your emergency')
        print('Expected Inputs:\n' +
              '\t>Country\n' +
              '\t>Type of emergency\n' +
              '\t>Description of your emrgency\n' +
              '\t>Start date\n')
        print('[B] to go back')
        print('[Q] to quit')

        while True:
            emergency_db = self.emergencies_db.copy()
            country_dict = self.countries_db.to_dict(orient='index')

            def go_back(questionStack):
                i = 0
                answerStack = []
                while i < len(questionStack):

                    if i == 0:
                        while True:
                            answer = input(questionStack[i])
                            if answer in list(self.countries_db.index):
                                break
                            else:
                                print('Please select valid country')
                                continue
                    elif i == 3:
                        while True:
                            answer = input(questionStack[i])
                            try:
                                datetime.date.fromisoformat(answer)
                                answer = datetime.datetime.strptime(
                                    answer, "%Y-%m-%d").strftime("%d/%m/%Y")
                                break
                            except:
                                print(
                                    'Please enter a day of valid format [YYYY-MM-DD]: ')
                                continue
                    else:
                        answer = input(questionStack[i])

                    if answer == 'B':
                        if i == 0:
                            print(100*'=')
                            menu(self.functions)
                            exit()
                        answerStack.pop()
                        i -= 1
                        continue
                    elif answer == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()

                    answerStack.append(answer)
                    i += 1

                return answerStack

            questions = ['\nPlease select the country of emergency: ', '\nPlease enter type of emergency: ', '\nPlease briefly describe your emergency: ',
                         '\nPlease enter start date of the emergency [YYYY-MM-DD]: ']
            answers = go_back(questions)
            country_code = country_dict[answers[0]]['Country code']

            if True in list(emergency_db['Emergency ID'].str.contains(country_code, case=False)):
                new_no_index = int(emergency_db.loc[emergency_db['Emergency ID'].str.contains(
                    country_code, case=False)].iloc[-1]['Emergency ID'][2:]) + 1
            else:
                new_no_index = 1
            emergency_id = country_code + str(new_no_index)

            emergency_db.loc[len(emergency_db.index)] = [
                emergency_id, answers[0], answers[1], answers[2], answers[3], None]

            print('\n', emergency_db.iloc[-1])
            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue

            if commit == 'y':
                self.emergencies_db = emergency_db.copy()
                emergency_db.to_csv('emergency_database.csv', index=False)
                break
            else:
                continue
        print(100*'=')

    def close_emergency(self):
        '''
        Closes emergency by adding current date to Close Date column.
        '''
        emergency_db = self.emergencies_db.copy()
        print(100*'=')
        while True:
            print('Please specify which emergency you would like to close')
            print('Expected Inputs:\n' +
                  '\t>Emergency ID\n')
            print('[B] to go back')
            print('[Q] to quit\n')
            print(emergency_db)

            while True:
                ID = input('\nPlease provide the emergency ID: ').upper()
                if ID in list(emergency_db['Emergency ID']):
                    break
                elif ID == 'Q' or ID == 'B':
                    print(100*'=')
                    menu(self.functions)
                    exit()
                else:
                    print('Please provide valid ID')
                    continue

            emergency_db.loc[emergency_db['Emergency ID'] == ID,
                             'Close date'] = datetime.date.today().strftime("%d/%m/%Y")
            print(emergency_db.loc[emergency_db['Emergency ID'] == ID])
            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue

            if commit == 'y':
                self.emergencies_db = emergency_db.copy()
                emergency_db.to_csv('emergency_database.csv', index=False)
                break
            else:
                continue
        print(100*'=')

    def amend_camp_capacity(self):
        '''
        Allows user to change the capacity of one of the camps. Selection by camp ID.
        '''
        camp_db = self.camps_db.copy()
        print(100*'=')
        print("Select which camp's capacity needs to be altered")
        print('Expected Inputs:\n' +
              '\t>Emergency ID\n')
        print('[B] to go back')
        print('[Q] to quit\n')
        print(camp_db)

        while True:
            while True:
                choose_camp = input(
                    "\nChoose camp for which you want to edit: ").upper()
                if choose_camp in list(camp_db['Camp ID']) or choose_camp == 'Q' or choose_camp == 'B':
                    break
                else:
                    print('Please select a valid camp')
                    continue
            if choose_camp == 'Q' or choose_camp == 'B':
                print(100*'=')
                menu(self.functions)
                exit()

            print(camp_db.loc[camp_db["Camp ID"] == choose_camp])

            while True:
                cap = input("\nState new capacity: ")
                if cap == 'B' or cap == 'Q':
                    break
                else:
                    try:
                        cap = int(cap)
                        if cap < int(camp_db.loc[camp_db['Camp ID'] == choose_camp]['Number of refugees']):
                            print(
                                'Your new capacity is lower than current number of refugees.')
                            continue
                        else:
                            break
                    except ValueError:
                        print('Your input needs to be an integer')
                        continue
            if cap == 'B':
                continue
            elif cap == 'Q':
                print(100*'=')
                menu(self.functions)
                exit()

            camp_db.loc[camp_db['Camp ID'] == choose_camp, 'Capacity'] = cap
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
        print(100*'=')

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
                    if self.quit == True:
                        break
                if self.quit == True:
                    break

                vol_df.loc[len(vol_df.index)] = [
                    username, '', '', '', camp, '']
                users_df.loc[len(users_df.index)] = [
                    username, password, 'volunteer', 'TRUE']
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
                        'Volunteer'+str(new_usr_index+i), '111', 'volunteer', 'TRUE']

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

    def write_camp(self):
        '''
        Allows admin to add a news camp to an existing emergency.
        '''
        self.quit = False
        counter = 0
        self.count_ref_vol()
        print(100*'=')
        print('Please provide details of the new camp')
        print('Expected Inputs:\n' +
              '\t>Country\n' +
              '\t>Emergency ID\n' +
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
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    # and country_id in list(emergency_df['Emergency ID']):
                    if country in countries.keys():
                        country_id = countries[country]['Country code']
                        if True in list(emergency_df['Emergency ID'].str.contains('PK', case=False)):
                            break
                    print('Please select country with an existing emergency.')
                return 1

            def assign_emergency():
                global emergency
                emergencies_in_country = emergency_df.loc[emergency_df['Emergency ID'].str.contains(
                    country_id, case=False)]
                if len(emergencies_in_country.index) >= 1:
                    print('\n', emergencies_in_country)
                while True:
                    if len(emergencies_in_country.index) > 1:
                        emergency = input(
                            '\nPlease select which emergency you would like to assign your camp to: ')
                        if emergency == 'B' or emergency == 'Q':
                            break
                        if emergency in list(emergencies_in_country['Emergency ID']):
                            break
                        else:
                            print('Please select valid ID.')
                            continue
                    else:
                        emergency = list(
                            emergencies_in_country['Emergency ID'])[0]
                        break
                if emergency == 'B':
                    return -1
                elif emergency == 'Q':
                    print(100*'=')
                    menu(self.functions)
                    exit()
                else:
                    return 1

            def assign_capacity():
                global capacity
                while True:
                    capacity = input("\nEnter maximum camp capacity:")
                    if capacity == 'B' or emergency == 'Q':
                        break
                    if capacity.isdigit() == False:
                        print('Please enter an integer.')
                        continue
                    break
                if capacity == 'B':
                    return -1
                elif capacity == 'Q':
                    print(100*'=')
                    menu(self.functions)
                    exit()
                else:
                    return 1

            inputs = [assign_country, assign_emergency, assign_capacity]

            while counter < len(inputs):
                counter += inputs[counter]()
                if self.quit == True:
                    break
            if self.quit == True:
                break

            new_camp_index = len(
                camps_df.loc[camps_df['Camp ID'].str.contains(emergency, case=False)].index)+1
            new_ID = emergency + '-' + str(new_camp_index)

            camps_df.loc[len(camps_df.index)] = [
                new_ID, country, '', capacity, emergency, '']

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
                counter = 0
                continue
        print(100*'=')


class Volunteer(CentralFunctions):

    def __init__(self, current_user, camp_of_user):
        CentralFunctions.__init__(self)
        self.functions = {"1": {'method': self.amend_self_info,         'message': '[1] - Amend your profile info', },
                          "2": {'method': self.call_camps,              'message': '[2] - See camp info', },
                          "3": {'method': self.create_profile,          'message': '[3] - Create refugee profile', },
                          "4": {'method': self.amend_refugee_profile,   'message': '[4] - Amend refugee profile', }}
        self.current_user = current_user
        self.camp_of_user = camp_of_user

    def amend_self_info(self):
        '''
        Allows volunteer user to input their name, surname, phone number and availability.
        '''
        print(100*'=')
        print('Please select input or update any information about you.')
        print("If you do NOT wish to change current value press ENTER during input.")
        print('Expected Inputs:\n' +
              '\t>First name\n' +
              '\t>Family name\n' +
              '\t>Phone number\n' +
              '\t>Availability\n')
        print('[B] to go back')
        print('[Q] to quit\n')

        vol_df = self.vol_db
        print(vol_df.loc[vol_df['Username'] == self.current_user])
        questions = ['\nEnter new first name: ', '\nEnter new second name: ',
                     '\nEnter new phone number in the format [44_______]:', '\nEnter new availability: ']

        def go_back(questionStack):
            i = 0
            answerStack = []

            while i < len(questionStack):
                if i == 0 or i == 1:
                    while True:
                        answer = input(questionStack[i])
                        if answer == 'B':
                            if i == 0:
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            answerStack.pop()
                            i -= 1
                        elif answer == 'Q':
                            print(100*'=')
                            menu(self.functions)
                            exit()
                        elif answer == '':
                            answer = vol_df.iloc[vol_df.index[vol_df['Username']
                                                              == self.current_user][0], i+1]
                        elif not answer.isalpha():
                            print("Please enter a valid name.")
                            continue
                        break
                elif i == 2:
                    while True:
                        answer = input(questionStack[i])
                        if answer == 'B':
                            if i == 0:
                                break
                            answerStack.pop()
                            i -= 1
                        elif answer == 'Q':
                            print(100*'=')
                            menu(self.functions)
                            exit()
                        elif answer == '':
                            answer = vol_df.iloc[vol_df.index[vol_df['Username']
                                                              == self.current_user][0], 3]
                        elif not answer.isnumeric():
                            print("Please enter a valid phone number.")
                            continue
                        elif len(answer) != 9 or answer[:2] != "44":
                            print("Invalid format.")
                            continue
                        break
                elif i == 3:
                    while True:
                        answer = input(questionStack[i])
                        if answer == 'B':
                            if i == 0:
                                break
                            answerStack.pop()
                            i -= 1
                        elif answer == 'Q':
                            print(100*'=')
                            menu(self.functions)
                            exit()
                        elif answer == '':
                            answer = vol_df.iloc[vol_df.index[vol_df['Username']
                                                              == self.current_user][0], 5]
                        elif not answer.isnumeric():
                            print("Invalid input.")
                            continue
                        elif int(answer) > 48:
                            print(
                                "Availability exceeds maximum weekly working hours (48h).")
                            continue
                        break
                if answer == 'B':
                    continue

                answerStack.append(answer)
                i += 1

            return answerStack

        while True:
            answers = go_back(questions)
            vol_df.loc[vol_df['Username'] == self.current_user] = [
                self.current_user, answers[0], answers[1], answers[2], self.camp_of_user, answers[3]]

            print('\n', vol_df.loc[vol_df['Username'] == self.current_user])
            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue

            if commit == 'y':
                self.emergencies_db = vol_df.copy()
                vol_df.to_csv('volunteer_database.csv', index=False)
                break
            else:
                answers = []
                continue
        print(100*'=')


def session_over_message():
    print(100*'=')
    print('\nSESSION OVER')
    print(100*'=')


def menu(functions):
    while True:
        print(100*'=')
        print('MAIN MENU')
        print('\nChoose an interaction by typing the corresponding number.')
        print('Example: type "1" to a'+functions['1']['message'][7:]+'.\n')
        for i in range(len(functions.keys())):
            print(functions[str(i+1)]['message'])
        print('\n[Q] to end session')
        user_input = input('\nPlease select your interaction: ')
        if user_input == 'Q':
            session_over_message()
            exit()
        if user_input not in functions.keys():
            print('Please select valid input.')
            continue
        print(100*'=')
        functions[user_input]['method']()


if __name__ == '__main__':
    login = CentralFunctions()
    login.users_login()
    if login.current_user != 'adm':
        vol = Volunteer(login.current_user, login.camp_of_user)
        print(vol.current_user)
        menu(vol.functions)
    else:
        adm = Admin(login.current_user, login.camp_of_user)
        print(adm.current_user)
        menu(adm.functions)