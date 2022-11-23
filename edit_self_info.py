import pandas as pd

def edit_self_info():
    try:
        vol_df = pd.read_csv("VolounteersData.csv", index_col = "Username")
        current_user = 'Volunteer1'
        while True:
            print("Enter [1] to edit first name.\n"
                  "Enter [2] to edit second name.\n"
                  "Enter [3] to edit phone number.\n"
                  "Enter [4] to edit availability.\n"
                  "Enter [5] to exit.")
            user_input = input("Choose interaction:")
            if user_input == '1':
                current_name = vol_df.at["Volunteer1","First name "]
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
                        vol_df.at["Volunteer1", "First name "] = new_name
                        vol_df.to_csv("VolounteersData.csv")
                        print(f"First name has been set to {new_name}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input == '2':
                current_second_name = vol_df.at["Volunteer1", "Second name "]
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
                        vol_df.at["Volunteer1", "Second name "] = new_second_name
                        vol_df.to_csv("VolounteersData.csv")
                        print(f"Second name has been set to {new_second_name}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input == '3':
                current_phone = vol_df.at["Volunteer1", "Phone "]
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
                        vol_df.at["Volunteer1", "Phone "] = new_phone
                        vol_df.to_csv("VolounteersData.csv")
                        print(f"Phone number has been set to {new_phone}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input == '4':
                current_availability = vol_df.at["Volunteer1", "Avability "]
                print(f"Currently, your availability is set to {current_availability}.")
                while True:
                    new_availability = input("Enter new availability:")
                    if not new_availability.isnumeric():
                        print("Invalid input.")
                    elif new_availability>48:
                        print("Availability exceeds maximum weekly working hours (48h).")
                    else:
                        break
                while True:
                    user_input = input("To confirm change of data, enter [y]:")
                    if user_input == "y":
                        vol_df.at["Volunteer1", "Avability "] = f"{new_availability}h"
                        vol_df.to_csv("VolounteersData.csv")
                        print(f"Availability has been set to {new_availability}.")
                        break
                    else:
                        print("Invalid input.")
            elif user_input=="5":
                quit()
            else:
                print("Invalid input. Please select from the following options.")
    except FileNotFoundError:
        print("System could not read your volunteer database file.")
    except:
        print("An error occured.")

edit_self_info()

