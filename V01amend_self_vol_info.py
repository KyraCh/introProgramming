import pandas as pd
import datetime
import os

class test():
    
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

        self.current_user = 'Volunteer1'
        self.camp_of_user = 'AU1-1'
        
        pass
    
    def download_all_data(self):
        
        dataFailure = False

        try: 
            df = pd.read_csv('user_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
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
            df = pd.read_csv('volunteer_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
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
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
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
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
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
            df = pd.read_csv('emergency_database.csv')
            df.dropna(how="all", inplace=True)
            df.fillna('',inplace=True)
            self.emergencies_db = df
        except FileNotFoundError:
            emergencies_db = {'Emergency ID':[''],'Location':[''],'Type':[''],'Description':[''],'Start date':[''],'Close date':['']}
            df = pd.DataFrame(emergencies_db)
            df.set_index('Emergency ID', inplace=True)
            df.to_csv('emergency_database.csv')
            self.emergencies_db = df
        except:
            print("System couldn't read your camplist database file.")
            dataFailure = True
        
        try:
            df = pd.read_csv("countries.csv", index_col = 'Country name')
            self.countries_db = df
        except:
            print("System couldn't read the countries database file.")
            dataFailure = True
        
        return dataFailure
    
    def amend_self_info(self):
        
        print('Please select input or update any information about you.')
        print("If you do NOT wish to change current value press ENTER during input.")
        print('Expected Inputs:\n'+
              '\t>First name\n'+
              '\t>Family name\n'+
              '\t>Phone number\n'+
              '\t>Availability\n')
        print('[B] to go back')
        print('[Q] to quit\n')

        vol_df = self.vol_db
        print(vol_df.loc[vol_df['Username']==self.current_user])
        questions = ['\nEnter new first name: ', '\nEnter new second name: ', '\nEnter new phone number in the format [44_______]:', '\nEnter new availability: ']

        def go_back(questionStack):
                i = 0
                answerStack = []

                while i < len(questionStack):
                    if i == 0 or i == 1:
                        while True:
                            answer = input(questionStack[i])
                            if answer == 'B':
                                if i == 0:
                                    break
                                answerStack.pop()
                                i -= 1
                            elif answer == 'Q':
                                break
                            elif answer == '':
                                answer = vol_df.iloc[vol_df.index[vol_df['Username'] == self.current_user][0],i+1]
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
                                break
                            elif answer == '':
                                answer = vol_df.iloc[vol_df.index[vol_df['Username'] == self.current_user][0],3]
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
                                break
                            elif answer == '':
                                answer = vol_df.iloc[vol_df.index[vol_df['Username'] == self.current_user][0],5]
                            elif not answer.isnumeric():
                                print("Invalid input.")
                                continue
                            elif int(answer) > 48:
                                print("Availability exceeds maximum weekly working hours (48h).")
                                continue
                            break                    
                    if answer == 'B':     
                        continue 
                    elif answer == 'Q':
                        exit()
                    answerStack.append(answer)
                    i += 1

                return answerStack

        while True:
            answers = go_back(questions)
            print(answers)
            vol_df.loc[vol_df['Username']==self.current_user] = [self.current_user,answers[0],answers[1],answers[2],self.camp_of_user,answers[3]]

            print('\n', vol_df.loc[vol_df['Username']==self.current_user])
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
        
tst = test()
tst.amend_self_info()