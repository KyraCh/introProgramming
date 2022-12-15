import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import datetime
from tabulate import tabulate
import re
import smtplib
import random
from email.message import EmailMessage
import ssl
from colorama import Fore, Back, Style


class CentralFunctions():

    def __init__(self):
        self.user_db = None
        self.vol_db = None
        self.refugee_db = None
        self.camps_db = None
        self.emergencies_db = None
        self.meals_db = None
        self.countries_db = None
        self.organisations_db = None

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
            df['password'] = df['password'].astype(str)
            df.to_csv('user_database.csv',index=False)
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
            df.to_csv('volunteer_database.csv',index=False)
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
            df.to_csv('refugee_database.csv',index=False)
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
            df.to_csv('camp_database.csv',index=False)
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
            df.to_csv('emergency_database.csv',index=False)
            self.emergencies_db = df
        except:
            print("System couldn't read your camplist database file.")
            dataFailure = True

        try:
            df = pd.read_csv('mealplans_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('', inplace=True)
            self.meals_db = df
        except FileNotFoundError:
            meals_db = {'Camp ID': [''], 'Total number of refugees': [''],
                       'Meals per day': [''], 'Days': [''], 'Total meals': [''],
                       'Price per meal': [''], 'Budget per day': [''], 'Total budget': ['']}
            df = pd.DataFrame(meals_db)
            df.to_csv('mealplans_database.csv',index=False)
            self.meals_db = df
        except:
            print("System couldn't read the camps meals database file.")
            dataFailure = True


        try:
            df = pd.read_csv(".sys_countries.csv", index_col='Country name')
            self.countries_db = df
        except:
            print("System couldn't read the countries database file.")
            dataFailure = True
        
        try:
            df = pd.read_csv('.sys_organisation_per_continent.csv')
            self.organisations_db = df
        except:
            print("System couldn't read the Organisations per Continent database file.")
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
                    if password.upper() == 'B':
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
                    else:
                        break
                if password.upper() == 'B':
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
                    print('WARNING: PLEASE ADD YOUR PERSONAL INFORMATION AND CHANGE PASSWORD')
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
                            if self.user_db.loc[self.user_db["username"] == self.current_user]['role'].values[0] == "volunteer":
                                print("Your account was deactivated. Please contact admin")
                                self.user_db.loc[self.user_db["username"] == self.current_user, 'activated'] = False
                                self.user_db.to_csv("user_database.csv", index=False)
                            exit()
                        continue
                    else:
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
        print(100 * '=')
        print('\nPlease provide details of the new refugee family.')
        print('Expected Inputs:\n'+
            '\t>Name of lead family member\n'+
            '\t>Surname of lead family member\n'+
            '\t>Mental state of the family\n'+
            '\t>Physical state of the family\n'+
            '\t>Number of family members')
        if self.current_user == 'admin':
            print('\t>Emergency\n'+
            '\t>Camp')
        print('\n[B] to go back')
        print('[Q] to quit')
        while True:
            refugee_df = self.refugee_db.copy()
            name = input("\nState name of family's lead member: ")
            if name.upper() == "Q" or name.upper() == "B":
                print(100 * '=')
                menu(self.functions)
                exit()
            while True:
                surname = input("\nState surname of the family: ")
                if surname.upper() == "B":
                    break
                elif surname.upper() == "Q":
                    print(100 * '=')
                    menu(self.functions)
                    exit()
                if not name.isalpha() or not surname.isalpha():
                    print("Invalid input.")
                while True:
                    mental_state = input(
                        "\nDescribe the mental state of the family: ")
                    if mental_state.upper() == "B":
                        break
                    elif mental_state.upper() == "Q":
                        print(100 * '=')
                        menu(self.functions)
                        exit()
                    while True:
                        physical_state = input(
                            "\nDescribe the physical state of the family: ")
                        if physical_state.upper() == "B":
                            break
                        elif physical_state.upper() == "Q":
                            print(100 * '=')
                            menu(self.functions)
                            exit()
                        while True:
                            no_of_members = (
                                input("\nType the number of family members: "))
                            if no_of_members.upper() == "B":
                                break
                            elif no_of_members.upper() == "Q":
                                print(100 * '=')
                                menu(self.functions)
                                exit()
                            try:
                                no_of_members = int(no_of_members)

                            except ValueError:
                                print("It has to be an integer")
                                continue

                            if self.current_user == 'admin':
                                while True:
                                    df = self.emergencies_db[["Emergency ID"]]
                                    emergency_list = self.emergencies_db["Emergency ID"].tolist()
                                    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                                    emergency_id = input("\nChoose emergency: ")
                                    if emergency_id.upper() == "B":
                                        break
                                    elif emergency_id.upper() == "Q":
                                        print(100 * '=')
                                        menu(self.functions)
                                        exit()
                                    elif emergency_id not in emergency_list:
                                        print("Invalid input for emergency")
                                        continue
                                    df = self.camps_db.loc[self.camps_db['Camp ID'].str.contains(emergency_id, case=False)][['Camp ID']]
                                    df.drop_duplicates(subset = 'Camp ID', inplace = True)
                                    camp_id_list = list(df['Camp ID'])
                                    if len(camp_id_list) == 0:
                                        print("!There are no camps in this emergency.")
                                        continue
                                    while True:
                                        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                                        camp_choice = input("\nChoose a camp to which you want to assign family: ")
                                        if camp_choice.upper() == "B":
                                            break
                                        elif camp_choice.upper() == "Q":
                                            print(100 * '=')
                                            menu(self.functions)
                                            exit()
                                        elif camp_choice not in camp_id_list:
                                            print("You have to choose from a list of available camps!")
                                            continue
                                        
                                        family_count = len(refugee_df.loc[refugee_df['Camp ID'].str.contains(
                                            camp_choice, case=False)]) + 1
                                        family_id = str(
                                            family_count) + camp_choice
                                        break
                                    if camp_choice.upper() == "B":
                                        continue
                                    break
                                if emergency_id.upper() == "B":
                                    continue
                                break

                            else:
                                camp_choice = self.vol_db[self.vol_db['Camp ID']
                                                          == self.camp_of_user]['Camp ID'].values[0]
                                family_count = len(refugee_df.loc[refugee_df['Camp ID'].str.contains(
                                    camp_choice, case=False)]) + 1
                                family_id = str(family_count) + camp_choice      

                            break
                        if type(no_of_members) == str and no_of_members.upper() == "B":
                            continue
                        break
                    if physical_state.upper() == "B":
                        continue
                    break
                if mental_state.upper() == "B":
                    continue
                break
            if surname.upper() == "B":
                continue
            refugee_df.loc[len(refugee_df)] = [family_id, name, surname, camp_choice, mental_state, physical_state, no_of_members]
            print(tabulate(refugee_df.tail(1), headers='keys', tablefmt='psql', showindex=False))
            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue
            
            if commit == 'y':
                self.refugee_db = refugee_df.copy()
                refugee_df.to_csv('refugee_database.csv', index=False)
                break
            else:
                continue

        print(100 * '=')

    def call_camps(self):
        print(100*'=')
        print('\nChoose an interaction by typing the corresponding number.')
        print('Example: type "1" to view comprehensive data on all refugee camps.\n')
        print("[1] - List of all camps")
        print("[2] - Total number of camps")
        print("[3] - Number of volunteers in each camp")
        print("[4] - Number of refugees in each camp")
        print("[5] - Capacity by camp")
        print("[6] - Number of camps in each area")
        print("[7] - Number of active camps")
        print("[8] - Number of inactive camps")
        print("[9] - Number of camps by emergency type")
        print('\n[B] to go back')
        print('[Q] to quit')
        
        self.count_ref_vol()
        while True:

            user_input = input("\nChoose interaction: ")
            local_db = self.camps_db.merge(self.emergencies_db, on='Emergency ID', how='inner')

            if user_input == '1':
                df = self.camps_db
                print("\nSee camp list:")
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input == "2":
                print("\nNumber of camps: ", len(self.camps_db.index))
            elif user_input == "3":       
                df = self.camps_db.loc[self.camps_db['Number of volunteers'] != '', ['Camp ID','Number of volunteers']]
                print("\nNumber of volunteers per camp:")
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input == "4":
                df = self.camps_db.loc[self.camps_db['Number of refugees'] != '', ['Camp ID','Number of refugees']]
                print('Number of refugees per each non-empty camp:')
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input == "5":
                df = self.camps_db[['Camp ID','Capacity']]
                print("\nCapacity by camp:")
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input == "6":
                df = self.camps_db.Location.value_counts().reset_index()
                df.rename(columns = {'index':'Location', 'Location':'Number of camps'}, inplace = True)
                print("\nCamps for each disaster:")
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input == '7':
                local_db = local_db[['Camp ID', 'Emergency ID', 'Location_x', 'Capacity', 'Number of volunteers', 'Number of refugees', 'Type', 'Description', 'Start date', 'Close date']]
                local_db.rename(columns={"Location_x": "Location"}, inplace=True)
                print('\nNumber of active camps: ', len(local_db[local_db['Close date'] == '']))
                df = local_db[local_db['Close date'] == '']
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input == '8':
                local_db = local_db[['Camp ID', 'Emergency ID', 'Location_x', 'Capacity', 'Number of volunteers', 'Number of refugees', 'Type', 'Description', 'Start date', 'Close date']]
                local_db.rename(columns={"Location_x": "Location"}, inplace=True)
                print('\nNumber of inactive camps: ',len(local_db[local_db['Close date'] != '']))
                df = local_db[local_db['Close date'] != '']
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input == '9':
                df = self.emergencies_db.Type.value_counts().reset_index()
                df.rename(columns = {'index':'Type', 'Type':'Number of camps'}, inplace = True)
                print("\nCamps in each area:")
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif user_input.upper() == 'B' or user_input.upper() == 'Q':
                break
            else:
                print('Invalid input')
            continue
        
        print(100*'=')

    def call_volunteers(self):
        self.count_ref_vol()
        while True:
            vol_data = self.vol_db.copy()
            camp_data = self.camps_db.copy()
            print(100*'=')
            print('\nChoose an interaction by typing the corresponding number.')
            print('Example: type "1" to view comprehensive data on all volunteers.\n')
            print("[1] - View all volunteer data\n"
                  "[2] - See volunteer data by camp\n"
                  "[3] - See total number of volunteers\n"
                  "[4] - See number of volunteers by camp\n"
                  "[5] - Check if the volunteer exists\n")
            print('[B] to go back')
            print('[Q] to quit')
            choose_action = input('\nEnter here: ')
            if choose_action == '1':
                print('')
                print(tabulate(vol_data, headers='keys', tablefmt='psql', showindex=False))
                #print(f"\n{vol_data}")
            elif choose_action == '2':
                while True:
                    print('\nList of Camp IDs: ')
                    print(tabulate(self.camps_db[['Camp ID']], headers='keys', tablefmt='psql', showindex=False))
                    choose_camp = input('\nEnter a Camp ID: ')
                    if choose_camp.upper() == 'B':
                        break
                    elif choose_camp in vol_data['Camp ID'].values:
                        df = self.vol_db.loc[self.vol_db['Camp ID'] == choose_camp]
                        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                    else:
                        print(Fore.RED + '\nInvalid Camp ID. Try again.')
                        print(Style.RESET_ALL)
            elif choose_action == '3':
                print(f"There are {len(vol_data)} volunteers")
            elif choose_action == '4':
                df = camp_data[['Camp ID','Number of volunteers']]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            elif choose_action == '5':
                while True:
                    def go_back(questionStack):
                        i = 0
                        answerStack = []
                        while i < len(questionStack):
                            if i == 0:
                                while True:
                                    answer = input(questionStack[i])
                                    if answer.upper() == 'B' or answer.upper() == 'Q':
                                        break
                                    elif answer.isnumeric():
                                        print(Fore.RED + 'First Name cannot include a number. Try again.')
                                        print(Style.RESET_ALL)
                                        continue
                                    else:
                                        break
                            elif i == 1:
                                while True:
                                    answer = input(questionStack[i])
                                    if answer.upper() == 'B' or answer.upper() == 'Q':
                                        break
                                    elif answer.isnumeric():
                                        print(Fore.RED + 'Last Name cannot include a number. Try again.')
                                        print(Style.RESET_ALL)
                                        continue
                                    else:
                                        break
                            else:
                                answer = input(questionStack[i])
                            if answer.upper() == 'B':
                                if i == 0:
                                    break
                                answerStack.pop()
                                i -= 1
                                continue
                            elif answer.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            answerStack.append(answer)
                            i += 1
                        return answerStack
                    questions = ['\nEnter First Name: ', '\nEnter Last Name: ']
                    answers = go_back(questions)
                    
                    if len(answers) == 0:
                        break
                    if answers[0] in vol_data['First name'].values and answers[1] in vol_data['Second name'].values:
                        print(f'\nHere is our record for {answers[0]} {answers[1]}: \n')
                        df = vol_data[(vol_data['First name'] == answers[0].title()) & (vol_data['Second name'] == answers[1].title())]
                        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                        #print(f"{vol_data[(vol_data['First name'] == answers[0].title()) & (vol_data['Second name'] == answers[1].title())].to_string(index=False)}\n")
                    else:
                        print(Fore.RED + f'\nThere is no volunteer with the name {answers[0]} {answers[1]}\n')
                        print(Style.RESET_ALL)
                if len(answers) == 0:
                    continue
            elif choose_action.upper() == 'Q' or choose_action.upper() == 'B':
                print(100 * '=')
                menu(self.functions)
                exit()
            else:
                print(Fore.RED + '\nInvalid action. Try again.')
                print(Style.RESET_ALL)
        print(100*'=')

    def amend_refugee_profile(self):
        '''
        Interactive method which allows one to amend information about a refugee.
        '''
        while True:
            list_of_refugees = self.refugee_db.copy()
            camps_df = self.camps_db.copy()
            print(100*'=')
            print('\nPlease select which refugee profile you would like to ammend\n')
            print('[B] to go back')
            print('[Q] to quit\n')
            
            if self.current_user == 'admin':
                print(tabulate(list_of_refugees, headers='keys', tablefmt='psql', showindex=False))
            else:
                df = list_of_refugees.loc[list_of_refugees['Camp ID']==self.camp_of_user]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                                
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
                        print('')
                        print(tabulate(camps_df, headers='keys', tablefmt='psql', showindex=False))

                    change = input(f'\nPlease select new value for {list_of_refugees.columns[i]}: ')
                    
                    if change.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    elif change.upper() == 'B':
                        if counter == 0:
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
                            list_of_refugees.loc[list_of_refugees['Family ID'] == iD,'Camp ID']  = change
                            continue
                        else:
                            list_of_refugees.loc[list_of_refugees['Family ID'] == iD,'Family ID'] = '1' + change
                            iD = '1' + change
                            counter += 1
                            list_of_refugees.loc[list_of_refugees['Family ID'] == iD,'Camp ID']  = change
                            continue
                    counter += 1
                    list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0], list_of_refugees.columns[i]] = change
                if change.upper() == 'B':
                    continue
                break
            
            print('')
            df = list_of_refugees.loc[list_of_refugees['Family ID'] == iD]
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

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

    def count_ref_vol(self):  # what is the purpose of this method? - count refugees and volunteers and update camps_db - Fedor
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
                        'Number of refugees'] = refugee_df.loc[refugee_df['Camp ID'] == i]['No. Of Family Members'].sum(axis=0)

        self.camps_db = camp_df.copy()
        camp_df.to_csv('camp_database.csv', index=False)

    def call_no_of_refugees(self):
        '''Reads the file and prints out the general list of families in a system with
        some summary about them by stating the number of refugees, their mental and physical
        state per each camp and gives information about each family that is assigned to certain camp.
        Secondly, the method call no of refugees now will only show you camp details of only the one that you are assigned to.
        Unless you are admin then you can see evrything '''
        print(100*'=')  
        self.count_ref_vol()  
        if self.current_user == "admin":
            print("\nChoose emergency for which you want to see the summary.")
            print("Below are all emergencies with non-zero refugee populations.")
            print('Expected Inputs:\n'+
                '\t>Emergency ID\n')
            df = self.camps_db.loc[self.camps_db['Number of refugees']!='',["Emergency ID"]].drop_duplicates(subset=["Emergency ID"])
            countries_camps = set(df["Emergency ID"])
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            choose_emergency = input("\nChoose emergency for which you want to see the summary: ").upper()
            if choose_emergency == "Q" or choose_emergency == "B":
                print(100 * '=')
                menu(self.functions)
                exit()
            while choose_emergency not in set(countries_camps):
                choose_emergency = input("\nChoose emergency for which you want to see the summary: ").upper()

        else:
            volunteer_campID = self.camp_of_user
            choose_emergency = self.camps_db[self.camps_db["Camp ID"] == volunteer_campID]["Emergency ID"].values[0]
            
        print('\nChoose an interaction by typing the corresponding number.')
        print('Example: type "1" to view comprehensive data on all refugee profiles.\n')
        print("[1] - List of all refugees for all camps")
        print("[2] - Total number of refugees in chosen camp")
        print("[3] - Number of families in each camp")
        print("[4] - Total summary for each camp\n")
        print('[B] to go back')
        print('[Q] to quit')

        while True:
            user_input = input("\nChoose interaction: ")
            print('')
            if user_input == '1':
                country_refugees = self.refugee_db.loc[self.refugee_db['Camp ID'].str.contains(choose_emergency+'-', case=False)]
                print(tabulate(country_refugees, headers='keys', tablefmt='psql', showindex=False))

            elif user_input == "2":
                number_of_refugee = int(self.camps_db[self.camps_db["Emergency ID"] == choose_emergency]['Number of refugees'].values[0])
                print(f"Number of refugees in {choose_emergency} = {number_of_refugee}")

            elif user_input == "3":
                camp_id = self.camps_db[self.camps_db["Emergency ID"] == choose_emergency]['Camp ID'].values[0]
                count_refugees = self.refugee_db[self.refugee_db["Camp ID"] == camp_id]['Camp ID'].count()
                print(f"Number of families for camp {camp_id} = {count_refugees}")

            elif user_input == "4":
                camps = list(self.camps_db.loc[self.camps_db['Number of refugees'] != '','Camp ID'])
                for i in camps:
                    no_of_refugees = str(int(self.camps_db.loc[self.camps_db['Camp ID'] == i,'Number of refugees'].values[0]))
                    refugees_in_camp = self.refugee_db.loc[self.refugee_db['Camp ID'] == i]
                    print("\n\tCamp " + i + " --> " + no_of_refugees + " refugees.\n")
                    print(tabulate(refugees_in_camp, headers='keys', tablefmt='psql', showindex=False))
                    
            elif user_input.upper() == 'B' or user_input.upper() == 'Q':
                print(100*'=')
                menu(self.functions)
                exit()

            else:
                print('Invalid input')
                continue

    def call_help(self):
        print(100*'=')
        print('\nContacts of helpful organisations in emergency area:\n')

        local_db = self.camps_db.merge(self.emergencies_db, on='Emergency ID', how='inner')
        local_db_II = self.countries_db.reset_index().merge(self.organisations_db, on='Continent', how='left').set_index('Country name')
        local_db_III = pd.merge(local_db_II,local_db, left_index=True, right_on='Location_x')
        help = local_db_III.loc[local_db_III['Close date'] == '',['Emergency ID','Camp ID','Type','Name of non-profit organisation','Email','Website']]
        if self.current_user == 'admin':
            help = local_db_III.loc[local_db_III['Close date'] == '',['Location_x','Type','Name of non-profit organisation','Email','Website']].drop_duplicates()
            print(tabulate(help, headers='keys', tablefmt='psql', showindex=False))
            print('')
        else:
            help = local_db_III.loc[local_db_III['Close date'] == '',['Emergency ID','Camp ID','Type','Name of non-profit organisation','Email','Website']]
            print(tabulate(help.loc[help['Camp ID']==self.camp_of_user], headers='keys', tablefmt='psql', showindex=False))
            print('')
        print(100*'=')


