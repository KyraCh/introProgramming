import pandas as pd
import datetime
import os
import smtplib
import random
from email.message import EmailMessage
import ssl

class test():
    
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

        self.current_user = 'Volunteer1'
        self.camp_of_user = 'AU1-1'
        
        self.functions = 'dummy'

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
    
    def amend_self_info(self):
        '''
        Allows volunteer user to input their name, surname, phone number and availability.
        '''
        if '' not in list(self.vol_db.loc[self.vol_db['Username']==self.current_user]):
        
            while True:
                print(100 * '=')
                print('Please select which information you would like to change about yourself.')
                print('Input a digit to change the correpsonding piece of information.')
                print('E.g. input "1" to change your first name.\n' +
                        '[1] - First name\n' +
                        '[2] - Family name\n' +
                        '[3] - Phone number\n' +
                        '[4] - Availability\n' +
                        '[5] - Change password\n')
                print('[B] to go back')
                print('[Q] to quit')
                
                current_name = self.vol_db[self.vol_db["Username"] == self.current_user]["First name"].values[0]
                current_second_name = self.vol_db[self.vol_db["Username"] == self.current_user]["Second name"].values[0]
                current_phone = str(self.vol_db[self.vol_db["Username"] == self.current_user]["Phone"].values[0])
                current_availability = self.vol_db[self.vol_db["Username"] == self.current_user]["Availability"].values[0]
                password = self.user_db[self.user_db["username"] == self.current_user]['password'].values[0]
                vol_df = self.vol_db
                
                user_input = input("\nChoose interaction: ")
                if user_input == '1':
                    print(f"Currently, your first name is set to {current_name}.")
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
                    print(f"Currently, your second name is set to {current_second_name}.")
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
                    print(f"Currently, your phone number is set to +{current_phone}.")
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
                    print(f"Currently, your availability is set to {current_availability}.")
                    while True:
                        inpt = input("\nEnter new availability: ")
                        if inpt == 'B' or inpt == 'Q':
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
                    otp = ''.join([str(random.randint(0, 9)) for x in range(4)])
                    email_sender = "hemsystem1@gmail.com"
                    email_password = "asbwtshlldlaalld"
                    email_receiver = self.user_db[self.user_db["username"] == self.current_user]['email'].values[0]

                    subject = "OTP to reset password"
                    body = """Yours OTP to reset password is: {}""".format(str(otp))
                    mail = EmailMessage()
                    mail["From"] = email_sender
                    mail["To"] = email_receiver
                    mail["Subject"] = subject
                    mail.set_content(body)
                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, mail.as_string())
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
                            print("Sorry but your password can't be the same as the previous one.")
                        elif len(inpt) < 8:
                            print("Sorry but your password needs to be at least 8 characters long.")
                        else:
                            password = inpt
                            break

                else:
                    print('Please enter a valid interaction.')
                    continue
                
                if inpt == 'B':
                    continue
                elif inpt == 'Q' or user_input == 'B' or user_input == 'Q':
                    print(100*'=')
                    menu(self.functions)
                    exit()

                vol_df.loc[vol_df['Username']==self.current_user] = [self.current_user, current_name, current_second_name, current_phone, self.camp_of_user, current_availability]
                print('')
                print(vol_df.loc[vol_df['Username']==self.current_user])
                
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

def menu(a):
    print('\nYou are in menu now!\n')    
       
tst = test()
tst.amend_self_info()