### FIRST ROUGH OUTLINE ###
# Please nevermind the incorrect spelling; am tired

# Docstring aren't serious docstrings but rough estimates of what certain method/class is all about
# Comments set my immediate ideas on how to implement
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

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
        self.user_db = None
        self.vol_db = None
        self.refugee_db = None
        self.camps_db = None
        self.countries_db = None
        self.emergencies_db = None 

        fileCheckError =  self.download_all_data()
        
        if fileCheckError:
            exit()

        # self.active_emergency = self.emergencies_db.loc[self.emergencies_db['Close date'].isnull()]
        self.current_user = None
        self.camp_of_user = None
        self.functions()
        
        pass
    
    def download_all_data(self):
        
        dataFailure = False

        try: 
            df = pd.read_csv('user_database.csv').set_index('username')
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
            df = list(pd.read_csv("countries.csv", index_col = 'Country name').index)
            self.countries_db = df
        except:
            print("System couldn't read the countries database file.")
            dataFailure = True
        
        return dataFailure
        
    def save(self, **kwargs):
        '''
        Saves a relvant file when we are done inputting new data.
        I put default value as None so we have a quick trigger to save every file together. If you manage a particular file at a time then 
        what file we are saving should be specified
        '''
        pass
    
    def call_no_of_refugees(self):

        '''Reads the file and prints out the general list of families in a system with 
        some summary about them by sating the number of refugees, their mental and physical 
        state per each camp and gives information about each family that is assigned to certain camp.
        Secondly, the method call no of refugees now will only show you camp details of only the one that you are assigned to. 
        Unless you are admin then you can see evrything '''


        
        if self.current_user == "adm":
            countries_camps = self.camps_db["Emergency ID"]
            print(*countries_camps,sep='\n')
            choose_emergency = input("Choose emergency for which you want to see the summary:")
            choose_emergency= choose_emergency.upper()
        else:
            volunteer_campID = self.camp_of_user
            choose_emergency = self.camps_db[self.camps_db["Camp ID"] == volunteer_campID]["Emergency ID"].values[0]
        while True:
            print("Choose 1 if you want to see the list of all refugees for all camps")
            print("Choose 2 if you want to see the total number of refugees in chosen camp")
            print("Choose 3 if you want to see the number of families in each camp")
            print("Choose 4 if you want to see the total summary for each camp")
            print("Choose Quit if you want exit this summary")
            user_input = input("Choose interaction: ")
            if user_input == '1':
                country_refugees = self.camps_db[self.camps_db["Emergency ID"] == choose_emergency]
                print(country_refugees)
            elif user_input == "2":
                number_of_refugee = self.camps_db[self.camps_db["Emergency ID"] == choose_emergency]['Number of refugees']
                print("Number of refugee in {}: ".format(choose_emergency), *number_of_refugee, sep='\n')
            elif user_input == "3":
                camp_id = self.camps_db[self.camps_db["Emergency ID"] == choose_emergency]['Camp ID'].values[0]
                count_camps = self.refugee_db[self.refugee_db["Camp ID"] ==camp_id]['Camp ID'].count()
                print("Number of families for camp {}:".format(choose_emergency))
                print(*count_camps, sep='\n')
            elif user_input == "4":
                camp_id = self.camps_db[self.camps_db["Emergency ID"] == choose_emergency]['Camp ID'].values[0]
                group_camps = self.refugee_db[self.refugee_db["Camp ID"] ==camp_id].groupby("Camp ID")
                for name, camp in group_camps:
                    print("Camp " + name + "->" + str(len(camp)) + " family/families")
                    print(camp)
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
                    list_of_refugees = self.refugee_db
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
            
            self.refugee_db = list_of_refugees
            break

    def call_camps(self, prev):
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

        column_headers = list(self.camps_db.columns.values)

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
                print("Number of volunteers per camp: \n", self.camps_db[self.camps_db.columns[7:9]])
            elif user_input == "4":
                print("Number of refugees per camp: \n", self.camps_db[self.camps_db.columns[6:8]])
            elif user_input == "5":
                print("Capacity by camp: \n", self.camps_db[[column_headers[7], column_headers[9]]])
            elif user_input == "6":
                print("Camps in each area: ")
                print(self.camps_db[column_headers[3]].value_counts())
            elif user_input=="7":
                print("Active Camps: ", self.camps_db[column_headers[5]].isna().sum())
            elif user_input=="8":
                print("Closed Camps: ", self.camps_db[column_headers[5]].notna().sum())
            elif user_input=="9":
                self.camps_db[column_headers[1]].value_counts().plot(kind='bar')
                plt.title("Emergency Tipes Counted")
                plt.show()
            else:
                break

    def users_login(self):

        users_dict = self.user_db.to_dict(orient='index')
        vol_dict = self.vol_db.to_dict(orient='index')
        
        while True:
            username = input('Please input your username: ')
            password = input('Please input your password: ')

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
            print(f'Welcome Back admin')
        else:
            name = vol_dict[username]['First name']
            self.camp_of_user = vol_dict[username]['Camp ID']
            print(f'Welcome back {name}')

    def create_profile(self): # no interaction
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
                no_of_members = int(input("Type the number of family members: "))
                break
            except ValueError:
                print("It has to be an integer")
                continue

        campID = self.camp_of_user
        count_camps = self.refugee_db[self.refugee_db["Camp ID"] == campID]['Camp ID'].value_counts().values[0]
        family_id = str(count_camps + 1) + campID

        # new_family_data = pd.DataFrame({'Family ID': [family_id],'Lead Family Member Name': [name], 'Lead Family Member Surname': [surname],'Camp ID': [campID],'Mental State': [mental_state],'Physical State': [physical_state],'No. Of Family Members': [int(no_of_members)]})
        # self.refugee_db = pd.concat([self.refugee_db,new_family_data])
        self.refugee_db.loc[len(self.refugee_db)] = [family_id, name, surname, campID, mental_state, physical_state, no_of_members]
        self.refugee_db.to_csv("refugee_db.csv",index = False)
        refugee_number = self.camps_db[self.camps_db["Camp ID"] == campID]["Number of refugees"].values[0]
        new_refugee_number = refugee_number + no_of_members
        index = self.camps_db.index[self.camps_db["Camp ID"] == campID].tolist()[0]
        self.camps_db.at[index, 'Number of refugees'] = new_refugee_number
        self.camps_db.to_csv("camplist.csv", index=False)
        print('Registration complete! A new family has been added to the list.')