class Admin(CentralFunctions):

    def __init__(self, current_user, camp_of_user):
        CentralFunctions.__init__(self,)
        self.functions = {"1": {'method': self.create_emergency,            'message': '[1] - Add new Emergency', },
                          "2": {'method': self.close_emergency,             'message': '[2] - Close Emergency', },
                          "3": {'method': self.call_camps,                  'message': '[3] - See camp info', },
                          "4": {'method': self.write_camp,                  'message': '[4] - Add new camp', },
                          "5": {'method': self.amend_camp_capacity,         'message': '[5] - Amend capacity of a camp', },
                          "6": {'method': self.call_volunteers,             'message': '[6] - See information about volunteers', },
                          "7": {'method': self.write_volunteer,             'message': '[7] - Add new volunteer(s) profile(s)', },
                          "8": {'method': self.admin_volunteer_commands,    'message': '[8] - Amend volunteer activation status', },
                          "9": {'method': self.create_profile,              'message': '[9] - Create refugee profile', },
                          "10": {'method': self.amend_refugee_profile,      'message': '[10] - Amend refugee profile', },
                          "11": {'method': self.call_no_of_refugees,        'message': '[11] - See information about refugees', },
                          "12": {'method': self.camp_finance,               'message': '[12] - Create meal plan for a camp', },
                          "13": {'method': self.call_help,                  'message': '\n[h] - Contacts of local relief organisations', }}
        self.current_user = current_user
        self.camp_of_user = camp_of_user

    def create_emergency(self):
        '''
        Allows user to create emergency by requesting country of emergencym type of emergency, description and start date.
        Automatically assigns emergency ID and upon commit adds new emergency to emergency_database.csv 
        '''
        print(100*'=')
        print('\nPlease input information about your emergency')
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
                            if answer.upper() == 'B' or answer.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            elif answer in list(self.countries_db.index):
                                break
                            else:
                                print('Please select valid country')
                                continue
                    elif i == 3:
                        while True:
                            answer = input(questionStack[i])
                            if answer.upper() == 'B':
                                break
                            elif answer.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            try:
                                datetime.date.fromisoformat(answer)
                                answer = datetime.datetime.strptime(
                                    answer, "%Y-%m-%d").strftime("%d/%m/%Y")
                                break
                            except:
                                print('Please enter a day of valid format [YYYY-MM-DD]: ')
                                continue
                    else:
                        answer = input(questionStack[i])

                    if answer.upper() == 'B':
                        answerStack.pop()
                        i -= 1
                        continue
                    elif answer.upper() == 'Q':
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

            emergency_db.loc[len(emergency_db.index)] = [emergency_id, answers[0], answers[1], answers[2], answers[3], None]
            print('')
            print(tabulate(self.emergencies_db.tail(1), headers='keys', tablefmt='psql', showindex=False))
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
            print('\nPlease specify which emergency you would like to close')
            print('Expected Inputs:\n' +
                  '\t>Emergency ID\n')
            print('[B] to go back')
            print('[Q] to quit\n')
            print(tabulate(emergency_db, headers='keys', tablefmt='psql', showindex=False))

            while True:
                ID = input('\nPlease provide the emergency ID: ').upper()
                if ID in list(emergency_db['Emergency ID']):
                    break
                elif ID.upper() == 'Q' or ID.upper() == 'B':
                    print(100*'=')
                    menu(self.functions)
                    exit()
                else:
                    print('Please provide valid ID')
                    continue

            emergency_db.loc[emergency_db['Emergency ID'] == ID, 'Close date'] = datetime.date.today().strftime("%d/%m/%Y")
            df = emergency_db.loc[emergency_db['Emergency ID'] == ID]
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))            
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
        self.count_ref_vol()
        camp_db = self.camps_db.copy()
        print(100*'=')
        print("\nSelect which camp's capacity needs to be altered")
        print('Expected Inputs:\n' +
              '\t>Emergency ID\n')
        print('[B] to go back')
        print('[Q] to quit\n')
        print(tabulate(camp_db, headers='keys', tablefmt='psql', showindex=False))

        while True:
            while True:
                choose_camp = input(
                    "\nChoose camp for which you want to edit: ").upper()
                if choose_camp in list(camp_db['Camp ID']) or choose_camp.upper() == 'Q' or choose_camp.upper() == 'B':
                    break
                else:
                    print('Please select a valid camp')
                    continue
            if choose_camp.upper() == 'Q' or choose_camp.upper() == 'B':
                print(100*'=')
                menu(self.functions)
                exit()

            print(camp_db.loc[camp_db["Camp ID"] == choose_camp])

            while True:
                cap = input("\nState new capacity: ")
                if cap.upper() == 'B' or cap.upper() == 'Q':
                    break
                else:
                    try:
                        cap = int(cap)
                        limit = 0
                        if camp_db.loc[camp_db['Camp ID'] == choose_camp]['Number of refugees'].values[0] != '':
                            limit = int(camp_db.loc[camp_db['Camp ID'] == choose_camp]['Number of refugees'])
                        if cap < limit:
                            print('Your new capacity is lower than current number of refugees.')
                            continue
                        else:
                            break
                    except:
                        print('Your input needs to be an integer')
                        continue
            if cap.upper() == 'B':
                continue
            elif cap.upper() == 'Q':
                print(100*'=')
                menu(self.functions)
                exit()

            camp_db.loc[camp_db['Camp ID'] == choose_camp, 'Capacity'] = cap
            df = camp_db.loc[camp_db['Camp ID'] == choose_camp]
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

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
        self.count_ref_vol()
        vol_df = self.vol_db.copy()
        users_df = self.user_db.copy()
        camps_df = self.camps_db.copy()
        users_exist = list(users_df['username'])
        camps_exist = list(camps_df['Camp ID'])
        self.quit = False
        print(100*'=')
        print('\nPlease select how would you like to create a new volunteer profile\n')
        print('[1] - manual input')
        print('[2] - automatic creation\n')
        print('[B] to go back')
        print('[Q] to quit\n')

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
                    if inpt.upper() == 'B':
                        self.write_volunteer()
                        exit()
                    if inpt.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    return 1

                def assign_password():
                    global password
                    inpt = input('\nSet a password: ')
                    password = inpt
                    if inpt.upper() == 'B':
                        return -1
                    elif inpt.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    else:
                        return 1

                def assign_camp():
                    global camp
                    while True:
                        print('\nSet camp:\n')
                        print('[1] - View camp summary information')
                        print('[2] - Assign camp\n')
                        print('[B] to go back')
                        print('[Q] to quit')
                        user_input = input('\nChoose interaction: ')
                        if user_input == '1':
                            print(tabulate(camps_df, headers='keys', tablefmt='psql', showindex=False))
                        elif user_input == '2':
                            pass
                        elif user_input.upper() == 'B' or user_input.upper() == 'Q':
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

                    if user_input.upper() == 'B':
                        return -1
                    elif user_input.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    else:
                        return 1

                inputs = [assign_username, assign_password, assign_camp]

                while counter < len(inputs):
                    counter += inputs[counter]()

                vol_df.loc[len(vol_df.index)] = [username, '', '', '', camp, '']
                users_df.loc[len(users_df.index)] = [username, password, 'volunteer', 'TRUE', '']
                print(tabulate(users_df.tail(1), headers='keys', tablefmt='psql', showindex=False))
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
                        if type(no_of_new_users) == str and no_of_new_users.upper() == 'Q':
                            print(100*'=')
                            menu(self.functions)
                            exit()
                    except ValueError:
                        print('Your input needs to be an integer')
                        continue
                    while True:
                        print('')
                        print(tabulate(camps_df, headers='keys', tablefmt='psql', showindex=False))
                        camp = input('\nEnter camp ID: ')
                        if camp not in camps_exist:
                            print('Invalid Camp ID.')
                            continue
                        else:
                            break
                    if camp.upper() == 'B':
                        continue
                    elif type(no_of_new_users) == str and no_of_new_users.upper() == 'Q':
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
                    
                df = users_df.tail(no_of_new_users)
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
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
            if user_input.upper() == 'B' or user_input.upper() == 'Q':
                print(100*'=')
                menu(self.functions)
                exit()
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

    def admin_volunteer_commands(self):

        def print_msg_box(msg, indent=1, width=None, title=None):
            lines = msg.split('\n')
            space = " " * indent
            if not width:
                width = max(map(len, lines))
            box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
            if title:
                box += f'║{space}{title:<{width}}{space}║\n'  # title
                box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
            box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
            box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
            print(box)

        df = self.user_db.copy()
        df1 = self.vol_db.copy()
        df2 = self.camps_db.copy()
        while True:
            try:
                print_msg_box('Enter d, r or del and the volunteer username separated by space\n'
                              "Example: d Volunteer1 to deactive Volunteer1's account.\n\n"
                              '[d] - deactivate volunteer account\n'
                              '[r] - reactivate volunteer account\n'
                              '[del] delete volunteer account\n\n'
                              '[B] to go back.\n'
                              '[Q] to quit\n')
                
                print(tabulate(df[['username','role','activated']].tail(len(df)-1), headers='keys', tablefmt='psql', showindex=False))
                action_and_volunteer = input('\nInput: ')

                if action_and_volunteer.upper() == 'B' or action_and_volunteer.upper() == 'Q':
                    print(100 * '=')
                    menu(self.functions)
                    exit()
                action = action_and_volunteer.split(' ')[0].lower()
                volunteer_username = action_and_volunteer.split(' ')[1]

                if volunteer_username in df1['Username'].values:
                    index = df.index[df['username'] == volunteer_username].tolist()[0]
                    if action == 'd':
                        if df.at[index, 'activated']:
                            df.at[index, 'activated'] = False
                            df.to_csv('user_database.csv', index=False)
                            print(Fore.BLUE + f'\nAction completed.\n{volunteer_username} has been deactivated.\n')
                            print(Style.RESET_ALL)
                            continue
                        else:
                            print(Fore.RED + '\nThis user is not active.\n')
                            print(Style.RESET_ALL)
                            continue
                    elif action == 'r':
                        if df.at[index, 'activated']:
                            print(Fore.RED + '\nThis user is already active.\n')
                            print(Style.RESET_ALL)
                            continue
                        else:
                            df.at[index, 'activated'] = True
                            df.to_csv('user_database.csv', index=False)
                            print(Fore.BLUE + f'\nAction completed.\n{volunteer_username} has been reactivated.\n')
                            print(Style.RESET_ALL)
                            continue
                    elif action == 'del':
                        # subtract number of volunteers in camp_database
                        camp_id = df1[df1['Username'] == volunteer_username]['Camp ID'].values[0]
                        index_camp = df2.index[df2['Camp ID'] == camp_id].tolist()[0]
                        df2.at[index_camp, 'Number of volunteers'] = df2[df2['Camp ID'] == camp_id]["Number of volunteers"].values[0] - 1
                        df2.to_csv('camp_database.csv', index=False)
                        # delete Volunteer from volunteer_database
                        df = df.drop(index)
                        df.to_csv('user_database.csv', index=False)
                        #delete Volunteer from user_database
                        index_vol = df1.index[df1['Username'] == volunteer_username].tolist()[0]
                        df1 = df1.drop(index_vol)
                        df1.to_csv('volunteer_database.csv', index=False)

                        print(Fore.BLUE + f'\nAction completed.\n{volunteer_username} has been deleted.\n')
                        print(Style.RESET_ALL)
                    else:
                        print(Fore.RED + '\nInvalid action. Try again. \n')
                        print(Style.RESET_ALL)
                        continue

                else:
                    print(Fore.RED + '\nThere is no volunteer with this username. Try again.\n')
                    print(Style.RESET_ALL)
                    continue
            except IndexError:
                print(Fore.RED + '\nInvalid input. Try again.\n')
                print(Style.RESET_ALL)
                continue

    def write_camp(self):
        '''
        Allows admin to add a news camp to an existing emergency.
        '''
        self.quit = False
        counter = 0
        self.count_ref_vol()
        print(100*'=')
        print('\nPlease provide details of the new camp')
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
                    if country.upper() == 'B' or country.upper() == 'Q':
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
                emergencies_in_country = emergency_df.loc[emergency_df['Emergency ID'].str.contains(country_id, case=False)]
                if len(emergencies_in_country.index) >= 1:
                    print('')
                    print(tabulate(emergencies_in_country, headers='keys', tablefmt='psql', showindex=False))
                while True:
                    if len(emergencies_in_country.index) > 1:
                        emergency = input(
                            '\nPlease select which emergency you would like to assign your camp to: ')
                        if emergency.upper() == 'B' or emergency.upper() == 'Q':
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
                if emergency.upper() == 'B':
                    return -1
                elif emergency.upper() == 'Q':
                    print(100*'=')
                    menu(self.functions)
                    exit()
                else:
                    return 1

            def assign_capacity():
                global capacity
                while True:
                    capacity = input("\nEnter maximum camp capacity:")
                    if capacity.upper() == 'B' or emergency.upper() == 'Q':
                        break
                    if capacity.isdigit() == False:
                        print('Please enter an integer.')
                        continue
                    break
                if capacity.upper() == 'B':
                    return -1
                elif capacity.upper() == 'Q':
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

            print(tabulate(camps_df.tail(1), headers='keys', tablefmt='psql', showindex=False))
            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue

            if commit == 'y':
                self.camps_db = camps_df.copy()
                camps_df.to_csv('camp_database.csv', index=False)
                break
            else:
                counter = 0
                continue
        print(100*'=')

    def camp_finance(self):
        '''
        Allows admin to create meal plan for a camp.
        '''

        while True:
            counter = 0
            print(100*'=')
            camps_df = self.camps_db.copy()
            meals_df = self.meals_db.copy()
            refugee_df = self.refugee_db.copy()
            if len(meals_df['Camp ID']) != 0:
                print("\nExisting Mealplans: \n")
                print(tabulate(meals_df, headers='keys', tablefmt='psql', showindex=False))
                print('')
                
            print('\nPlease select which camp you would like to create meal plan for.')
            print('Expected Inputs:\n' +
                '\t>Camp ID\n'+
                '\t>Number of meals consumed per person\n'+
                '\t>Average price per meal [£]\n'+
                '\t>Number of days planned / Food budget [£]\n')
            print('[B] to go back')
            print('[Q] to quit\n')   
            df = camps_df.loc[camps_df['Number of refugees'] != '']
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            
            def choose_camp():
                while True:
                    global index
                    global camp_id
                    inpt = input('\nPlease select camp: ')
                    if inpt.upper() == 'B' or inpt.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    if inpt not in list(camps_df['Camp ID']):
                        print('Invalid input.')
                        continue
                    camp_id = inpt
                    if camp_id not in list(meals_df['Camp ID']):
                        meals_df.loc[len(meals_df)] = [camp_id,'','','','','','','']
                    index = meals_df.index[meals_df['Camp ID'] == camp_id].values[0]
                    return 1
            
            def assign_no_meals():
                global camp_id
                global index
                while True:
                    inpt = input('\nPlease input planned number of meals consumed per refugee: ')
                    if inpt.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    elif inpt.upper() == 'B':
                        return -1
                    try:
                        inpt = int(inpt)
                    except:
                        print('Invalid input.')
                        continue
                    no_of_refugees = refugee_df.loc[refugee_df['Camp ID'] == camp_id]['No. Of Family Members'].sum(axis=0)
                    meals_per_day = inpt * no_of_refugees
                    meals_df.loc[index, ['Meals per day']] = [meals_per_day]
                    meals_df.loc[index, ['Total number of refugees']] = [no_of_refugees]
                    return 1

            def assign_price_per_meal():
                global price_per_meal
                global index
                while True:
                    price_per_meal = input('\nPlease input average price per meal [£]: ')
                    if price_per_meal.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    elif price_per_meal.upper() == 'B':
                        return -1
                    if not price_per_meal.isdigit() and re.match(r'^-?\d+(?:\.\d+)$', price_per_meal) is None: # This check if inpt is neither integer nor float
                        print('Invalid input.')
                        continue
                    meals_df.loc[index, ['Price per meal']] = [price_per_meal]
                    return 1

            def days_or_money():
                global price_per_meal
                global camp_id
                global days
                global index
                print('\n[1] - Choose number of days planned\n'+
                        '[2] - Choose total food budget available')
                while True:
                    choice = input('\nChoose interaction: ')
                    if choice.upper() == 'Q':
                        print(100*'=')
                        menu(self.functions)
                        exit()
                    elif choice.upper() == 'B':
                        return -1
                    if choice not in ['1','2']:
                        print('Invalid input')
                        continue
                    while True:
                        days = 0
                        budget = 0
                        if choice == '1':
                            days = input('\nInput number of days: ')
                            if days.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            elif days.upper() == 'B':
                                break
                            try:
                                days = int(days)
                            except:
                                print('Invalid input.')
                                continue
                            break
                        else:
                            budget = input('\nInput your budget: ')
                            if budget.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            elif budget.upper() == 'B':
                                break
                            try:
                                budget = int(budget)
                            except:
                                print('Invalid input.')
                                continue
                            break
                    if type(days) == str or type(budget) == str:
                        if days.upper() == 'B' or budget.upper() == 'B':
                            continue
                    break
                
                if choice == '1':
                    
                    meals_per_day = meals_df['Meals per day'][index]
                    total_meals = float(days) * float(meals_per_day)
                    budget_per_day = float(price_per_meal) * float(meals_per_day)
                    total_budget = float(days) * float(budget_per_day)
                    meals_df.loc[index, ['Days']] = [days]
                    meals_df.loc[index, ['Total meals']] = [int(total_meals)]
                    meals_df.loc[index, ['Price per meal']] = [price_per_meal]
                    meals_df.loc[index, ['Budget per day']] = [budget_per_day]
                    meals_df.loc[index, ['Total budget']] = [total_budget]
                
                else:
                    
                    meals_per_day = meals_df['Meals per day'][index]
                    budget_per_day = float(price_per_meal) * float(meals_per_day)
                    days = round((float(budget) / float(budget_per_day)))
                    total_meals = float(days) * float(meals_per_day)
                    print(total_meals)
                    meals_df.loc[index, ['Days']] = [days]
                    meals_df.loc[index, ['Total meals']] = [total_meals]
                    meals_df.loc[index, ['Price per meal']] = [price_per_meal]
                    meals_df.loc[index, ['Budget per day']] = [budget_per_day]
                    meals_df.loc[index, ['Total budget']] = [budget]

                return 1

            inputs = [choose_camp, assign_no_meals, assign_price_per_meal, days_or_money]

            while counter < len(inputs):
                counter += inputs[counter]()
            
            print(tabulate(meals_df.loc[[index]], headers='keys', tablefmt='psql', showindex=False))

            while True:
                commit = input('\nCommit changes? [y]/[n] ')
                if commit == 'y' or commit == 'n':
                    break
                else:
                    print('Your input is not recognised')
                    continue

            if commit == 'y':
                self.meals_db = meals_df.copy()
                meals_df.to_csv('mealplans_database.csv', index=False)
            else:
                counter = 0
                continue

            while True:
                repeat = input('\nWould you like to create meal plan for another camp? [y]/[n] ')
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


