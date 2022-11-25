import pandas as pd

class test():
    def __init__(self):
        self.user_data = None
        self.current_user = None
        self.vol_data = None
        self.camp_of_user = None
        
    def users_login(self):
        '''
        Reads (or if first time logging in creates) users_dataframe.csv.
        Creates self.user_data DataFrame. # when admin wants to call all details of all users they'd use this
        Asks the user to input the login and password credentials.
        Upon successful login will set global parameter self.current_user as either 'adm' or 'vol'.
        
        (IMPORTANT: considers existence of only one admin username)
        '''
        # part which reads/creates the user_database file
        try: 
            df = pd.read_csv('user_database.csv').set_index('username')
            df['password'] = df['password'].astype(str)
            users_dict = df.to_dict(orient='index')
            self.user_data = df
        except FileNotFoundError:
            users_dict = {'username':['admin'],'password':['111'],'role':['admin'],'activated':['TRUE']}
            df = pd.DataFrame(users_dict)
            df.set_index('username', inplace=True)
            df['password'] = df['password'].astype(str)
            df.to_csv('user_database.csv')
            users_dict = df.to_dict(orient='index')
            self.user_data = df
        except:
            print("System couldn't read your user database file.")
        pass
        
        try:
            df = pd.read_csv('VolounteersData.csv').set_index('Username')
            #df['First name '] = df['First name '].astype(str)
            vol_dict = df.to_dict(orient='index')
            self.vol_data = df
        except FileNotFoundError:
            vol_dict = {'Username':[''],'First name':[''],'Second name':[''],'Camp ID':[''],'Avability':[''],'Status':['']}
            df = pd.DataFrame(vol_dict)
            df.set_index('Username', inplace=True)
            df.to_csv('VolounteersData.csv')
            self.vol_data = df
        except:
            print("System couldn't read your volunteer database file.")
        pass
        
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
                        if a == '':
                            print('Welcome to the volunteer manu! Please ensure to add your name to our records!')
                        else:
                            print(f'Welcome back {a}!')
                        
                    self.camp_of_user = vol_dict[username]['Camp ID']
                    break
                else:
                    print('You entered incorrect password')
            break

if __name__ == '__main__':
    
    a = test()
    a.users_login()