class Admin(CentralFunctions):
    '''
    Functions relevant to admin user type. Have both dry no-interaction methods and interactive methods to call them for ease of readability.
    '''

    def __init__(self):
        CentralFunctions.__init__(self)
        pass

    def create_emergency(current_user, type_emergency, description, country, start_date):
        #these are here if you want to define them with self.
        current_user = current_user
        start_date = start_date
        #initialising empty variables.
        country_code = ''
        emergency_id = ''
        #checking if the user is admin as is the only one who can create emergency.
        if current_user != "adm":
            return "Only admin has access to create emergency."
        try:
            #checks if the country exists in the csv file with all the country codes.
            df1 = pd.read_csv('countries.csv', encoding='latin-1')
            for index in df1.index:
                if df1['Country name'][index] == country:
                    country_code = df1['Country code'][index]
                    break
            #after searching, if country code is still empty means it's not in the csv file, so something wrong happened.
            if country_code == '':
                return "False country name"
            else:
                #modifying date to the appropriate format with as DD/MM/YYYY.
                datetime.date.fromisoformat(start_date)
                startDate = datetime.datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                #getting the file.
                file = 'camplist.csv'
                #readind data inside csv file and turning them to a panda dataframe.
                df2 = pd.read_csv(file, encoding='latin-1')
                #checking that the file is in .csv form.
                file_extension = os.path.splitext("camplist.csv")[-1].lower()
                if file_extension == '.csv':
                    #assigning emergency id, which is adding the country code with an auto-incremented number.
                    for index in df2.index[::-1]:
                        if (df2['Emergency ID'][index])[:2] == country_code:
                            emergency_id = country_code + str(int((df2['Emergency ID'][index][2:]))+1)
                            break
                    if emergency_id == '':
                        emergency_id = country_code + '1'
                    #adding data to pandas and then saving them in the csv file.
                    new_entry = {'Emergency ID': emergency_id, 'Type of emergency': type_emergency,
                                'Description': description, 'Location': country, 'Start date': startDate}
                    df3 = df2.append(new_entry, ignore_index=True)
                    df3.to_csv('camplist.csv', index=False)
                else:
                    #procedure if the file exists with the same name but has a different format other than csv.
                    #renaming the existing file so we can create a new one with the name camplist.csv as we want.
                    new_name = 'camplist_old'
                    os.rename(file, new_name+file_extension)
                    f = open("camplist.csv", "w")
                    #creating emergency ID, adding data to pandas and then saving them in the csv file.
                    emergency_id = country_code + '1'
                    first_entry = {'Emergency ID': [emergency_id], 'Type of emergency': [type_emergency],
                                'Description': [description], 'Location': [country], 'Start date': [startDate],
                                'Close date': [''], 'Number of refugees': [''], 'Camp ID': [''],
                                'No of Volunteers': [''], 'Capacity': ['']}
                    df4 = pd.DataFrame(first_entry)
                    df4.to_csv('camplist.csv', index=False)
                    f.close()
        except FileNotFoundError:
            #handling the case that file doesn't exist and then following the same procedure.
            f = open("camplist.csv", "w")
            emergency_id = country_code+'1'
            first_entry = {'Emergency ID': [emergency_id], 'Type of emergency': [type_emergency],
                        'Description': [description], 'Location': [country], 'Start date': [startDate],
                        'Close date': [''], 'Number of refugees': [''], 'Camp ID': [''], 'No of Volunteers': [''],
                        'Capacity': ['']}
            df5 = pd.DataFrame(first_entry)
            df5.to_csv('camplist.csv', index=False)
            f.close()
        except ValueError:
            #handling with the case that date is inserted in a form different to the required.
            return "Please enter a valid start date in the form YYYY-MM-DD."
        except TypeError:
            #handling with the case that some of the data are not entered as a string form.
            return "All fields should be entered as a string, even start date."

    def close_emergency(current_user, emergency_id, close_date):
        #selfemergency_id = emergency_id
        #self.close_date = close_date
        # checking if the user is admin as is the only one who can close emergency.
        if current_user != "adm":
            return "Only admin has access to create emergency."
        try:
            # modifying date to the appropriate format with as DD/MM/YYYY.
            datetime.date.fromisoformat(close_date)
            closeDate = datetime.datetime.strptime(close_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            # readind data inside csv file and turning them to a panda dataframe.
            df1 = pd.read_csv('camplist.csv', encoding='latin-1')
            #looping through the dataframe.
            for index in df1.index:
                #checking if the emergency entered exists by checking the emergency ID.
                if df1['Emergency ID'].loc[df1.index][index] == emergency_id:
                    #checking that close date is not earlier than start date.
                    if df1['Start date'].loc[df1.index][index] <= closeDate:
                        #add the close date to the pandas dataframe.
                        df1.loc[index, ['Close date']] = [closeDate]
                        #save the panda dataframe to the csv file.
                        df1.to_csv('camplist.csv', index=False)
                        return "Emergency was successfully closed."
                    else:
                        # handling with the case that close date is earlier than start date.
                        return "Close date shouldn't be earlier than start date"
            return "Emergency not found. Please enter a new existing emergency."
        except FileNotFoundError:
            #handling with the case that file was not found, which means that it was never created as there is no existing
            #emergency going on.
            return "No active emergencies right now."
        except ValueError:
            # handling with the case that date is inserted in a form different to the required.
            return "Please enter a valid start date in the form YYYY-MM-DD."
        except TypeError:
            # handling with the case that some of the data are not entered as a string form.
            return "All fields should be entered as a string, even start date."

    def amend_camps(self):
        '''
        >choose camp
        >add capacity
        >delete capacity
        >
        '''
        list_of_camps = self.list_of_camps.copy()
        camps = list_of_camps["Emergency ID"]

        print(*camps, sep='\n')

        choose_emergency = input("Choose emergency for which you want to edit:")
        choose_emergency = choose_emergency.upper()

        print(list_of_camps[list_of_camps["Emergency ID"] == choose_emergency])

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
                        ind = list_of_camps[list_of_camps["Emergency ID"] == choose_emergency].index.values
                        if cap < int(list_of_camps[list_of_camps["Emergency ID"] == choose_emergency]["Number of refugees"]):
                            raise CapacityTooSmall
                        break
                    except CapacityTooSmall:
                        print("Capacity is smaller than the number of refugees, try again!")

                ind = list_of_camps[list_of_camps["Emergency ID"] == choose_emergency].index.values
                list_of_camps.loc[ind[0], ['Capacity']] =cap
                print(list_of_camps[list_of_camps["Emergency ID"] == choose_emergency])
                # writing into the file
                list_of_camps.to_csv("camplist.csv", index=False)
            elif user_input=="BACK":
                print(*camps, sep='\n')

                choose_emergency = input("Choose emergency for which you want to edit:")
                choose_emergency = choose_emergency.upper()
                print(list_of_camps[list_of_camps["Emergency ID"] == choose_emergency])
            else:
                break

        self.list_of_camps = list_of_camps

    #def call_volunteers(self):
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

class Volunteer(CentralFunctions):
    '''
    Functions relevant to volunteer user type. Have both dry no-interaction methods and interactive methods to call them for ease of readability
    '''

    def __init__(self):
        CentralFunctions.__init__(self)
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
                      
a = CentralFunctions()


    # employ a while loop to keep the program running
    # call login method and methods made to check if there exists an emergency, then use logic to determine how to treat the admin and volunteers
    # depending on who the user is call relevant interaction method
