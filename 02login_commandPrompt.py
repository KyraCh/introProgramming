import pandas as pd

class test():
    def __init__(self):
        self.user_data = None
        self.current_user = None
        
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
            self.user_data = df
        except:
            print("System couldn'd read your user data base file.")
        pass
        
        # interactive part which checks credentials of the person attempting to login
        while True:
            username = input('Please input your username: ')
            if username not in df.index:
                print('Please input valid username')
                continue
            
            while True:
                password = input('Please input your password: ')
                if password == users_dict[username]['password']:
                    print(f'Welcome back {username}!')
                    if username == 'admin':
                        self.current_user = "adm"
                    else:
                        self.current_user = 'vol'
                    break
                else:
                    print('You entered incorrect password')
            break

if __name__ == '__main__':
    
    a = test()
    a.users_login()