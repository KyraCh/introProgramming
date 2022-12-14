### FIRST ROUGH OUTLINE ###
# Please nevermind the incorrect spelling; am tired

# Docstring aren't serious docstrings but rough estimates of what certain method/class is all about
# Comments set my immediate ideas on how to implement
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass
class CapacityTooSmall(Error):
    """Raised when the capacity input value is smaller than ref+vol"""
    pass

class CentralFunctions():
    
    '''
    Outlines key functions relevant to each user type. Without interactions though.
    Saves key data both through .csv files and in self.variables.
    Must be dry and designed in mind that all of these methods will be called through input-dictionary interactions.
    (input-dictionary interactions = input() function returns a str and then you put it into a dictionary to call a function)
    '''
    
    # Each method is a handfull so if we find we are repeating actions then feel free to add auxillary methods to help the main ones
    # IMPORTANT: I say .csv file a lot but that doesn't mean that the method must be reading from .csv files directly, but 
    # most likely from the local pandas dataframes formed by read_all_data()
    
    def __init__(self):
        self.user_data = None
        self.vol_data = None
        self.volunteer_data = None
        self.emergency_data = None
        self.list_of_refugee = None
        self.list_of_camps = None
        self.camps_df = None
        self.countries = None
        self.download_all_data()

        self.active_emergency = None
        self.current_user = None
        self.camp_of_user = None
        self.functions()
        pass
    
    def download_all_data(self):

        try: 
            df = pd.read_csv('user_database.csv').set_index('username')
            df['password'] = df['password'].astype(str)
            self.user_data = df
        except FileNotFoundError:
            users_dict = {'username':['admin'],'password':['111'],'role':['admin'],'activated':['TRUE']}
            df = pd.DataFrame(users_dict)
            df.set_index('username', inplace=True)
            df['password'] = df['password'].astype(str)
            df.to_csv('user_database.csv')
            self.user_data = df
        except:
            print("System couldn't read your user database file.")
            
        try:
            df = pd.read_csv('emergency_database.csv').set_index('Emergency ID')
            self.emergency_data = df
        except FileNotFoundError:
            emergency_dict = {'Emergency ID': [''], 'Location': [''], 'Description':[''],
                              'Start date': [''], 'Close date':['']}
            df = pd.DataFrame(emergency_dict)
            df.set_index('Emergency ID', inplace= True)
            df.to_csv('emergency_database.csv')
            self.emergency_data = df
        except:
            print("System couldn't read your emergency database file.")
        
        try:
            df = pd.read_csv('volunteer_database.csv').set_index('Username')
            self.volunteer_data = df
        except FileNotFoundError:
            vol_dict = {'Username': [''], 'First name': [''], 'Second name': [''], 'Camp ID': [''],
                        'Availability': ['']}
            df = pd.DataFrame(vol_dict)
            df.set_index('Username', inplace=True)
            df.to_csv('volunteer_database.csv')
            self.volunteer_data = df
        except:
            print("System couldn't read your volunteer database file.")
    
        try:
            df = pd.read_csv('VolounteersData.csv').set_index('Username')
            self.vol_data = df
        except FileNotFoundError:
            vol_dict = {'Username':[''],'First name':[''],'Second name':[''],'Camp ID':[''],'Avability':[''],'Status':['']}
            df = pd.DataFrame(vol_dict)
            df.set_index('Username', inplace=True)
            df.to_csv('VolounteersData.csv')
            self.vol_data = df
        except:
            print("System couldn't read your volunteer database file.")

        try:
            df = pd.read_csv('RefugeeList.csv')
            self.list_of_refugee = df
        except FileNotFoundError:
            list_of_refugee = {'Family ID':[''],'Lead Family Member Name':[''],'Lead Family Member Surname':[''],'Camp ID':[''],'Mental State':[''],'Physical State':[''],'No. Of Family Members':['']}
            df = pd.DataFrame(list_of_refugee)
            df.set_index('Family ID', inplace=True)
            df.to_csv('RefugeeList.csv')
            self.list_of_refugee = df
        except:
            print("System couldn't read your refugees database file.")

        try:
            df = pd.read_csv('camplist.csv')
            self.list_of_camps = df
        except FileNotFoundError:
            list_of_camps = {'Emergency ID':[''],'Type of emergency':[''],'Description':[''],'Location':[''],'Start date':[''],'Close date':[''],'Number of refugees':[''],'Camp ID':[''],'No Of Volounteers':[''],'Capacity':['']}
            df = pd.DataFrame(list_of_camps)
            df.set_index('Emergency ID', inplace=True)
            df.to_csv('camplist.csv')
            self.list_of_camps = df
        except:
            print("System couldn't read your camplist database file.")

        try:
            df = pd.read_csv("camp_database.csv") #index cannot be camp id because we cant access it
            self.camps_df = df
        except FileNotFoundError:
            camps_df = {'Camp ID':[''],'Location':[''],'Number of volunteers':[''],'Capacity':[''],'Current Emergency':[''],'Number of refugees':['']}
            df = pd.DataFrame(camps_df)
            df.set_index('Camp ID', inplace=True)
            df.to_csv('camp_database.csv')
            self.camps_df = df
        except:
            print("System couldn't read your camp database file.")

        try:
            df = list(pd.read_csv("countries.csv", index_col = 'Country name').index)
            self.countries = df
        except:
            print("System couldn't read the countries database file.")

        #counted the real values for volunteers and refugees in camp database

        for index, row in self.camps_df.iterrows():
            self.camps_df.at[index,'Number of volunteers']=len(self.vol_data[self.vol_data['Camp ID']==row['Camp ID']])
            self.camps_df.at[index,'Number of refugees']=self.list_of_refugee.loc[self.list_of_refugee['Camp ID'] == row['Camp ID'], 'No. Of Family Members'].sum()


        self.camps_df.to_csv("camp_database.csv", index=False)


    def save(self, file=None):
        '''
        Saves a relvant file when we are done inputting new data.
        I put default value as None so we have a quick trigger to save every file together. If you manage a particular file at a time then 
        what file we are saving should be specified
        '''

        pass
                  
    def call_no_refugees(self):
        '''Updated method'''
                  
        if self.current_user == 'adm':
            #prints list of emergency IDs + emergency description
            print(self.emergency_df['Description'])
            #list of emergency IDs
            list_emID = list(self.emergency_df.index)
            #list of camp IDs
            list_campID = list(self.camps_df.index)
            #list of family IDs
            list_famID = list(self.list_of_refugee.index)
            choose_emergency = input('Choose emergency by entering the associated emergency ID:')
            while choose_emergency not in list_emID:
                print('Invalid emergency ID.')
                choose_emergency = input('Choose emergency by entering the associated emergency ID:')
            choose_emergency = choose_emergency.upper()
            campID = input('Choose camp by entering the associated emergency ID:')
            while campID not in list_campID:
                print('Invalid camp ID.')
                campID = input('Choose camp by entering the associated emergency ID:')
        else:
            campID = self.camp_of_user
            choose_emergency = self.camps_df[self.camps_df.index == campID]["Current Emergency "].values[0]
        while True:
            print('Enter [1] to view current total number of refugees.')
            print('Enter [2] to view the number of refugees allocated per camp.')
            print('Enter [3] to view the number of families allocated per camp.')
            print(f'Enter [4] to view list of families allocated to your camp.')
            print('Enter [5] to view information about a specific family.')
            print('Enter [Quit] to exit.')
            user_input = input('Choose interaction:')
            if user_input == '1':
                total_ref = sum(self.camps_df[self.camps_df['Current Emergency ']==choose_emergency]['Number of refugees'])
                print(f'Current total number of refugees from {choose_emergency} is {total_ref}.')
            elif user_input == '2':
                ref_per_camp = self.camps_df[self.camps_df['Current Emergency ']==choose_emergency]['Number of refugees']
            elif user_input == '3':
                count_families = self.list_of_refugee['Camp ID'].value_counts()
                print(count_families)
            elif user_input == '4':
                if self.current_user == 'adm':
                    camp_ID = input('Enter camp ID:')
                    while camp_ID not in list_campID:
                        print('Invalid camp ID.')
                        camp_ID = input('Enter camp ID:')
                list_of_families = self.list_of_refugee[self.list_of_refugee['Camp ID']==camp_ID]
                print(list_of_families)
            elif user_input == '5':
                family = input('Enter family ID:')
                while family not in list_famID:
                    print('Invalid family ID.')
                    family = input('Enter family ID:')
                family_sum = self.list_of_refugee[self.list_of_refugee.index == family]
                while str(family_sum['Camp ID'].values[0])!= campID:
                    print('Access denied.')
                    family = input('Enter family ID:')
                    family_sum = self.list_of_refugee[self.list_of_refugee.index == family]
                print(family_sum)
            else:
                break

    def call_no_of_refugees(self):

        '''Reads the file and prints out the general list of families in a system with 
        some summary about them by sating the number of refugees, their mental and physical 
        state per each camp and gives information about each family that is assigned to certain camp.
        Secondly, the method call no of refugees now will only show you camp details of only the one that you are assigned to. 
        Unless you are admin then you can see evrything '''

        # pd.set_option('display.max_columns', 15)

  # pd.set_option('display.max_columns', 15)
        
        if self.current_user == "adm":
            countries_camps = self.list_of_camps["Emergency ID"]
            print(*countries_camps,sep='\n')
            choose_emergency = input("Choose emergency for which you want to see the summary:")
            choose_emergency= choose_emergency.upper()
        else:
            volunteer_campID = self.camp_of_user
            choose_emergency = self.list_of_camps[self.list_of_camps["Camp ID"] == volunteer_campID]["Emergency ID"].values[0]
        while True:
            print("Choose 1 if you want to see the list of all refugees for all camps")
            print("Choose 2 if you want to see the total number of refugees in chosen camp")
            print("Choose 3 if you want to see the number of families in each camp")
            print("Choose 4 if you want to see the total summary for each camp")
            print("Choose Quit if you want exit this summary")
            user_input = input("Choose interaction: ")
            if user_input == '1':
                country_refugees = self.list_of_camps[self.list_of_camps["Emergency ID"] == choose_emergency]
                print(country_refugees)
            elif user_input == "2":
                number_of_refugee = self.list_of_camps[self.list_of_camps["Emergency ID"] == choose_emergency]['Number of refugees']
                print("Number of refugee in {}: ".format(choose_emergency), *number_of_refugee, sep='\n')
            elif user_input == "3":
                camp_id = self.list_of_camps[self.list_of_camps["Emergency ID"] == choose_emergency]['Camp ID'].values[0]
                count_camps = self.list_of_refugee[self.list_of_refugee["Camp ID"] ==camp_id]['Camp ID'].value_counts()
                print("Number of families for camp {}:".format(choose_emergency))
                print(*count_camps, sep='\n')
            elif user_input == "4":
                camp_id = self.list_of_camps[self.list_of_camps["Emergency ID"] == choose_emergency]['Camp ID'].values[0]
                group_camps = self.list_of_refugee[self.list_of_refugee["Camp ID"] ==camp_id].groupby("Camp ID")
                for name, camp in group_camps:
                    print("Camp " + name + "->" + str(len(camp)) + " family/families")
                    print(camp)
            else:
                break

    def amend_refugee_profile(self):
        '''
        Interactive method which allows one to amend information about a refugee.
        '''
        list_of_refugees = self.list_of_refugee.copy()

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
            print(f'Please Choose which values you would like to ammend for family {iD}.')
            print('Input indices corresponding to value you wish to ammend separated by commas ",".')
            print('eg: "1,2" for amending "Lead Family Member Name" and "Lead Family Member Surname".\n')
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
                check = [not (i<1 or i>6) for i in ops]
                if any(i is False for i in check):
                    print('Please input valid indices\n')
                    continue
                break

            if ops == 'q':
                break
            
            for i in ops:
                change = input(f'\nPlease select new value for {list_of_refugees.columns[i]}: ')
                if change == 'q':
                    list_of_refugees = self.list_of_refugee
                    break
                if i == 3:
                    if change in [i[1:] for i in list(list_of_refugees['Family ID'])]:
                        new_index = str(max([int(i[0]) for i in list(list_of_refugees['Family ID']) if change in i])+1)
                        list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0],'Family ID'] = new_index + change
                        iD = new_index + change
                    else:
                        list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0],'Family ID'] = '1' + change
                        iD = '1' + change
                            
                list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0],list_of_refugees.columns[i]]=change
            
            if change == 'q':
                break
            
            print('\n')
            print(list_of_refugees.loc[list_of_refugees['Family ID'] == iD])
            
            if input('\nCommit changes? y/n ') == 'n':
                continue
            else:
                list_of_refugees.to_csv('RefugeeList.csv',index=False)
            
            self.list_of_refugee = list_of_refugees
            break
                  
    def call_camps(self):

                  
        '''Updated method'''
                  
        print("Choose 1 if you want to see the list of all camps")
        print("Choose 2 if you want to see the total number of camps")
        print("Choose 3 if you want to see the number of volunteers in each camp")
        print("Choose 4 if you want to see the number of refugees in each camp")
        print("Choose 5 if you want to see the capacity by camp")
        print("Choose 6 if you want to see the number of camps in each area")
        print("Choose 7 if you want to see the number of active camps")
        print("Choose 8 if you want to see the number of inactive camps")
        print("Choose 9 if you want to see the number of camps by location")
        print("Choose Quit if you want exit this summary")
        camp_summary = True
        while camp_summary:
            user_input = input('Choose interaction:')
            if user_input == '1':
                print('See camp list: \n', self.camps_df)
            elif user_input == '2':
                print("Number of camps:", len(self.camps_df.index))
            elif user_input == '3':
                print("Number of volunteers per camp: \n", self.camps_df[['Number of volunteers']].to_string())
            elif user_input == '4':
                print('Number of refugees per camp: \n', self.camps_df[['Number of refugees']].to_string())
            elif user_input=='5':
                print('Capacity per camp:\n', self.camps_df[['Capacity']].to_string())
            elif user_input == '6':
                print('Camp in each area:\n',self.camps_df['Location'].value_counts())
            elif user_input == '7':
                print('Active Camps:\n', self.camps_df[self.camps_df['Current Emergency ']!='None'].index)
            elif user_input == '8':
                print('Closed Camps:\n', self.camps_df[self.camps_df['Current Emergency ']=='None'].index)
            elif user_input == '9':
                self.camps_df['Location'].value_counts().plot(kind='bar')
                plt.title('Camps by location')
                plt.yticks(np.arange(0, 10, 1))
                plt.show()
            else:
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
        # '''

        column_headers = list(self.list_of_camps.columns.values)

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
        camp_summary = True

        while camp_summary:

            user_input = input("Choose interaction: ")
            if user_input == '1':
                print("See camp list: \n", self.list_of_camps)
            elif user_input == "2":
                print("Number of camps: ", len(self.list_of_camps.index))
            elif user_input == "3":
                print("Number of volunteers per camp: \n", self.list_of_camps[self.list_of_camps.columns[7:9]])
            elif user_input == "4":
                print("Number of refugees per camp: \n", self.list_of_camps[self.list_of_camps.columns[6:8]])
            elif user_input == "5":
                print("Capacity by camp: \n", self.list_of_camps[[column_headers[7], column_headers[9]]])
            elif user_input == "6":
                print("Camps in each area: ")
                print(self.list_of_camps[column_headers[3]].value_counts())
            elif user_input=="7":
                print("Active Camps: ", self.list_of_camps[column_headers[5]].isna().sum())
            elif user_input=="8":
                print("Closed Camps: ", self.list_of_camps[column_headers[5]].notna().sum())
            elif user_input=="9":
                self.list_of_camps[column_headers[1]].value_counts().plot(kind='bar')
                plt.title("Emergency Tipes Counted")
                plt.show()
            else:
                break
    def amend_camps(self):
        '''
        >choose camp
        >add capacity
        >delete capacity
        >
        '''
        list_of_camps = self.camps_df.copy()
        camps = list_of_camps["Camp ID"]

        print(*camps, sep='\n')

        choose_camp = input("Choose camp for which you want to edit:")
        choose_camp = choose_camp.upper()

        print(list_of_camps[list_of_camps["Camp ID"] == choose_camp])

        camp_amend = True

        while camp_amend:
            print("Choose 1 if you want to modify capacity")
            print("Choose BACK if you want to change camp")
            print("Choose Quit if you want exit")

            user_input = input("Choose interaction: ")
            if user_input == '1':
                while True:
                    try:
                        cap=int(input("State new capacity: "))
                        ind = list_of_camps[list_of_camps["Camp ID"] == choose_camp].index.values
                        if cap < int(list_of_camps[list_of_camps["Camp ID"] == choose_camp]["Number of refugees"]):
                            raise CapacityTooSmall
                        break
                    except CapacityTooSmall:
                        print("Capacity is smaller than the number of refugees, try again!")

                ind = list_of_camps[list_of_camps["Camp ID"] == choose_camp].index.values
                list_of_camps.loc[ind[0], ['Capacity']] =cap
                print(list_of_camps[list_of_camps["Camp ID"] == choose_camp])
                # writing into the file
                list_of_camps.to_csv("camp_database.csv", index=False)
            elif user_input=="BACK":
                print(*camps, sep='\n')

                choose_camp = input("Choose camp for which you want to edit:")
                choose_camp = choose_camp.upper()
                print(list_of_camps[list_of_camps["Camp ID"] == choose_camp])
            else:
                break

        self.camps_df = list_of_camps

    def call_volunteers(self):
        '''
        Reads the .csv file with volunteers and returns relevant info
            > How many volunteers
            > How many volunteers in each camp
            > Their names
        Potentially put limiters to view volunteers from one specific camp
        (Potentially add an option to curtail information to bare bones minimum(just username for example or just in one specific camp). Why?
        So we can use this method in the future for activating and deactivating volunteers in a curtailed form.
        It would be convinient to look at the list of volunteers when you type out a deletion command)
        '''
        on = True
        camp_dict = {
            '1': 'A1',
            '2': 'A2',
            '3': 'A3'
        }
        while True:
                print("\nEnter [1] to view all volunteer data\n"
                      "Enter [2] to see volunteer data by camp\n"
                      "Enter [3] to see total number of volunteers\n"
                      "Enter [4] to see number of volunteers by camp\n"
                      "Enter [5] to check if the volunteer exists\n"
                      "Enter [6] to exit")
                choose_action = input('Enter here: ')
                data = pd.read_csv('VolunteersData.csv').set_index('Username')

                if choose_action == '1':
                    print(f"\n{data}")
                elif choose_action == '2':
                    while on:
                        choose_camp = input('Choose camp. [1] A1 [2] A2 [3] A3 [4] Go back : ')
                        if choose_camp == '4':
                            break
                        try:
                            print(data[data['CampID'] == camp_dict[choose_camp].title()])
                        except KeyError:
                            print('Invalid Camp. Try again. ')
                elif choose_action == '3':
                    print(f"There are {len(data)} volunteers")
                elif choose_action == '4':
                    while on:
                        choose_camp = input('Choose camp. [1] A1 [2] A2 [3] A3 [4] Go back: ')
                        if choose_camp == '4':
                            break
                        try:
                            lst1 = [item for item in data['CampID'] if item == camp_dict[choose_camp].title()]
                            print(f"There are {len(lst1)} volunteers in {camp_dict[choose_camp]}.")
                        except KeyError:
                            print('Invalid Camp. Try again. ')
                elif choose_action == '5':
                    while on:
                        first_name = input('Enter First Name: ')
                        last_name = input('Enter Last Name: ')
                        if first_name in data['First Name'].values and last_name in data['Last Name'].values:
                            print(data[(data['First Name'] == first_name.title()) & (data['Last Name'] == last_name.title())])
                            on = False
                        else:
                            print(f'There is no volunteer with the name {first_name} {last_name}')
                            try_again = input('Would you like to try again? y/n : ')
                            if try_again == 'y':
                                continue
                            else:
                                on = False
                else:
                    break

    def users_login(self):
        '''
        Reads (or, if first time logging-in, creates) users_dataframe.csv.
        Reads (or, if first time logging-in, creates) VolounteersData.csv.
        
        Creates self.user_data DataFrame. # when admin wants to call all details of all users they'd use this
        Creates self.vol_data DataFrame which contains info on all volunteers.
        
        Asks the user to input the login and password credentials.
        
        Upon successful login will set global parameter self.current_user as either 'adm' or 'vol'.
        Upon successful login will set global parameter self.camp_of_user to either the camp of user in case
        a volunteer logged in or 'adm' in case admin logged in.
        
        (IMPORTANT: considers existence of only one admin username)
        '''

        users_dict = self.user_data.to_dict(orient='index')
        vol_dict = self.vol_data.to_dict(orient='index')
        
        # interactive part which checks credentials of the person attempting to login
        while True:
            username = input('Please input your username: ')
            if username not in self.user_data.index:
                print('Please input valid username')
                continue
            while True:
                password = input('Please input your password: ')
                if password == users_dict[username]['password']:
                    if username == 'admin':
                        self.current_user = "adm"
                    else:
                        self.current_user = 'vol'
                        
                    if self.current_user == 'adm':
                        print(f'Welcome back {username}!')
                        self.camp_of_user = 'adm'
                        break
                    else:
                        a = vol_dict[username]['First name ']
                        print(f'Welcome back {a}!')
                        
                    self.camp_of_user = vol_dict[username]['Camp ID']
                    break
                else:
                    print('You entered incorrect password')
            break

    def amend_refugee_profile(self):
        '''
        Interactive method which allows one to amend information about a refugee.
        '''
        list_of_refugees = self.list_of_refugee.copy()
        
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
            print('\n')
            print('-'*25)
            print(f'Please Choose which values you would like to ammend for family {iD}.')
            print('Input indices corresponding to value you wish to ammend separated by commas ",".')
            print('eg: "1,2" for amending "Lead Family Member Name" and "Lead Family Member Surname".\n')
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
                check = [not (i<1 or i>6) for i in ops]
                if any(i is False for i in check):
                    print('Please input valid indices\n')
                    continue
                break

            if ops == 'q':
                break
            
            for i in ops:
                change = input(f'\nPlease select new value for {list_of_refugees.columns[i]}: ')
                if change == 'q':
                    list_of_refugees = self.list_of_refugee
                    break
                if i == 3:
                    if change in [i[1:] for i in list(list_of_refugees['Family ID'])]:
                        new_index = str(max([int(i[0]) for i in list(list_of_refugees['Family ID']) if change in i])+1)
                        list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0],'Family ID'] = new_index + change
                        iD = new_index + change
                    else:
                        list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0],'Family ID'] = '1' + change
                        iD = '1' + change
                list_of_refugees.at[list_of_refugees.index[list_of_refugees['Family ID'] == iD][0],list_of_refugees.columns[i]]=change
            
            if change == 'q':
                break
            
            print('\n')
            print(list_of_refugees.loc[list_of_refugees['Family ID'] == iD])
            
            if input('\nCommit changes? y/n ') == 'n':
                continue
            
            self.list_of_refugee = list_of_refugees
            break

    def functions(self):
        '''
        creates a dictionary of all central functions to be used by admin and volunteer classes
        '''
        pass

