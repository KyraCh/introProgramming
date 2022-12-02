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

        self.current_user = None
        self.camp_of_user = None
        
        pass
    
    def download_all_data(self):
        
        dataFailure = False

        try: 
            df = pd.read_csv('user_database.csv')
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
            df = pd.read_csv('emergency_database.csv')
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
        
    def create_emergency(self,prev=None):
        '''
        Allows user to create emergency by requesting country of emergencym type of emergency, description and start date.
        Automatically assigns emergency ID and upon commit adds new emergency to emergency_database.csv 
        '''
        self.quit = False
        print('Please input information about your emergency')
        print('Expected Inputs:\n'+
              '\t>Country\n'+
              '\t>Type of emergency\n'+
              '\t>Description of your emrgency\n'+
              '\t>Start date\n')
        print('[B] to go back')
        print('[Q] to quit')
        
        while True: 
            emergency_db = self.emergencies_db.copy()
            country_dict  = self.countries_db.to_dict(orient='index')
            counter = 0
                
            # def country_select():
            #     global country
            #     while True:
            #         country = input('\nPlease select the country of emergency: ')
            #         if country in list(self.countries_db.index):
            #             break
            #         elif country == 'Q':
            #             self.quit = True
            #             break
            #         else:
            #             print('Please select valid country')
            #             continue
            #     return 1
            
            # def type_select():
            #     global type_emergency
            #     inpt = input('\nPlease enter type of emergency: ')
            #     type_emergency = inpt
            #     if inpt == 'B':
            #         return -1
            #     elif inpt == 'Q':
            #         self.quit = True
            #         return 0
            #     else:
            #         return 1
                
            # def descr_select():
            #     global description
            #     inpt = input('\nPlease briefly describe your emergency: ')
            #     description = inpt
            #     if inpt == 'B':
            #         return -1
            #     elif inpt == 'Q':
            #         self.quit = True
            #         return 0
            #     else:
            #         return 1

            # def start_select():
            #     global start_date
            #     global startDate
              
            #     while True:
            #         inpt = input('\nPlease enter start date of the emergency [YYYY-MM-DD]: ')
            #         if inpt == 'B':
            #             return -1
            #         elif inpt == 'Q':
            #             self.quit = True
            #             return 0
            #         else:
            #             try:
            #                 start_date = inpt
            #                 datetime.date.fromisoformat(start_date)
            #                 startDate = datetime.datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y") 
            #             except:
            #                 print('Please enter a day of valid format [YYYY-MM-DD]: ') 
            #                 continue
            #             return 1
                
            # inputs = [country_select, type_select, descr_select, start_select]
            
            # while counter < len(inputs):
            #     counter += inputs[counter]()
            #     if self.quit == True:
            #         break
            # if self.quit == True:
            #     break
            
            
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
                                answer = datetime.datetime.strptime(answer, "%Y-%m-%d").strftime("%d/%m/%Y") 
                                break
                            except:
                                print('Please enter a day of valid format [YYYY-MM-DD]: ') 
                                continue
                    else:
                        answer = input(questionStack[i])

                    if answer == 'B':
                        if i == 0:
                            break
                        answerStack.pop()
                        i -= 1
                        continue
                    elif answer == 'Q':
                        break

                    answerStack.append(answer)
                    i += 1

                return answerStack

            questions = ['\nPlease select the country of emergency: ', '\nPlease enter type of emergency: ', '\nPlease briefly describe your emergency: ',
                 '\nPlease enter start date of the emergency [YYYY-MM-DD]: ']
            answers = go_back(questions)
            country_code = country_dict[answers[0]]['Country code']    

            if True in list(emergency_db['Emergency ID'].str.contains(country_code, case=False)):
                new_no_index = int(emergency_db.loc[emergency_db['Emergency ID'].str.contains(country_code, case=False)].iloc[-1]['Emergency ID'][2:]) + 1
            else:
                new_no_index = 1
            emergency_id = country_code + str(new_no_index)
            
            emergency_db.loc[len(emergency_db.index)] = [emergency_id, answers[0], answers[1], answers[2], answers[3], None]
            
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
            
            
tst = test()
tst.create_emergency()