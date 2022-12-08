import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import re
import smtplib
import random
from email.message import EmailMessage
import ssl


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

    def save(self, dataFrame, fileName):
        try:
            dataFrame.to_csv(f"{fileName}", index=False)
            return True
        except PermissionError:
            return False

    def users_login(self):
        '''
        Login function that allows you to login normally with 111 password first time and
        once you input new password and email you user your double authentication.
        '''
        users_dict = self.user_db.copy().set_index('username').to_dict(orient='index')
        users_df = self.user_db.copy()
        vol_dict = self.vol_db.copy().set_index('Username').to_dict(orient='index')
        while True:
            while True:
                username = input('\nPlease input your USERNAME: ').strip()

                if username not in users_dict:
                    print('Username is incorrect.')
                elif not users_dict[username]['activated']:
                    print('Account not activated. Please contact your admin.')
                else:
                    break

            self.current_user = username
            count_password = 0 # counts the amount of time password was typed wrongly
            # IF PASSWORD = 111
            # if users_df.loc[users_df['username'] == username,'email'].values[0] == '': # CHECKS IF EMAIL IS SET
            if users_df.loc[users_df['username'] == username, 'password'].values[
                0] == '111':  # CHECKS IF PASSWORD IS 111

                while True:
                    password = input('\nPlease input your PASSWORD: ').strip()
                    if password == 'B':
                        break
                    elif password != users_dict[username]['password']:
                        print('Password is incorrect.')
                        count_password += 1
                        left_attempts = 3 - count_password
                        print(f"You have {left_attempts} attempts left ")
                        if count_password == 3:
                            if self.user_db.loc[self.user_db["username"] == self.current_user]['role'].values[0] == "volunteer":
                                print("Your account was deactivated. Please contact admin")
                                self.user_db.loc[self.user_db["username"] == self.current_user, 'activated'] = False
                                self.user_db.to_csv("user_database.csv",index=False)
                            exit()
                if password == 'B':
                    continue
                print('')
                print(100 * '=')
                if username == 'admin':
                    self.current_user = 'admin'
                    self.camp_of_user = 'adm'
                    print(f'Welcome admin!')
                    print('WARNING: YOUR PASSWORD IS IN DANGER')
                else:
                    name = vol_dict[username]['First name']
                    self.camp_of_user = vol_dict[username]['Camp ID']
                    print(f'Welcome {name}!')
                    print(
                        'WARNING: PLEASE ADD YOUR PERSONAL INFORMATION AND CHANGE PASSWORD')
                break
            # IF PASSWORD != 111
            else:

                while True:
                    password = input('\nPlease input your PASSWORD: ').strip()
                    if password == 'B':
                        break
                    elif password != users_dict[username]['password']:
                        print('Password is incorrect.')
                        count_password += 1
                        left_attempts = 3 - count_password
                        print(f"You have {left_attempts} attempts left ")
                        if count_password == 3:
                            if self.user_db.loc[self.user_db["username"] == self.current_user]['role'].values[
                                0] == "volunteer":
                                print("Your account was deactivated. Please contact admin")
                                self.user_db.loc[self.user_db["username"] == self.current_user, 'activated'] = False
                                self.user_db.to_csv("user_database.csv", index=False)
                            exit()
                        continue
                    break
                if password == 'B':
                    continue

                print("\nEmail with One-Time-Password to reset password was sent to you.")
                otp = ''.join([str(random.randint(0, 9)) for x in range(4)])
                email_sender = "hemsystem1@gmail.com"
                email_password = "asbwtshlldlaalld"
                email_receiver = self.user_db[self.user_db["username"]
                                              == self.current_user]['email'].values[0]

                subject = "OTP to login"
                body = """Yours OTP to login is: {}""".format(str(otp))
                mail = EmailMessage()
                mail["From"] = email_sender
                mail["To"] = email_receiver
                mail["Subject"] = subject
                mail.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver,
                                  mail.as_string())

                while True:
                    inpt = input("\nInput here the OTP: ")
                    if inpt == 'B':
                        break
                    elif otp != inpt:
                        print("Please enter valid OTP.")
                    else:
                        break
                if inpt == 'B':
                    continue

                print('')
                print(100 * '=')
                if username == 'admin':
                    self.camp_of_user = 'adm'
                    print('Welcome back admin!')
                else:
                    name = vol_dict[username]['First name']
                    self.camp_of_user = vol_dict[username]['Camp ID']
                    print(f'Welcome back {name}!')
                break

    def create_profile(self):
        '''
        Interactive method which allows to add new family to the list
        '''
        while True:
            print('[Q] to go back to main menu')
            name = input("State name of family's lead member: ")
            if name == "q" or name == "Q":
                print(100 * '=')
                menu(self.functions)
                exit()
            while True:
                print('[B] to go back to main menu')
                surname = input("State surname of the family: ")
                if surname == "b" or surname == "B":
                    break
                if not name.isalpha() or not surname.isalpha():
                    print("You can't use numbers for this input. Try again ")
                while True:
                    print('[B] to go back to main menu')
                    mental_state = input(
                        "Describe the mental state of the family: ")
                    if mental_state == "b" or mental_state == "B":
                        break
                    while True:
                        physical_state = input(
                            "Describe the physical state of the family: ")
                        if physical_state == "b" or physical_state == "B":
                            break
                        while True:
                            print('[Q] to go back to main menu')
                            no_of_members = (
                                input("Type the number of family members: "))
                            if no_of_members == "b" or no_of_members == "B":
                                break
                            try:
                                no_of_members = int(no_of_members)

                            except ValueError:
                                print("It has to be an integer")

                            if self.current_user == 'adm':
                                emergency_options = self.emergencies_db["Emergency ID"]
                                print(*emergency_options, sep='\n')
                                emergency_list = self.emergencies_db["Emergency ID"].tolist(
                                )
                                while True:
                                    print('[B] to go back to main menu')
                                    emergency_id = input("Choose emergency: ")
                                    if emergency_id == 'b' or emergency_id == "B":
                                        break
                                    elif emergency_id not in emergency_list:
                                        print("Invalid input for emergency")
                                    camp_id = self.refugee_db.loc[self.refugee_db['Camp ID'].str.contains(
                                        emergency_id, case=False)]['Camp ID']
                                    camp_id_list = camp_id.tolist()
                                    print(*set(camp_id), sep='\n')
                                    while True:
                                        print('[B] to go back to main menu')
                                        camp_choice = input(
                                            "Choose a camp to which you want to assign family: ")
                                        if camp_choice not in camp_id_list:
                                            print(
                                                "You have to choose from a list of available camps!")
                                        elif camp_choice == "b" or camp_choice == "B":
                                            break

                                        family_count = len(self.refugee_db.loc[self.refugee_db['Camp ID'].str.contains(
                                            camp_choice, case=False)]) + 1
                                        family_id = str(
                                            family_count) + camp_choice
                                        self.refugee_db.loc[len(self.refugee_db)] = [family_id, name, surname, camp_choice,
                                                                                     mental_state, physical_state,
                                                                                     no_of_members]
                                        self.refugee_db.to_csv(
                                            "refugee_db.csv", index=False)
                                        self.save(self.refugee_db,
                                                  'refugee_database.csv')
                                        print("New refugee family was created")
                                        print(100 * '=')
                                        menu(self.functions)
                                        exit()
                            else:
                                camp_choice = self.vol_db[self.vol_db['Camp ID']
                                                          == self.camp_of_user]['Camp ID'].values[0]
                                family_count = len(self.refugee_db.loc[self.refugee_db['Camp ID'].str.contains(
                                    camp_choice, case=False)]) + 1
                                family_id = str(family_count) + camp_choice

                                self.refugee_db.loc[len(self.refugee_db)] = [
                                    family_id, name, surname, camp_choice, mental_state, physical_state, no_of_members]
                                self.refugee_db.to_csv(
                                    "refugee_db.csv", index=False)
                                self.save(self.refugee_db,
                                          'refugee_database.csv')
                                print("New refugee family was created")
                                print(100 * '=')
                                menu(self.functions)
                                exit()

    def call_camps(self):
        print("[1] - List of all camps")
        print("[2] - total number of camps")
        print("[3] - Number of volunteers in each camp")
        print("[4] - number of refugees in each camp")
        print("[5] - Capacity by camp")
        print("[6] - Number of camps in each area")
        print("[7] - Number of active camps")
        print("[8] - Number of inactive camps")
        print("[9] - Number of camps by emergency type")
        print("Choose [Q] if you want exit this summary")

        while True:

            user_input = input("Choose interaction: ")
            local_db = self.camps_db.merge(
                self.emergencies_db, on='Emergency ID', how='inner')

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
            elif user_input == '7':
                print(local_db['Close date'].isnull().sum())
            elif user_input == '8':
                print(local_db['Close date'].count())
            elif user_input == '9':
                print(self.emergencies_db.groupby(
                    by=self.emergencies_db['Type']).size())
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

    def call_no_of_refugees(self):
        '''Reads the file and prints out the general list of families in a system with
        some summary about them by sating the number of refugees, their mental and physical
        state per each camp and gives information about each family that is assigned to certain camp.
        Secondly, the method call no of refugees now will only show you camp details of only the one that you are assigned to.
        Unless you are admin then you can see evrything '''

        if self.current_user == "adm":
            countries_camps = self.camps_db["Emergency ID"]
            print(*countries_camps, sep='\n')
            choose_emergency = input(
                "\nChoose emergency for which you want to see the summary:").upper()

            while choose_emergency not in set(countries_camps):
                choose_emergency = input(
                    "\nChoose emergency for which you want to see the summary:").upper()

        else:
            volunteer_campID = self.camp_of_user
            choose_emergency = self.camps_db[self.camps_db["Camp ID"]
                                             == volunteer_campID]["Emergency ID"].values[0]
        print("[1] - List of all refugees for all camps")
        print(
            "[2] - Total number of refugees in chosen camp")
        print("[3] - Number of families in each camp")
        print("[4] - Total summary for each camp")
        print("Choose Quit if you want exit this summary")

        while True:
            user_input = input("Choose interaction: ")
            if user_input == '1':
                country_refugees = self.camps_db[self.camps_db["Emergency ID"]
                                                 == choose_emergency]
                print(country_refugees)

            elif user_input == "2":
                number_of_refugee = self.camps_db[self.camps_db["Emergency ID"]
                                                  == choose_emergency]['Number of refugees']
                print("Number of refugee in {}: ".format(
                    choose_emergency), *number_of_refugee, sep='\n')

            elif user_input == "3":
                camp_id = self.camps_db[self.camps_db["Emergency ID"]
                                        == choose_emergency]['Camp ID'].values[0]
                count_camps = self.refugee_db[self.refugee_db["Camp ID"] == camp_id]['Camp ID'].count(
                )
                print("Number of families for camp {}:".format(choose_emergency))
                print(count_camps)
                # print(*count_camps, sep='\n')

            elif user_input == "4":
                camp_id = self.camps_db[self.camps_db["Emergency ID"]
                                        == choose_emergency]['Camp ID'].values[0]
                group_camps = self.refugee_db[self.refugee_db["Camp ID"] == camp_id].groupby(
                    "Camp ID")
                for name, camp in group_camps:
                    print("Camp " + name + "->" +
                          str(len(camp)) + " family/families")
                    print(camp)
            else:
                break


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
        If system detects no lack of an input it will launch a "flowing" version, otherwise it will launch
        "selective" version of this method.
        '''
        current_name = self.vol_db[self.vol_db["Username"]
                                   == self.current_user]["First name"].values[0]
        current_second_name = self.vol_db[self.vol_db["Username"]
                                          == self.current_user]["Second name"].values[0]
        current_phone = str(
            self.vol_db[self.vol_db["Username"] == self.current_user]["Phone"].values[0])
        current_availability = self.vol_db[self.vol_db["Username"]
                                           == self.current_user]["Availability"].values[0]
        password = self.user_db[self.user_db["username"]
                                == self.current_user]['password'].values[0]
        current_email = self.user_db[self.user_db["username"]
                                     == self.current_user]['email'].values[0]
        vol_df = self.vol_db.copy()
        users_df = self.user_db.copy()

        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        def check_email(email):
            if(re.search(regex, email)):
                return True
            else:
                return False

        if '' not in list(self.vol_db.loc[self.vol_db['Username'] == self.current_user]):

            while True:
                print(100 * '=')
                print(
                    'Please select which information you would like to change about yourself.')
                print('Input a digit to change the correpsonding piece of information.')
                print('E.g. input "1" to change your first name.\n' +
                      '[1] - First name\n' +
                      '[2] - Family name\n' +
                      '[3] - Phone number\n' +
                      '[4] - Availability\n' +
                      '[5] - Change password\n' +
                      '[6] - Change email')
                print('\n[B] to go back')
                print('[Q] to quit')

                user_input = input("\nChoose interaction: ")

                if user_input == '1':
                    print(
                        f"Currently, your first name is set to {current_name}.")
                    while True:
                        inpt = input("\nEnter new first name: ")
                        inpt = inpt.capitalize()
                        if inpt == 'B' or inpt == 'Q':
                            break
                        elif not inpt.isalpha():
                            print("Please enter a valid name.")
                            continue
                        current_name = inpt
                        break

                elif user_input == '2':
                    print(
                        f"Currently, your second name is set to {current_second_name}.")
                    while True:
                        inpt = input("\nEnter new second name: ")
                        inpt = inpt.capitalize()
                        if inpt == 'B' or inpt == 'Q':
                            break
                        elif not inpt.isalpha():
                            print("Please enter a valid name.")
                            continue
                        else:
                            current_second_name = inpt
                            break

                elif user_input == '3':
                    print(
                        f"Currently, your phone number is set to +{current_phone}.")
                    while True:
                        inpt = input(
                            "\nEnter new phone number in the format +44(0)_______: ")
                        if inpt == 'B' or inpt == 'Q':
                            break
                        elif not inpt.isnumeric():
                            print("Please enter a valid phone number.")
                            continue
                        elif len(inpt) != 10:
                            print("Invalid format.")
                            continue
                        else:
                            current_phone = inpt
                            break

                elif user_input == '4':
                    print(
                        f"Currently, your availability is set to {current_availability}.")
                    while True:
                        inpt = input("\nEnter new availability: ")
                        if inpt == 'B' or inpt == 'Q':
                            break
                        elif not inpt.isnumeric():
                            print("Invalid input.")
                        elif int(inpt) > 48:
                            print(
                                "Availability exceeds maximum weekly working hours (48h).")
                        else:
                            current_availability = inpt
                            break

                elif user_input == '5':
                    print("Email with OTP to reset password was sent to you")
                    otp = ''.join([str(random.randint(0, 9))
                                  for x in range(4)])
                    email_sender = "hemsystem1@gmail.com"
                    email_password = "asbwtshlldlaalld"
                    email_receiver = self.user_db[self.user_db["username"]
                                                  == self.current_user]['email'].values[0]

                    subject = "OTP to reset password"
                    body = """Yours OTP to reset password is: {}""".format(
                        str(otp))
                    mail = EmailMessage()
                    mail["From"] = email_sender
                    mail["To"] = email_receiver
                    mail["Subject"] = subject
                    mail.set_content(body)
                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(
                            email_sender, email_receiver, mail.as_string())
                    while True:
                        inpt = input("\nInput here the OTP: ")
                        if inpt == 'B' or inpt == 'Q':
                            break
                        elif otp != inpt:
                            print("Please enter valid OTP.")
                        else:
                            break
                    while True:
                        inpt = input("\nType your new password: ")
                        if inpt == 'B' or inpt == 'Q':
                            break
                        elif password == inpt:
                            print(
                                "Sorry but your password can't be the same as the previous one.")
                        elif len(inpt) < 8:
                            print(
                                "Sorry but your password needs to be at least 8 characters long.")
                        else:
                            password = inpt
                            break

                if user_input == '6':
                    print(f"Currently, your email is set to {current_email}.")
                    while True:
                        inpt = input("\nEnter new email: ")
                        inpt = inpt.capitalize()
                        if inpt == 'B' or inpt == 'Q':
                            break
                        elif check_email(inpt):
                            print("Please enter a valid email address.")
                            continue
                        current_email = inpt
                        break

                else:
                    print('Invalid input. Please select from the options above.')
                    continue

                if inpt == 'B':
                    continue
                elif inpt == 'Q' or user_input == 'B' or user_input == 'Q':
                    print(100*'=')
                    menu(self.functions)
                    exit()

                vol_df.loc[vol_df['Username'] == self.current_user] = [self.current_user, current_name,
                                                                       current_second_name, current_phone, self.camp_of_user, current_availability]
                users_df.loc[users_df['username'] == self.current_user, [
                    'password', 'email']] = (password, current_email)

                print(
                    '\n', vol_df.loc[vol_df['Username'] == self.current_user])
                print(users_df.loc[users_df['username'] == self.current_user, [
                      'username', 'password', 'email']])

                while True:
                    commit = input('\nCommit changes? [y]/[n] ')
                    if commit == 'y' or commit == 'n':
                        break
                    else:
                        print('Your input is not recognised')
                        continue

                if commit == 'y':
                    self.vol_db = vol_df.copy()
                    vol_df.to_csv('volunteer_database.csv', index=False)
                else:
                    counter = 0
                    continue

                while True:
                    repeat = input(
                        '\nWould you like to alter another parameter? [y]/[n] ')
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

            print(100*'=')

        else:

            print(100*'=')
            print('Please select input or update any information about you.')
            print("If you do NOT wish to change current value press ENTER during input.")
            print('Expected Inputs:\n' +
                  '\t>First name\n' +
                  '\t>Family name\n' +
                  '\t>Phone number\n' +
                  '\t>Availability\n' +
                  '\t>Email\n' +
                  '\t>Password\n')
            print('[B] to go back')
            print('[Q] to quit\n')

            print(vol_df.loc[vol_df['Username'] == self.current_user])
            questions = ['\nEnter first name: ', '\nEnter second name: ',
                         '\nEnter phone number in the format [+44(0)_______]:', '\nEnter availability: ',
                         '\nEnter your email', '\nEnter your new password (over 8 characters long)']

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
                                answer = current_phone
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
                                answer = current_availability
                            elif not answer.isnumeric():
                                print("Invalid input.")
                                continue
                            elif int(answer) > 48:
                                print(
                                    "Availability exceeds maximum weekly working hours (48h).")
                                continue
                            break
                    elif i == 4:
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
                                answer = current_email
                            elif len(inpt) < 8:
                                print(
                                    "Sorry but your password needs to be at least 8 characters long.")
                                continue
                            break
                    elif i == 5:
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
                                answer = password
                            elif len(inpt) < 8:
                                print(
                                    "Sorry but your password needs to be at least 8 characters long.")
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

                print(
                    '\n', vol_df.loc[vol_df['Username'] == self.current_user])
                print(users_df.loc[users_df['username'] == self.current_user, [
                      'username', 'password', 'email']])
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

    # def amend_self_info(self):
    #     '''
    #     Allows volunteer user to input their name, surname, phone number and availability.
    #     '''
    #     print(100 * '=')
    #     print('Please select which information you would like to change about yourself.')
    #     print('Possible interactions:\n' +
    #           '[1] - First name\n' +
    #           '[2] - Family name\n' +
    #           '[3] - Phone number\n' +
    #           '[4] - Availability\n' +
    #           '[5] - Change password\n')
    #     while True:
    #         print('[Q] to go back to main menu')
    #         user_input = input("Choose interaction:")
    #         if user_input == '1':
    #             current_name = self.vol_db[self.vol_db["Username"] == self.current_user]["First name"].values[0]
    #             print(f"Currently, your first name is set to {current_name}.")
    #             while True:
    #                 new_name = input("Enter new first name:")
    #                 new_name = new_name.capitalize()
    #                 if not new_name.isalpha():
    #                     print("Please enter a valid name.")
    #                 else:
    #                     break
    #             while True:
    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
    #                 if user_input == "y":
    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "First name"] = new_name
    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
    #                     print(f"First name has been set to {new_name}.")
    #                     break
    #                 elif user_input == "b":
    #                     print(100 * '=')
    #                     menu(self.functions)
    #                     exit()
    #                 else:
    #                     print("Invalid input.")
    #         elif user_input == '2':
    #             current_second_name = self.vol_db[self.vol_db["Username"] == self.current_user]["Second name"].values[0]
    #             print(f"Currently, your second name is set to {current_second_name}.")
    #             while True:
    #                 new_second_name = input("Enter new second name:")
    #                 new_second_name = new_second_name.capitalize()
    #                 if not new_second_name.isalpha():
    #                     print("Please enter a valid name.")
    #                 else:
    #                     break
    #             while True:
    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
    #                 if user_input == "y":
    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "Second name"] = new_second_name
    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
    #                     print(f"Second name has been set to {new_second_name}.")
    #                     break
    #                 elif user_input == "b":
    #                     print(100 * '=')
    #                     menu(self.functions)
    #                     exit()
    #                 else:
    #                     print("Invalid input.")
    #         elif user_input == '3':
    #             current_phone = str(self.vol_db[self.vol_db["Username"] == self.current_user]["Phone"].values[0])
    #             print(f"Currently, your phone number is set to +{current_phone}.")
    #             while True:
    #                 new_phone = input(
    #                     "Enter new phone number in the format +44_______:")
    #                 if not new_phone.isnumeric():
    #                     print("Please enter a valid phone number.")
    #                 elif len(new_phone) != 9:
    #                     print("Invalid format.")
    #                 elif new_phone[:2] != "44":
    #                     print("Invalid format.")
    #                 else:
    #                     break
    #             while True:
    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
    #                 if user_input == "y":
    #                     # new_phone = f"+{str(new_phone)}"
    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "Phone"] = new_phone
    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
    #                     print(f"Phone number has been set to +{new_phone}.")
    #                     break
    #                 elif user_input == "b":
    #                     print(100 * '=')
    #                     menu(self.functions)
    #                     exit()
    #                 else:
    #                     print("Invalid input.")
    #         elif user_input == '4':
    #             current_availability = self.vol_db[self.vol_db["Username"] == self.current_user]["Availability"].values[0]
    #             print(f"Currently, your availability is set to {current_availability}.")
    #             while True:
    #                 new_availability = input("Enter new availability:")
    #                 if not new_availability.isnumeric():
    #                     print("Invalid input.")
    #                 elif int(new_availability) > 48:
    #                     print("Availability exceeds maximum weekly working hours (48h).")
    #                 else:
    #                     break
    #             while True:
    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
    #                 if user_input == "y":
    #                     new_availability= f"{new_availability}h"
    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "Availability"] = new_availability
    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
    #                     print(f"Availability has been set to {new_availability}.")
    #                     break
    #                 elif user_input == "b":
    #                     print(100 * '=')
    #                     menu(self.functions)
    #                     exit()
    #                 else:
    #                     print("Invalid input.")
    #         elif user_input == '5':
    #             print("Email with OTP to reset password was sent to you")
    #             otp = ''.join([str(random.randint(0, 9)) for x in range(4)])
    #             email_sender = "hemsystem1@gmail.com"
    #             email_password = "asbwtshlldlaalld"
    #             email_receiver = self.user_db[self.user_db["username"] == self.current_user]['email'].values[0]

    #             subject = "OTP to reset password"
    #             body = """Yours OTP to reset password is: {}""".format(str(otp))
    #             mail = EmailMessage()
    #             mail["From"] = email_sender
    #             mail["To"] = email_receiver
    #             mail["Subject"] = subject
    #             mail.set_content(body)
    #             context = ssl.create_default_context()

    #             with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    #                 smtp.login(email_sender, email_password)
    #                 smtp.sendmail(email_sender, email_receiver, mail.as_string())
    #             while True:
    #                 otp_validation = input("Input here the OTP: ")
    #                 if otp != otp_validation:
    #                     print("Please enter valid OTP")
    #                 else:
    #                     break
    #             while True:
    #                 new_password = input("Type your new password: ")
    #                 password = self.user_db[self.user_db["username"] == self.current_user]['password'].values[0]
    #                 if password == new_password:
    #                     print("Sorry but your password can't be the same as the previous one")
    #                 elif len(new_password) < 8:
    #                     print("Sorry but your password needs to be at least 8 characters long")
    #                 else:
    #                     while True:
    #                         user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
    #                         if user_input == "y":
    #                             self.user_db.loc[self.user_db["username"] == self.current_user, 'password'] = new_password
    #                             self.user_db.to_csv("user_database.csv",index=False)
    #                             print("Password has been changed")
    #                             break
    #                         elif user_input == "b":
    #                             print(100 * '=')
    #                             menu(self.functions)
    #                             exit()
    #                         else:
    #                             print("Invalid input.")
    #                     break

    #         elif user_input == "Q" or user_input == "q":
    #             print(100 * '=')
    #             menu(self.functions)
    #             exit()
    #         else:
    #             print("Invalid input. Please select from the following options.")

    # def amend_self_info(self):
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
    if login.current_user != 'admin':
        vol = Volunteer(login.current_user, login.camp_of_user)
        menu(vol.functions)
    else:
        adm = Admin(login.current_user, login.camp_of_user)
        menu(adm.functions)
