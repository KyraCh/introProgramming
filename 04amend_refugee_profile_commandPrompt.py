import pandas as pd

pd.set_option('display.max_columns',15)

class test():
    
    def __init__(self):
        self.list_of_refugee = pd.read_csv('RefugeeList.csv')
        self.current_user = 'vol'
        self.camp_of_user = 'A1'

        self.vol_data = pd.read_csv('VolounteersData.csv').set_index('Username')
        
    def amend_refugee_profile(self):
        '''
        Interactive method which allows one to amend information about a refugee.
        '''
        list_of_refugees = self.list_of_refugee.copy()
        vol_dict = self.vol_data.to_dict(orient='index')

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
                list_of_refugees.to_csv('RefugeeList.csv')
            
            self.list_of_refugee = list_of_refugees
            break
        
if __name__ == '__main__':
    
    a = test()
    a.amend_refugee_profile()