class Volunteer(CentralFunctions):

    def __init__(self, current_user, camp_of_user):
        CentralFunctions.__init__(self)
        self.functions = {"1": {'method': self.amend_self_info,         'message': '[1] - Amend your profile info', },
                          "2": {'method': self.call_camps,              'message': '[2] - See camp info', },
                          "3": {'method': self.call_volunteers,         'message': '[3] - See information about volunteers', },
                          "4": {'method': self.create_profile,          'message': '[4] - Create refugee profile', },
                          "5": {'method': self.amend_refugee_profile,   'message': '[5] - Amend refugee profile', },
                          "6": {'method': self.call_no_of_refugees,     'message': '[6] - See information about refugees', },
                          "7": {'method': self.call_help,               'message': '\n[h] - Contacts of local relief organisations', }}
        self.current_user = current_user
        self.camp_of_user = camp_of_user

    def amend_self_info(self):
        '''
        Allows volunteer user to input their name, surname, phone number and availability.
        If system detects no lack of an input it will launch a "flowing" version, otherwise it will launch
        "selective" version of this method.
        '''
        current_name = self.vol_db[self.vol_db["Username"] == self.current_user]["First name"].values[0]
        current_second_name = self.vol_db[self.vol_db["Username"] == self.current_user]["Second name"].values[0]
        current_phone = str(self.vol_db[self.vol_db["Username"] == self.current_user]["Phone"].values[0])
        current_availability = self.vol_db[self.vol_db["Username"] == self.current_user]["Availability"].values[0]
        password = self.user_db[self.user_db["username"] == self.current_user]['password'].values[0]
        current_email = self.user_db[self.user_db["username"] == self.current_user]['email'].values[0]
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
                print('\nPlease select which information you would like to change about yourself.')
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

                print('')
                df = vol_df.loc[vol_df['Username'] == self.current_user]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                print('')
                df = users_df.loc[users_df['username'] == self.current_user, ['username', 'password', 'email']]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))

                user_input = input("\nChoose interaction: ")

                if user_input == '1':
                    print(f"Currently, your first name is set to {current_name}.")
                    while True:
                        inpt = input("\nEnter new first name: ")
                        inpt = inpt.capitalize()
                        if inpt.upper() == 'B' or inpt.upper() == 'Q':
                            break
                        elif not inpt.isalpha():
                            print("Please enter a valid name.")
                            continue
                        current_name = inpt
                        break

                elif user_input == '2':
                    print(f"Currently, your second name is set to {current_second_name}.")
                    while True:
                        inpt = input("\nEnter new second name: ")
                        inpt = inpt.capitalize()
                        if inpt.upper() == 'B' or inpt.upper() == 'Q':
                            break
                        elif not inpt.isalpha():
                            print("Please enter a valid name.")
                            continue
                        else:
                            current_second_name = inpt
                            break

                elif user_input == '3':
                    print(f"Currently, your phone number is set to +{current_phone}.")
                    while True:
                        inpt = input(
                            "\nEnter new phone number in the format +[country code](0)_______: ")
                        if inpt.upper() == 'B' or inpt.upper() == 'Q':
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
                    print(f"Currently, your availability is set to {current_availability}.")
                    while True:
                        inpt = input("\nEnter new availability: ")
                        if inpt.upper() == 'B' or inpt.upper() == 'Q':
                            break
                        elif not inpt.isnumeric():
                            print("Invalid input.")
                        elif int(inpt) > 48:
                            print("Availability exceeds maximum weekly working hours (48h).")
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
                        if inpt.upper() == 'B' or inpt.upper() == 'Q':
                            break
                        elif otp != inpt:
                            print("Please enter valid OTP.")
                        else:
                            break
                    while True:
                        inpt = input("\nType your new password: ")
                        if inpt.upper() == 'B' or inpt.upper() == 'Q':
                            break
                        elif password == inpt:
                            print("Sorry but your password can't be the same as the previous one.")
                        elif len(inpt) < 8:
                            print("Sorry but your password needs to be at least 8 characters long.")
                        else:
                            password = inpt
                            break
                        
                    print(password)

                elif user_input == '6':
                    print(f"Currently, your email is set to {current_email}.")
                    while True:
                        inpt = input("\nEnter new email: ")
                        inpt = inpt.capitalize()
                        if inpt.upper() == 'B' or inpt.upper() == 'Q':
                            break
                        elif check_email(inpt):
                            print("Please enter a valid email address.")
                            continue
                        current_email = inpt
                        break

                else:
                    print('Invalid input. Please select from the options above.')
                    continue

                if inpt.upper() == 'B':
                    continue
                elif inpt.upper() == 'Q' or user_input.upper() == 'B' or user_input.upper() == 'Q':
                    print(100*'=')
                    menu(self.functions)
                    exit()

                print(password)
                vol_df.loc[vol_df['Username'] == self.current_user] = [self.current_user, current_name, current_second_name, current_phone, self.camp_of_user, current_availability]
                users_df.loc[users_df['username'] == self.current_user, ['password', 'email']] = [password, current_email]

                print('')
                df = vol_df.loc[vol_df['Username'] == self.current_user]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                print('')
                df = users_df.loc[users_df['username'] == self.current_user, ['username', 'password', 'email']]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                # print('\n', vol_df.loc[vol_df['Username'] == self.current_user])
                # print(users_df.loc[users_df['username'] == self.current_user, ['username', 'password', 'email']])

                while True:
                    commit = input('\nCommit changes? [y]/[n] ')
                    if commit == 'y' or commit == 'n':
                        break
                    else:
                        print('Your input is not recognised')
                        continue

                if commit == 'y':
                    self.vol_db = vol_df.copy()
                    self.users_db = users_df.copy()
                    vol_df.to_csv('volunteer_database.csv', index=False)
                    users_df.to_csv('user_database.csv', index=False)
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

            df = vol_df.loc[vol_df['Username'] == self.current_user]
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            questions = ['\nEnter first name: ', '\nEnter second name: ',
                         '\nEnter phone number in the format [+[country code](0)_______]:', '\nEnter availability: ',
                         '\nEnter your email', '\nEnter your new password (over 8 characters long)']

            def go_back(questionStack):
                i = 0
                answerStack = []

                while i < len(questionStack):
                    if i == 0 or i == 1:
                        while True:
                            answer = input(questionStack[i])
                            if answer.upper() == 'B':
                                if i == 0:
                                    print(100*'=')
                                    menu(self.functions)
                                    exit()
                                answerStack.pop()
                                i -= 1
                            elif answer.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            elif answer == '':
                                answer = vol_df.iloc[vol_df.index[vol_df['Username'] == self.current_user][0], i+1]
                            elif not answer.isalpha():
                                print("Please enter a valid name.")
                                continue
                            break
                    elif i == 2:
                        while True:
                            answer = input(questionStack[i])
                            if answer.upper() == 'B':
                                if i == 0:
                                    break
                                answerStack.pop()
                                i -= 1
                            elif answer.upper() == 'Q':
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
                            if answer.upper() == 'B':
                                if i == 0:
                                    break
                                answerStack.pop()
                                i -= 1
                            elif answer.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            elif answer == '':
                                answer = current_availability
                            elif not answer.isnumeric():
                                print("Invalid input.")
                                continue
                            elif int(answer) > 48:
                                print("Availability exceeds maximum weekly working hours (48h).")
                                continue
                            break
                    elif i == 4:
                        while True:
                            answer = input(questionStack[i])
                            if answer.upper() == 'B':
                                if i == 0:
                                    break
                                answerStack.pop()
                                i -= 1
                            elif answer.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            elif answer == '':
                                answer = current_email
                            elif len(inpt) < 8:
                                print("Sorry but your password needs to be at least 8 characters long.")
                                continue
                            break
                    elif i == 5:
                        while True:
                            answer = input(questionStack[i])
                            if answer.upper() == 'B':
                                if i == 0:
                                    break
                                answerStack.pop()
                                i -= 1
                            elif answer.upper() == 'Q':
                                print(100*'=')
                                menu(self.functions)
                                exit()
                            elif answer == '':
                                answer = password
                            elif len(inpt) < 8:
                                print("Sorry but your password needs to be at least 8 characters long.")
                                continue
                            break

                    if answer.upper() == 'B':
                        continue

                    answerStack.append(answer)
                    i += 1

                return answerStack

            while True:
                answers = go_back(questions)
                vol_df.loc[vol_df['Username'] == self.current_user] = [
                    self.current_user, answers[0], answers[1], answers[2], self.camp_of_user, answers[3]]

                print('')
                df = vol_df.loc[vol_df['Username'] == self.current_user]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                print('')
                df = users_df.loc[users_df['username'] == self.current_user, ['username', 'password', 'email']]
                print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
                
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
    print('\nSESSION OVER\n')
    print(100*'=')

def login():
    if __name__ == '__main__':
        login = CentralFunctions()
        login.users_login()
        if login.current_user != 'admin':
            vol = Volunteer(login.current_user, login.camp_of_user)
            menu(vol.functions)
        else:
            adm = Admin(login.current_user, login.camp_of_user)
            menu(adm.functions)


def menu(functions):
    while True:
        print(100*'=')
        print('MAIN MENU')
        print('\nChoose an interaction by typing the corresponding number.')
        print('Example: type "1" to a'+functions['1']['message'][7:]+'.\n')
        for i in range(len(functions.keys())):
            print(functions[str(i+1)]['message'])
        print('[Q] to end session')
        print('[#] to logout')
        user_input = input('\nPlease select your interaction: ')
        if user_input.upper() == 'Q':
            session_over_message()
            exit()
        elif user_input == '#':
            print('You logged out.')
            print(100 * '=')
            login()
        elif user_input.upper() == 'H':
            user_input = list(functions.keys())[-1]
        if user_input not in functions.keys():
            print('Please select valid input.')
            continue
        print(100*'=')
        functions[user_input]['method']()

if __name__ == '__main__':
    login()