class admin(CentralFunctions):
    '''
    Functions relevant to admin user type. Have both dry no-interaction methods and interactive methods to call them for ease of readability.
    '''

    def __init__(self):
        CentralFunctions.__init__(self)
        pass

    def admin_functions(self): # no interaction
        '''
        creates dictionary of all no-interaction methods used by admin for later interpretation by user-input methods
        '''
        pass

    def create_emergency(self, name_of_emergency, type, description, location, start_date, close_date): # no interaction
        '''
        Inputs will all be strings (except maybe dates if we will be allowed to use datetime module)
        Creates a FOLDER with a number of .csv files, all with relevant names.
        self.active_emergency = 'name_of_emergency' <-- this is done so when we close the emergency it would get archieved and all
                                                        relevant data would be saved with relevant name for ease of use.
        .csv files: <-- .csv files provide PERSISTENCE
            > dataframe with emergency properties outlined in the argument
            > dataframe with all relevant camps (at this stage empty, but only with columns)
            > dataframe with volunteers (at this stage empty, but only with columns)
            > dataframe with refugees (at this stage empty, but only with columns)
        '''
        pass

    def close_emergency(self): # no interaction
        '''
        Take the folder and all the data we accumulated in the .csv files and save under a relevant name like "closed emergency XXX"
        Clear all global and local self.variables.
        Stop the entire program (I'm not even sure how to do that from a method tbh, but we'll figure it out)

        Advantage of saving all the data under a new name is it won't possibly ever be interacted with by the rest of the program and
        we get to archive the data which is real-life-useful thing to do.
        '''
        pass
                  
    def admin_volunteer_commands(self):
        '''
        Input will be a string which will dictate what command to apply. Why not use a dictionary? Because there will be only three available
        manipulations so it would be less messy to create one big method than three small and a dictionary.
        Commands available:
            > DEACTIVATE
            > REACTIVATE
            > DELETE
        Method will then apply these commands to the volunteer .csv file
        '''
        try:
            df = pd.read_csv('user_database.csv')
            self.user_data = df
        except FileNotFoundError:
            print('There are no volunteers in our database.')
        while True:
            try:
                action_and_volunteer = input('Type the word deactivate, reactivate or delete, '
                                             'and the volunteer username '
                                             'separated by space. If you want to go back enter quit: ')

                # d, r , de
                if action_and_volunteer == 'quit':
                    break

                action = action_and_volunteer.split(' ')[0].lower()
                volunteer_username = action_and_volunteer.split(' ')[1]

                if volunteer_username in df['username'].values:
                    index = df.index[df['username'] == volunteer_username].tolist()[0]
                    if action == 'deactivate':
                        if df.at[index, 'status']:
                            df.at[index, 'status'] = False
                            df.to_csv('user_database.csv', index=False)
                            break
                        else:

                            print('This user is not active.')
                            try_again = input('Would you like to try again y/n? ')
                            if try_again == 'y':
                                continue
                            else:
                                break
                    elif action == 'reactivate':
                        if df.at[index, 'status']:
                            print('This user is already active.')
                            try_again = input('Would you like to try again y/n? ')
                            if try_again == 'y':
                                continue
                            else:
                                break
                        else:
                            df.at[index, 'status'] = True
                            df.to_csv('user_database.csv', index=False)
                            break
                    elif action == 'delete':
                        df = df.drop(index)
                        df.to_csv('user_database.csv', index=False)
                        break
                        # delete from both file and
                        # camp_list subtract by 1

                    else:
                        print('Invalid action')
                        try_again = input('Would you like to try again y/n? ')
                        if try_again == 'y':
                            continue
                        else:
                            break
                else:
                    print('There is no volunteer with that username.')
                    try_again = input('Would you like to try again y/n? ')
                    if try_again == 'y':
                        continue
                    else:
                        break
            except IndexError:
                print('Invalid input.')
                try_again = input('Would you like to try again y/n? ')
                if try_again == 'y':
                    continue
                else:
                    break


    def write_volunteer(self):

        vol_df = self.vol_data
        #print(self.user_data)
        #print(self.user_data.index)
        #print(list(self.user_data.index))
        users_exist = list(self.user_data.index)
        users_df = self.user_data

        camps_df = self.camps_df
        camps_exist = list(camps_df.index)
        
        # allows user to choose a username and password
        username = input('Enter a new username:')
        while username in users_exist:
            print('Username taken. Try another.')
            username = input('Enter a new username:')
        password = input('Set a password:')
        camp_choice = True
        while camp_choice:
        #option to view statistics about existing camps before assigning new volunteer to a camp
            print('Enter [1] to first view camp summary information.\n'
              'Enter [2] to assign camp.')
            user_input = input('Choose interaction:')
            if user_input == '1':
                print("Camp summary information: \n", camps_df)
                camp = input('Enter camp ID:')
                break
            elif user_input == '2':
                camp = input('Enter camp ID:')
                break
            else:
                print('Invalid input.')
            #checks that camp chosen by the user exists
        while camp not in camps_exist:
            print('Invalid Camp ID.')
            camp = input('Enter camp ID:')
            #add new volunteer to list of volunteers and save updated file
        try:
            new_vol = pd.DataFrame({'Username': username, 'Camp ID': camp}, index=[0])
            vol_df = pd.concat([vol_df, new_vol]).fillna(' ')
            vol_df.to_csv("volunteer_database.csv", index=False)
        #add new volunteer to list of users and save updated file
            new_account = pd.DataFrame({'username': [username], 'password': [password], 'role': ['volunteer'], 'activated': ['TRUE']}, index=[0])
            users_df = pd.concat([users_df, new_account])
            users_df.to_csv("user_database.csv", index=False)
        #change number of volunteers in camp database
            camps_df.at[camp, "Number of volunteers"] +=1
            camps_df.to_csv("camp_database.csv")
            print('Registration complete! A volunteer account has been created.')
        except:
            print('An error occured.')

    def write_camp(self):
        camps_df = self.camps_df

        #read camp id last created
        last_camp_id = camps_df.index[-1]
        # generate new camp ID (increments A1, A2,...,A99, B1, B2,...,Z99)
        if '99' not in last_camp_id:
            new_camp_id = last_camp_id[0] + str((int(last_camp_id[1]) + 1))
        else:
            new_camp_id = chr(ord(last_camp_id[0]) + 1) + '1'
        # asks user to enter camp capacity
        capacity = input("Enter maximum camp capacity:")
        while capacity.isdigit()==False:
            print('Please enter an integer.')
            capacity = input("Enter maximum camp capacity:")
        # asks user to enter location
        print(self.countries)
        country = input("Enter country name:")
        countries = self.countries
        
        while country not in countries:
            print("Please enter a valid country name.")
            country = input("Enter country name:")
        new_camp = pd.DataFrame({'Camp ID': [new_camp_id], "Location": [country], "Number of refugees": [0],
                                    "Number of volunteers": [0], "Capacity": [capacity],
                                    "Current Emergency ": [0]}).set_index(['Camp ID'])
        camps_df = pd.concat([camps_df, new_camp])
        camps_df.to_csv("camp_database.csv")
        print("Registration complete! A new camp has been created.")
        
        
    def admin_interaction(self):
        '''
        method that will require user input and then interpret it as an executable method. This one will be tricky to design because the following functions must be
        implemented:
            1 When logging in first time call methods in this order:
                > login() <-- special procedures for admins
                > create_emergency() <--  input each piece of data sequentially so it's userfriendly
                > write_camps() <--  input each piece of data sequentially so it's userfriendly
                > write_volunteers() <--  input each piece of data sequentially so it's userfriendly
            2 When logging in subsequently any method should be run regardless of order
            3 At any point the data logging should be cancelled
            4 Every time data is logged we must be write it to .csv files to prevent it from disappearing in case of system failure
            5 When a method is performed we must be able to perform another one and then do it indefinetly
            6 Have a shut off button <-- maybe separate method?
        '''
        # 1 check if there are any files in directory that have something like "EMERGENCY" in the name, if none then you are logging in first time
        #   this should lead to triggering a chain of methods to properly create an emergency
        # 2 check if there are files in the directory with code name like "EMERGENCY" in the name, if there are then read them and basically get the system up to date
        # 3 the entire thing should be in the while loop that should be engineered to loop/jump to any method when commanded. When inputting data, sequentilly, we
        #   we should have an off button like just pressing enter to cancel input, ask user if they mean to stop and then send them back to the neutral method
        #   selection menu
        # 4 Once all data is logged in the local dataframe, show it to the user for confimation, ask if they are satisfied and then if they are save() it
        # 5 smart use of while loops
        pass

