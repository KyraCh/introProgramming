import pandas as pd

pd.set_option('display.max_columns',15)
list_of_refugee = pd.read_csv('RefugeeList.csv')

def create_profile(self, name, no_of_relatives, medical_needs, camp):
    '''
    Family ID	Lead Family Member Name	Lead Family Member Surname	Camp ID	Mental State	Physical State	No. Of Family Members
    '''
    