import pandas as pd
def write_volunteer():
    try:
        #read user database file
        users_df = pd.read_csv("user_database.csv")
        #read list of existing usernames
        users_exist = list(users_df['username'])
    except FileNotFoundError:
        print('System could not read your user database file.')
    except:
        print('An error occured.')
    try:
        #read volunteer database file
        vol_df = pd.read_csv("VolounteersData.csv", dtype = str)
    except FileNotFoundError:
        print('System could not read your volunteer database file.')
    except:
        print('An error occured.')
    try:
        #read camp summary information
        camps_df = pd.read_csv("camp_database.csv", index_col = 'Camp ID')
        #read list of existing camps
        camps_exist = list(camps_df.index)
    except FileNotFoundError:
        print('System could not read your camp database file.')
    except:
        print('An error occured.')
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
        vol_df.to_csv("VolounteersData.csv", index=False)
    #add new volunteer to list of users and save updated file
        new_account = pd.DataFrame({'username': [username], 'password': [password], 'role': ['volunteer'], 'activated': ['TRUE']}).set_index(['username'])
        users_df = pd.concat([users_df, new_account])
        users_df.to_csv("user_database.csv")
    #change number of volunteers in camp database
        camps_df.at[camp, "Number of volunteers"] +=1
        camps_df.to_csv("camp_database.csv")
        print('Registration complete! A volunteer account has been created.')
    except:
        print('An error occured.')

write_volunteer()