class volunteer(CentralFunctions):
    '''
    Functions relevant to volunteer user type. Have both dry no-interaction methods and interactive methods to call them for ease of readability
    '''

    def __init__(self):
        CentralFunctions.__init__(self)
        pass

    def vol_functions(self): # no interaction
        '''
        creates dictionary of all no-interaction methods used by volunteer for later interpretation by user-input methods
        '''
        pass

    def edit_self_info(self):

        vol_df = self.vol_data
        current_user = 'Volunteer1'
        while True:
            print("Enter [1] to edit first name.\n"
                "Enter [2] to edit second name.\n"
                "Enter [3] to edit phone number.\n"
                "Enter [4] to edit availability.\n"
                "Enter [5] to exit.")
            user_input = input("Choose interaction:")
            if user_input == '1':
                current_name = vol_df.at[current_user,"First name "]
                print(f"Currently, your first name is set to {current_name}.")
                while True:
                    new_name = input("Enter new first name:")
                    new_name = new_name.capitalize()
                    if not new_name.isalpha():
                        print("Please enter a valid name.")
                    else:
                        break
                while True:
                    user_input = input("To confirm change of data, enter [y]:")
                    if user_input == "y":
                        vol_df.at[current_user, "First name "] = new_name
                        vol_df.to_csv("volunteer_database.csv")
                        print(f"First name has been set to {new_name}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input == '2':
                current_second_name = vol_df.at[current_user, "Second name "]
                print(f"Currently, your second name is set to {current_second_name}.")
                while True:
                    new_second_name = input("Enter new second name:")
                    new_second_name = new_second_name.capitalize()
                    if not new_second_name.isalpha():
                        print("Please enter a valid name.")
                    else:
                        break
                while True:
                    user_input = input("To confirm change of data, enter [y]:")
                    if user_input == "y":
                        vol_df.at[current_user, "Second name "] = new_second_name
                        vol_df.to_csv("volunteer_database.csv")
                        print(f"Second name has been set to {new_second_name}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input == '3':
                current_phone = vol_df.at[current_user, "Phone "]
                print(f"Currently, your phone number is set to {current_phone}.")
                while True:
                    new_phone = input("Enter new phone number in the format [44_______]:")
                    if not new_phone.isnumeric():
                        print("Please enter a valid phone number.")
                    elif len(new_phone)!= 9:
                        print("Invalid format.")
                    elif new_phone[:2]!="44":
                        print("Invalid format.")
                    else:
                        break
                while True:
                    user_input = input("To confirm change of data, enter [y]:")
                    if user_input == "y":
                        vol_df.at[current_user, "Phone "] = new_phone
                        vol_df.to_csv("volunteer_database.csv")
                        print(f"Phone number has been set to {new_phone}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input == '4':
                current_availability = vol_df.at[current_user, "Availability "]
                print(f"Currently, your availability is set to {current_availability}.")
                while True:
                    new_availability = input("Enter new availability:")
                    if not new_availability.isnumeric():
                        print("Invalid input.")
                    elif int(new_availability)>48:
                        print("Availability exceeds maximum weekly working hours (48h).")
                    else:
                        break
                while True:
                    user_input = input("To confirm change of data, enter [y]:")
                    if user_input == "y":
                        vol_df.at[current_user, "Availability "] = f"{new_availability}h"
                        vol_df.to_csv("volunteer_database.csv")
                        print(f"Availability has been set to {new_availability}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input=="5":
                quit()
            else:
                print("Invalid input. Please select from the following options.")                      
                      
    def create_profile(self): # no interaction
        '''
        Interactive method which allows to add new family to the list
        '''

        while True:
            name = input("State name of family's lead member: ")
            surname = input("State surname of the family: ")
            if name.isdigit() or surname.isdigit():
                print("You can't use number for this input. Try again ")
            else:
                break

        mental_state = input("Describe the mental state of the family: ")
        physical_state = input("Describe the physical state of the family: ")

        while True:
            try:
                no_of_members = input("Type the number of family members: ")
                break
            except ValueError:
                print("It has to be an integer")
        campID = self.camp_of_user
        count_camps = self.list_of_refugee[self.list_of_refugee["Camp ID"] == campID]['Camp ID'].value_counts().values[0]
        family_id = str(count_camps + 1)+campID

        new_family_data = pd.DataFrame({'Family ID': [family_id],'Lead Family Member Name': [name], 'Lead Family Member Surname': [surname],'Camp ID': [campID],'Mental State': [mental_state],'Physical State': [physical_state],'No. Of Family Members': [int(no_of_members)]})
        self.list_of_refugee = pd.concat([self.list_of_refugee,new_family_data])
        self.list_of_refugee.to_csv("RefugeeList.csv",index = False)
        refugee_number = self.list_of_camps[self.list_of_camps["Camp ID"] == campID]["Number of refugees"].values[0]
        new_refugee_number = refugee_number + int(no_of_members)
        index = self.list_of_camps.index[self.list_of_camps["Camp ID"] == campID].tolist()[0]
        self.list_of_camps.at[index, 'Number of refugees'] = new_refugee_number
        self.list_of_camps.to_csv("camplist.csv", index=False)
        print('Registration complete! A new family has been added to the list.')


    def vol_interaction(self):
        '''
        Puts the no interaction methods together to form an interaface that allows the volunteer to interact with the program. Largely similar to the admin analogue
            > When first logged in make the volunteer fill up the data about them.
            > Allow to call any method at any time
            > Basically have the same capabilities to interact as the admin
        '''
        pass

def execute():
    '''
    How does all of this shit work bruh
    '''
    # employ a while loop to keep the program running
    # call login method and methods made to check if there exists an emergency, then use logic to determine how to treat the admin and volunteers
    # depending on who the user is call relevant interaction method


