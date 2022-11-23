import pandas as pd
def write_camp():
    try:
        camps_df = pd.read_csv("camp_database.csv", index_col='Camp ID')
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
        country = input("Enter country name:")
        try:
            countries = list(pd.read_csv("country_codes.csv")["Country"])
            while country not in countries:
                print("Please enter a valid country name.")
                country = input("Enter country name:")
            new_camp = pd.DataFrame({'Camp ID': [new_camp_id], "Location": [country], "Number of refugees": [0],
                                         "Number of volunteers": [0], "Capacity": [capacity],
                                         "Current Emergency ": [0]}).set_index(['Camp ID'])
            camps_df = pd.concat([camps_df, new_camp])
            camps_df.to_csv("camp_database.csv")
        except FileNotFoundError:
            print("System could not read your country code file.")
        except:
            print('An error occured.')
    except FileNotFoundError:
        print(('System could not read your camp database file.'))
    except:
        print('An error occured.')

write_camp()




