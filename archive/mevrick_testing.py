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

        self.users_login()

    def download_all_data(self):

        dataFailure = False

        try:
            df = pd.read_csv('user_database.csv').set_index('username')
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
            df = pd.read_csv('emergency_database.csv')
            self.emergencies_db = df
        except FileNotFoundError:
            emergencies_db = {'Emergency ID': [''], 'Location': [''], 'Type': [
                ''], 'Description': [''], 'Start date': [''], 'Close date': ['']}
            df = pd.DataFrame(emergencies_db)
            df.set_index('Emergency ID', inplace=True)
            self.emergencies_db = df
        except:
            print("System couldn't read your emergency database file.")
            dataFailure = True

        try:
            df = pd.read_csv('volunteer_database.csv').set_index('Username')
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
            self.camps_db = df
        except FileNotFoundError:
            camps_db = {'Camp ID': [''], 'Location': [''], 'Number of volunteers': [''], 'Capacity': [''], 'Current Emergency': [
                ''], 'Number of refugees': ['']}
            df = pd.DataFrame(camps_db)
            df.set_index('Camp ID', inplace=True)
            df.to_csv('camp_database.csv')
            self.camps_db = df
        except:
            print("System couldn't read your camplist database file.")
            dataFailure = True

        try:
            df = list(pd.read_csv("countries.csv",
                      index_col='Country name').index)
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

    # def call_no_of_refugees(self):
    #     '''Reads the file and prints out the general list of families in a system with
    #     some summary about them by sating the number of refugees, their mental and physical
    #     state per each camp and gives information about each family that is assigned to certain camp.
    #     Secondly, the method call no of refugees now will only show you camp details of only the one that you are assigned to.
    #     Unless you are admin then you can see evrything '''

    #     if self.current_user == "adm":
    #         countries_camps = self.camps_db["Emergency ID"]
    #         print(*countries_camps, sep='\n')
    #         choose_emergency = input(
    #             "Choose emergency for which you want to see the summary:")
    #         choose_emergency = choose_emergency.upper()
    #     else:
    #         volunteer_campID = self.camp_of_user
    #         choose_emergency = self.camps_db[self.camps_db["Camp ID"]
    #                                          == volunteer_campID]["Emergency ID"].values[0]
    #     while True:
    #         print("Choose 1 if you want to see the list of all refugees for all camps")
    #         print(
    #             "Choose 2 if you want to see the total number of refugees in chosen camp")
    #         print("Choose 3 if you want to see the number of families in each camp")
    #         print("Choose 4 if you want to see the total summary for each camp")
    #         print("Choose Quit if you want exit this summary")
    #         user_input = input("Choose interaction: ")
    #         if user_input == '1':
    #             country_refugees = self.camps_db[self.camps_db["Emergency ID"]
    #                                              == choose_emergency]
    #             print(country_refugees)
    #         elif user_input == "2":
    #             number_of_refugee = self.camps_db[self.camps_db["Emergency ID"]
    #                                               == choose_emergency]['Number of refugees']
    #             print("Number of refugee in {}: ".format(
    #                 choose_emergency), *number_of_refugee, sep='\n')
    #         elif user_input == "3":
    #             camp_id = self.camps_db[self.camps_db["Emergency ID"]
    #                                     == choose_emergency]['Camp ID'].values[0]
    #             count_camps = self.refugee_db[self.refugee_db["Camp ID"] == camp_id]['Camp ID'].count(
    #             )
    #             print("Number of families for camp {}:".format(choose_emergency))
    #             print(*count_camps, sep='\n')
    #         elif user_input == "4":
    #             camp_id = self.camps_db[self.camps_db["Emergency ID"]
    #                                     == choose_emergency]['Camp ID'].values[0]
    #             group_camps = self.refugee_db[self.refugee_db["Camp ID"] == camp_id].groupby(
    #                 "Camp ID")
    #             for name, camp in group_camps:
    #                 print("Camp " + name + "->" +
    #                       str(len(camp)) + " family/families")
    #                 print(camp)
    #         else:
    #             break

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

    def call_camps(self):
        '''
        Sounds fucking evil, we might need to change the name of the method XD
        Reads the .csv file with camps and returns relevant data.
            > camp list
            > How many camps
            > How many volunteers in each camp
            > How many refugees in each
            > Each camp's capacity
            >count camps in each area
            >active camps (not closed)
            >closed camps
            >bar plot emergency type
        '''

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
            # double check this --> Do you mean Location ?
            elif user_input == "6":
                print("Camps in each area: \n", self.camps_db.groupby(
                    by=self.camps_db['Location']).size())
            elif user_input == "7":
                print("Active Camps: ",
                      self.camps_db[column_headers[5]].isna().sum())
            elif user_input == "8":
                print("Closed Camps: ",
                      self.camps_db[column_headers[5]].notna().sum())
            elif user_input == "9":
                self.camps_db[column_headers[1]
                              ].value_counts().plot(kind='bar')
                # plt.title("Emergency Tipes Counted")
                # plt.show()
            else:
                break

    def users_login(self):

        users_dict = self.user_db.to_dict(orient='index')
        vol_dict = self.vol_db.to_dict(orient='index')

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

        self.current_user = 'vol'

        if username == 'admin':
            self.current_user = 'adm'
            self.camp_of_user = 'adm'
            print(f'Welcome Back admin\n')
        else:
            name = vol_dict[username]['First name']
            self.camp_of_user = vol_dict[username]['Camp ID']
            print(f'Welcome back {name}\n')

    def create_profile(self):  # no interaction
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

        refugee_number = self.camps_db[self.camps_db["Camp ID"]
                                       == self.camp_of_user]["Number of refugees"].values[0]
        new_refugee_number = refugee_number + no_of_members
        index = self.camps_db.index[self.camps_db["Camp ID"] == self.camp_of_user].tolist()[
            0]
        self.camps_db.at[index, 'Number of refugees'] = new_refugee_number
        self.camps_db.to_csv("camplist.csv", index=False)
        print('Registration complete! A new family has been added to the list.')

    def random(self):
        pass


a = CentralFunctions()
a.call_camps()
