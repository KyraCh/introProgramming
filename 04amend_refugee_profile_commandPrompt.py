import pandas as pd

pd.set_option('display.max_columns',15)
list_of_refugee = pd.read_csv('RefugeeList.csv')

def create_profile(self, name, no_of_relatives, medical_needs, camp):
    '''
    Family ID	Lead Family Member Name	Lead Family Member Surname	Camp ID	Mental State	Physical State	No. Of Family Members
    '''
    print('AMEND REFUGEE PROFILE')

    while True:
        iD = input('Please choose Family ID you would like to ammend: ')
        if iD not in list(list_of_refugee['Family ID']):
            print('Please enter valid Family ID')
            continue
        print(f'\nPlease Choose which values you would like to ammend for Family {iD}')
        print('-'*25)
        print('Input indices corresponding to value you wish to ammend separated by commas ","')
        print('eg: "1,2" for amending "Lead Family Member Name" and "Lead Family Member Surname"')
        print('[1] - "Lead Family Member Name"')
        print('[2] - "Lead Family Member Surname"')
        print('[3] - "Camp ID"')
        print('[4] - "Mental State"')
        print('[5] - "Physical State"')
        print('[6] - "No. Of Family Members"\n')

        while True:
            ops = input('Indices: ')
            try:
                ops = [int(i) for i in ops.split(',')]
            except:
                print('Please input valid indices')
                continue
            check = [not (i<1 or i>6) for i in ops]
            if any(i is False for i in check):
                print('Please input valid indices')
                continue
            break
        
        for i in ops:
            change = input(f'Please select new value for {list_of_refugee.columns[i]}')
            list_of_refugee.at[list_of_refugee.index[list_of_refugee['Family ID'] == iD][0],list_of_refugee.columns[i]]=change
        
        break