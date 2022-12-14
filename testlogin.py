def users_login(self):
    users_dict = self.user_db.copy().set_index('username').to_dict(orient='index')
    vol_dict = self.vol_db.copy().set_index('Username').to_dict(orient='index')

    while True:
        username = input('Please input your username: ').strip()
        password = input('Please input your password: ').strip()

        if username not in users_dict:
            print('Username is incorrect.')
        elif password != users_dict[username]['password']:
            print('Password is incorrect.')
        elif not users_dict[username]['activated']:
            print('Account not activated. Please contact your admin.')
        else:
            break

    self.current_user = username

    if username == 'admin':
        self.current_user = 'adm'
        self.camp_of_user = 'adm'
        print(f'Welcome Back admin\n')
    else:
        name = vol_dict[username]['First name']
        self.camp_of_user = vol_dict[username]['Camp ID']
        print(f'Welcome back {name}\n')

        user_role = self.user_db[self.user_db['username'] == self.current_user]['role'].values[0]
        if user_role == 'volunteer':
            # index = self.user_db.index[self.user_db['username'] == self.current_user].tolist()[0]
            self.user_db.loc[self.user_db["username"] == self.current_user, 'activated'] = False
            self.user_db.to_csv('user_database.csv', index=False)
            print("Your account was deactivated. Please contact admin")
            break
    exit()
    #         deactiavted = "False"
    #         self.user_db.loc[self.user_db["username"] == self.current_user, 'activated'] = deactiavted
    #         self.user_db.to_csv("user_database.csv",index=False)
    #         print("Your account was deactivated. Please contact admin")
    #     exit()




    def create_profile(self):
        '''
        Interactive method which allows to add new family to the list
        '''
        while True:
            print('[Q] to go back to main menu')
            name = input("State name of family's lead member: ")
            if name == "q" or name == "Q":
                print(100 * '=')
                menu(self.functions)
                exit()
            while True:
                print('[B] to go back to main menu')
                surname = input("State surname of the family: ")
                if surname == "b" or surname == "B":
                    break
                if not name.isalpha() or not surname.isalpha():
                    print("You can't use numbers for this input. Try again ")
                while True:
                    print('[B] to go back to main menu')
                    mental_state = input(
                        "Describe the mental state of the family: ")
                    if mental_state == "b" or mental_state == "B":
                        break
                    while True:
                        physical_state = input(
                            "Describe the physical state of the family: ")
                        if physical_state == "b" or physical_state == "B":
                            break
                        while True:
                            print('[Q] to go back to main menu')
                            no_of_members = (
                                input("Type the number of family members: "))
                            if no_of_members == "b" or no_of_members == "B":
                                break
                            try:
                                no_of_members = int(no_of_members)

                            except ValueError:
                                print("It has to be an integer")
                                continue
                            if self.current_user == 'admin':
                                emergency_options = self.emergencies_db["Emergency ID"]
                                print(*emergency_options, sep='\n')
                                emergency_list = self.emergencies_db["Emergency ID"].tolist()
                                while True:
                                    print('[B] to go back to main menu')
                                    emergency_id = input("Choose emergency: ")
                                    if emergency_id == 'b' or emergency_id == "B":
                                        break
                                    elif emergency_id not in emergency_list:
                                        print("Invalid input for emergency")
                                    camp_id = self.camps_db.loc[self.camps_db['Camp ID'].str.contains(emergency_id, case=False)]['Camp ID']
                                    camp_id_list = camp_id.tolist()
                                    print(*set(camp_id), sep='\n')
                                    while True:
                                        print('[B] to go back to main menu')
                                        if len(camp_id_list) ==0:
                                            print("Chosen emergency doesn't have camp yet. You need to create one first before assigining family to it ")
                                            print(100 * '=')
                                            menu(self.functions)
                                            exit()
                                        else:
                                            camp_choice = input(
                                                "Choose a camp to which you want to assign family: ")
                                            if camp_choice not in camp_id_list:
                                                print(
                                                    "You have to choose from a list of available camps!")
                                            elif camp_choice == "b" or camp_choice == "B":
                                                break

                                        family_count = len(self.refugee_db.loc[self.refugee_db['Camp ID'].str.contains(
                                            camp_choice, case=False)]) + 1
                                        family_id = str(
                                            family_count) + camp_choice
                                        self.refugee_db.loc[len(self.refugee_db)] = [family_id, name, surname, camp_choice,
                                                                                     mental_state, physical_state,
                                                                                     no_of_members]
                                        self.refugee_db.to_csv(
                                            "refugee_db.csv", index=False)
                                        self.save(self.refugee_db,
                                                  'refugee_database.csv')
                                        print("New refugee family was created")
                                        print(100 * '=')
                                        menu(self.functions)
                                        exit()
                            else:
                                camp_choice = self.vol_db[self.vol_db['Camp ID']
                                                          == self.camp_of_user]['Camp ID'].values[0]
                                family_count = len(self.refugee_db.loc[self.refugee_db['Camp ID'].str.contains(
                                    camp_choice, case=False)]) + 1
                                family_id = str(family_count) + camp_choice

                                self.refugee_db.loc[len(self.refugee_db)] = [
                                    family_id, name, surname, camp_choice, mental_state, physical_state, no_of_members]
                                self.refugee_db.to_csv(
                                    "refugee_db.csv", index=False)
                                self.save(self.refugee_db,
                                          'refugee_database.csv')
                                print("New refugee family was created")
                                print(100 * '=')
                                menu(self.functions)
                                exit()

                                def amend_self_info(self):
                                    '''
                                    Allows volunteer user to input their name, surname, phone number and availability.
                                    If system detects no lack of an input it will launch a "flowing" version, otherwise it will launch
                                    "selective" version of this method.
                                    '''
                                    current_name = self.vol_db[self.vol_db["Username"]
                                                               == self.current_user]["First name"].values[0]
                                    current_second_name = self.vol_db[self.vol_db["Username"]
                                                                      == self.current_user]["Second name"].values[0]
                                    current_phone = str(
                                        self.vol_db[self.vol_db["Username"] == self.current_user]["Phone"].values[0])
                                    current_availability = self.vol_db[self.vol_db["Username"]
                                                                       == self.current_user]["Availability"].values[0]
                                    password = self.user_db[self.user_db["username"]
                                                            == self.current_user]['password'].values[0]
                                    current_email = self.user_db[self.user_db["username"]
                                                                 == self.current_user]['email'].values[0]
                                    vol_df = self.vol_db.copy()
                                    users_df = self.user_db.copy()

                                    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

                                    def check_email(email):
                                        if (re.search(regex, email)):
                                            return True
                                        else:
                                            return False

                                    if '' not in list(self.vol_db.loc[self.vol_db['Username'] == self.current_user]):

                                        while True:
                                            print(100 * '=')
                                            print(
                                                'Please select which information you would like to change about yourself.')
                                            print('Input a digit to change the correpsonding piece of information.')
                                            print('E.g. input "1" to change your first name.\n' +
                                                  '[1] - First name\n' +
                                                  '[2] - Family name\n' +
                                                  '[3] - Phone number\n' +
                                                  '[4] - Availability\n' +
                                                  '[5] - Change password\n' +
                                                  '[6] - Change email')
                                            print('\n[B] to go back')
                                            print('[Q] to quit')

                                            user_input = input("\nChoose interaction: ")

                                            if user_input == '1':
                                                print(
                                                    f"Currently, your first name is set to {current_name}.")
                                                while True:
                                                    inpt = input("\nEnter new first name: ")
                                                    inpt = inpt.capitalize()
                                                    if inpt == 'B' or inpt == 'Q':
                                                        break
                                                    elif not inpt.isalpha():
                                                        print("Please enter a valid name.")
                                                        continue
                                                    current_name = inpt
                                                    break

                                            elif user_input == '2':
                                                print(
                                                    f"Currently, your second name is set to {current_second_name}.")
                                                while True:
                                                    inpt = input("\nEnter new second name: ")
                                                    inpt = inpt.capitalize()
                                                    if inpt == 'B' or inpt == 'Q':
                                                        break
                                                    elif not inpt.isalpha():
                                                        print("Please enter a valid name.")
                                                        continue
                                                    else:
                                                        current_second_name = inpt
                                                        break

                                            elif user_input == '3':
                                                print(
                                                    f"Currently, your phone number is set to +{current_phone}.")
                                                while True:
                                                    inpt = input(
                                                        "\nEnter new phone number in the format +44(0)_______: ")
                                                    if inpt == 'B' or inpt == 'Q':
                                                        break
                                                    elif not inpt.isnumeric():
                                                        print("Please enter a valid phone number.")
                                                        continue
                                                    elif len(inpt) != 10:
                                                        print("Invalid format.")
                                                        continue
                                                    else:
                                                        current_phone = inpt
                                                        break

                                            elif user_input == '4':
                                                print(
                                                    f"Currently, your availability is set to {current_availability}.")
                                                while True:
                                                    inpt = input("\nEnter new availability: ")
                                                    if inpt == 'B' or inpt == 'Q':
                                                        break
                                                    elif not inpt.isnumeric():
                                                        print("Invalid input.")
                                                    elif int(inpt) > 48:
                                                        print(
                                                            "Availability exceeds maximum weekly working hours (48h).")
                                                    else:
                                                        current_availability = inpt
                                                        break

                                            elif user_input == '5':
                                                print("Email with OTP to reset password was sent to you")
                                                otp = ''.join([str(random.randint(0, 9))
                                                               for x in range(4)])
                                                email_sender = "hemsystem1@gmail.com"
                                                email_password = "asbwtshlldlaalld"
                                                email_receiver = self.user_db[self.user_db["username"]
                                                                              == self.current_user]['email'].values[0]

                                                subject = "OTP to reset password"
                                                body = """Yours OTP to reset password is: {}""".format(
                                                    str(otp))
                                                mail = EmailMessage()
                                                mail["From"] = email_sender
                                                mail["To"] = email_receiver
                                                mail["Subject"] = subject
                                                mail.set_content(body)
                                                context = ssl.create_default_context()

                                                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                                    smtp.login(email_sender, email_password)
                                                    smtp.sendmail(
                                                        email_sender, email_receiver, mail.as_string())
                                                while True:
                                                    inpt = input("\nInput here the OTP: ")
                                                    if inpt == 'B' or inpt == 'Q':
                                                        break
                                                    elif otp != inpt:
                                                        print("Please enter valid OTP.")
                                                    else:
                                                        break
                                                while True:
                                                    inpt = input("\nType your new password: ")
                                                    if inpt == 'B' or inpt == 'Q':
                                                        break
                                                    elif password == inpt:
                                                        print(
                                                            "Sorry but your password can't be the same as the previous one.")
                                                    elif len(inpt) < 8:
                                                        print(
                                                            "Sorry but your password needs to be at least 8 characters long.")
                                                    else:
                                                        password = inpt
                                                        break

                                            if user_input == '6':
                                                print(f"Currently, your email is set to {current_email}.")
                                                while True:
                                                    inpt = input("\nEnter new email: ")
                                                    inpt = inpt.capitalize()
                                                    if inpt == 'B' or inpt == 'Q':
                                                        break
                                                    elif check_email(inpt):
                                                        print("Please enter a valid email address.")
                                                        continue
                                                    current_email = inpt
                                                    break

                                            else:
                                                print('Invalid input. Please select from the options above.')
                                                continue

                                            if inpt == 'B':
                                                continue
                                            elif inpt == 'Q' or user_input == 'B' or user_input == 'Q':
                                                print(100 * '=')
                                                menu(self.functions)
                                                exit()

                                            vol_df.loc[vol_df['Username'] == self.current_user] = [self.current_user,
                                                                                                   current_name,
                                                                                                   current_second_name,
                                                                                                   current_phone,
                                                                                                   self.camp_of_user,
                                                                                                   current_availability]
                                            users_df.loc[users_df['username'] == self.current_user, [
                                                'password', 'email']] = (password, current_email)

                                            print(
                                                '\n', vol_df.loc[vol_df['Username'] == self.current_user])
                                            print(users_df.loc[users_df['username'] == self.current_user, [
                                                'username', 'password', 'email']])

                                            while True:
                                                commit = input('\nCommit changes? [y]/[n] ')
                                                if commit == 'y' or commit == 'n':
                                                    break
                                                else:
                                                    print('Your input is not recognised')
                                                    continue

                                            if commit == 'y':
                                                self.vol_db = vol_df.copy()
                                                vol_df.to_csv('volunteer_database.csv', index=False)
                                            else:
                                                counter = 0
                                                continue

                                            while True:
                                                repeat = input(
                                                    '\nWould you like to alter another parameter? [y]/[n] ')
                                                if repeat == 'y' or repeat == 'n':
                                                    break
                                                else:
                                                    print('Your input is not recognised')
                                                    continue
                                            if repeat == 'n':
                                                break
                                            else:
                                                counter = 0
                                                continue

                                        print(100 * '=')

                                    else:

                                        print(100 * '=')
                                        print('Please select input or update any information about you.')
                                        print("If you do NOT wish to change current value press ENTER during input.")
                                        print('Expected Inputs:\n' +
                                              '\t>First name\n' +
                                              '\t>Family name\n' +
                                              '\t>Phone number\n' +
                                              '\t>Availability\n' +
                                              '\t>Email\n' +
                                              '\t>Password\n')
                                        print('[B] to go back')
                                        print('[Q] to quit\n')

                                        print(vol_df.loc[vol_df['Username'] == self.current_user])
                                        questions = ['\nEnter first name: ', '\nEnter second name: ',
                                                     '\nEnter phone number in the format [+44(0)_______]:',
                                                     '\nEnter availability: ',
                                                     '\nEnter your email',
                                                     '\nEnter your new password (over 8 characters long)']

                                        def go_back(questionStack):
                                            i = 0
                                            answerStack = []

                                            while i < len(questionStack):
                                                if i == 0 or i == 1:
                                                    while True:
                                                        answer = input(questionStack[i])
                                                        if answer == 'B':
                                                            if i == 0:
                                                                print(100 * '=')
                                                                menu(self.functions)
                                                                exit()
                                                            answerStack.pop()
                                                            i -= 1
                                                        elif answer == 'Q':
                                                            print(100 * '=')
                                                            menu(self.functions)
                                                            exit()
                                                        elif answer == '':
                                                            answer = vol_df.iloc[vol_df.index[vol_df['Username']
                                                                                              == self.current_user][
                                                                                     0], i + 1]
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
                                                            print(100 * '=')
                                                            menu(self.functions)
                                                            exit()
                                                        elif answer == '':
                                                            answer = current_phone
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
                                                            print(100 * '=')
                                                            menu(self.functions)
                                                            exit()
                                                        elif answer == '':
                                                            answer = current_availability
                                                        elif not answer.isnumeric():
                                                            print("Invalid input.")
                                                            continue
                                                        elif int(answer) > 48:
                                                            print(
                                                                "Availability exceeds maximum weekly working hours (48h).")
                                                            continue
                                                        break
                                                elif i == 4:
                                                    while True:
                                                        answer = input(questionStack[i])
                                                        if answer == 'B':
                                                            if i == 0:
                                                                break
                                                            answerStack.pop()
                                                            i -= 1
                                                        elif answer == 'Q':
                                                            print(100 * '=')
                                                            menu(self.functions)
                                                            exit()
                                                        elif answer == '':
                                                            answer = current_email
                                                        elif len(inpt) < 8:
                                                            print(
                                                                "Sorry but your password needs to be at least 8 characters long.")
                                                            continue
                                                        break
                                                elif i == 5:
                                                    while True:
                                                        answer = input(questionStack[i])
                                                        if answer == 'B':
                                                            if i == 0:
                                                                break
                                                            answerStack.pop()
                                                            i -= 1
                                                        elif answer == 'Q':
                                                            print(100 * '=')
                                                            menu(self.functions)
                                                            exit()
                                                        elif answer == '':
                                                            answer = password
                                                        elif len(inpt) < 8:
                                                            print(
                                                                "Sorry but your password needs to be at least 8 characters long.")
                                                            continue
                                                        break

                                                if answer == 'B':
                                                    continue

                                                answerStack.append(answer)
                                                i += 1

                                            return answerStack

                                        while True:
                                            answers = go_back(questions)
                                            vol_df.loc[vol_df['Username'] == self.current_user] = [
                                                self.current_user, answers[0], answers[1], answers[2],
                                                self.camp_of_user, answers[3]]

                                            print(
                                                '\n', vol_df.loc[vol_df['Username'] == self.current_user])
                                            print(users_df.loc[users_df['username'] == self.current_user, [
                                                'username', 'password', 'email']])
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
                                        print(100 * '=')

                                    # def amend_self_info(self):
                                    #     '''
                                    #     Allows volunteer user to input their name, surname, phone number and availability.
                                    #     '''
                                    #     print(100 * '=')
                                    #     print('Please select which information you would like to change about yourself.')
                                    #     print('Possible interactions:\n' +
                                    #           '[1] - First name\n' +
                                    #           '[2] - Family name\n' +
                                    #           '[3] - Phone number\n' +
                                    #           '[4] - Availability\n' +
                                    #           '[5] - Change password\n')
                                    #     while True:
                                    #         print('[Q] to go back to main menu')
                                    #         user_input = input("Choose interaction:")
                                    #         if user_input == '1':
                                    #             current_name = self.vol_db[self.vol_db["Username"] == self.current_user]["First name"].values[0]
                                    #             print(f"Currently, your first name is set to {current_name}.")
                                    #             while True:
                                    #                 new_name = input("Enter new first name:")
                                    #                 new_name = new_name.capitalize()
                                    #                 if not new_name.isalpha():
                                    #                     print("Please enter a valid name.")
                                    #                 else:
                                    #                     break
                                    #             while True:
                                    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
                                    #                 if user_input == "y":
                                    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "First name"] = new_name
                                    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
                                    #                     print(f"First name has been set to {new_name}.")
                                    #                     break
                                    #                 elif user_input == "b":
                                    #                     print(100 * '=')
                                    #                     menu(self.functions)
                                    #                     exit()
                                    #                 else:
                                    #                     print("Invalid input.")
                                    #         elif user_input == '2':
                                    #             current_second_name = self.vol_db[self.vol_db["Username"] == self.current_user]["Second name"].values[0]
                                    #             print(f"Currently, your second name is set to {current_second_name}.")
                                    #             while True:
                                    #                 new_second_name = input("Enter new second name:")
                                    #                 new_second_name = new_second_name.capitalize()
                                    #                 if not new_second_name.isalpha():
                                    #                     print("Please enter a valid name.")
                                    #                 else:
                                    #                     break
                                    #             while True:
                                    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
                                    #                 if user_input == "y":
                                    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "Second name"] = new_second_name
                                    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
                                    #                     print(f"Second name has been set to {new_second_name}.")
                                    #                     break
                                    #                 elif user_input == "b":
                                    #                     print(100 * '=')
                                    #                     menu(self.functions)
                                    #                     exit()
                                    #                 else:
                                    #                     print("Invalid input.")
                                    #         elif user_input == '3':
                                    #             current_phone = str(self.vol_db[self.vol_db["Username"] == self.current_user]["Phone"].values[0])
                                    #             print(f"Currently, your phone number is set to +{current_phone}.")
                                    #             while True:
                                    #                 new_phone = input(
                                    #                     "Enter new phone number in the format +44_______:")
                                    #                 if not new_phone.isnumeric():
                                    #                     print("Please enter a valid phone number.")
                                    #                 elif len(new_phone) != 9:
                                    #                     print("Invalid format.")
                                    #                 elif new_phone[:2] != "44":
                                    #                     print("Invalid format.")
                                    #                 else:
                                    #                     break
                                    #             while True:
                                    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
                                    #                 if user_input == "y":
                                    #                     # new_phone = f"+{str(new_phone)}"
                                    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "Phone"] = new_phone
                                    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
                                    #                     print(f"Phone number has been set to +{new_phone}.")
                                    #                     break
                                    #                 elif user_input == "b":
                                    #                     print(100 * '=')
                                    #                     menu(self.functions)
                                    #                     exit()
                                    #                 else:
                                    #                     print("Invalid input.")
                                    #         elif user_input == '4':
                                    #             current_availability = self.vol_db[self.vol_db["Username"] == self.current_user]["Availability"].values[0]
                                    #             print(f"Currently, your availability is set to {current_availability}.")
                                    #             while True:
                                    #                 new_availability = input("Enter new availability:")
                                    #                 if not new_availability.isnumeric():
                                    #                     print("Invalid input.")
                                    #                 elif int(new_availability) > 48:
                                    #                     print("Availability exceeds maximum weekly working hours (48h).")
                                    #                 else:
                                    #                     break
                                    #             while True:
                                    #                 user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
                                    #                 if user_input == "y":
                                    #                     new_availability= f"{new_availability}h"
                                    #                     self.vol_db.loc[self.vol_db["Username"] == self.current_user, "Availability"] = new_availability
                                    #                     self.vol_db.to_csv("volunteer_database.csv",index=False)
                                    #                     print(f"Availability has been set to {new_availability}.")
                                    #                     break
                                    #                 elif user_input == "b":
                                    #                     print(100 * '=')
                                    #                     menu(self.functions)
                                    #                     exit()
                                    #                 else:
                                    #                     print("Invalid input.")
                                    #         elif user_input == '5':
                                    #             print("Email with OTP to reset password was sent to you")
                                    #             otp = ''.join([str(random.randint(0, 9)) for x in range(4)])
                                    #             email_sender = "hemsystem1@gmail.com"
                                    #             email_password = "asbwtshlldlaalld"
                                    #             email_receiver = self.user_db[self.user_db["username"] == self.current_user]['email'].values[0]

                                    #             subject = "OTP to reset password"
                                    #             body = """Yours OTP to reset password is: {}""".format(str(otp))
                                    #             mail = EmailMessage()
                                    #             mail["From"] = email_sender
                                    #             mail["To"] = email_receiver
                                    #             mail["Subject"] = subject
                                    #             mail.set_content(body)
                                    #             context = ssl.create_default_context()

                                    #             with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                                    #                 smtp.login(email_sender, email_password)
                                    #                 smtp.sendmail(email_sender, email_receiver, mail.as_string())
                                    #             while True:
                                    #                 otp_validation = input("Input here the OTP: ")
                                    #                 if otp != otp_validation:
                                    #                     print("Please enter valid OTP")
                                    #                 else:
                                    #                     break
                                    #             while True:
                                    #                 new_password = input("Type your new password: ")
                                    #                 password = self.user_db[self.user_db["username"] == self.current_user]['password'].values[0]
                                    #                 if password == new_password:
                                    #                     print("Sorry but your password can't be the same as the previous one")
                                    #                 elif len(new_password) < 8:
                                    #                     print("Sorry but your password needs to be at least 8 characters long")
                                    #                 else:
                                    #                     while True:
                                    #                         user_input = input("To confirm change of data, enter [Y]. To go back to the menu without saving this change, enter [B]:").lower()
                                    #                         if user_input == "y":
                                    #                             self.user_db.loc[self.user_db["username"] == self.current_user, 'password'] = new_password
                                    #                             self.user_db.to_csv("user_database.csv",index=False)
                                    #                             print("Password has been changed")
                                    #                             break
                                    #                         elif user_input == "b":
                                    #                             print(100 * '=')
                                    #                             menu(self.functions)
                                    #                             exit()
                                    #                         else:
                                    #                             print("Invalid input.")
                                    #                     break

                                    #         elif user_input == "Q" or user_input == "q":
                                    #             print(100 * '=')
                                    #             menu(self.functions)
                                    #             exit()
                                    #         else:
                                    #             print("Invalid input. Please select from the following options.")

                                    # def amend_self_info(self):
                                    '''
                                    Allows volunteer user to input their name, surname, phone number and availability.
                                    '''
                                    print(100 * '=')
                                    print('Please select input or update any information about you.')
                                    print("If you do NOT wish to change current value press ENTER during input.")
                                    print('Expected Inputs:\n' +
                                          '\t>First name\n' +
                                          '\t>Family name\n' +
                                          '\t>Phone number\n' +
                                          '\t>Availability\n')
                                    print('[B] to go back')
                                    print('[Q] to quit\n')

                                    vol_df = self.vol_db
                                    print(vol_df.loc[vol_df['Username'] == self.current_user])
                                    questions = ['\nEnter new first name: ', '\nEnter new second name: ',
                                                 '\nEnter new phone number in the format [44_______]:',
                                                 '\nEnter new availability: ']

                                    def go_back(questionStack):
                                        i = 0
                                        answerStack = []

                                        while i < len(questionStack):
                                            if i == 0 or i == 1:
                                                while True:
                                                    answer = input(questionStack[i])
                                                    if answer == 'B':
                                                        if i == 0:
                                                            print(100 * '=')
                                                            menu(self.functions)
                                                            exit()
                                                        answerStack.pop()
                                                        i -= 1
                                                    elif answer == 'Q':
                                                        print(100 * '=')
                                                        menu(self.functions)
                                                        exit()
                                                    elif answer == '':
                                                        answer = vol_df.iloc[vol_df.index[vol_df['Username']
                                                                                          == self.current_user][
                                                                                 0], i + 1]
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
                                                        print(100 * '=')
                                                        menu(self.functions)
                                                        exit()
                                                    elif answer == '':
                                                        answer = vol_df.iloc[vol_df.index[vol_df['Username']
                                                                                          == self.current_user][0], 3]
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
                                                        print(100 * '=')
                                                        menu(self.functions)
                                                        exit()
                                                    elif answer == '':
                                                        answer = vol_df.iloc[vol_df.index[vol_df['Username']
                                                                                          == self.current_user][0], 5]
                                                    elif not answer.isnumeric():
                                                        print("Invalid input.")
                                                        continue
                                                    elif int(answer) > 48:
                                                        print(
                                                            "Availability exceeds maximum weekly working hours (48h).")
                                                        continue
                                                    break
                                            if answer == 'B':
                                                continue

                                            answerStack.append(answer)
                                            i += 1

                                        return answerStack

                                    while True:
                                        answers = go_back(questions)
                                        vol_df.loc[vol_df['Username'] == self.current_user] = [
                                            self.current_user, answers[0], answers[1], answers[2], self.camp_of_user,
                                            answers[3]]

                                        print('\n', vol_df.loc[vol_df['Username'] == self.current_user])
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
                                    print(100 * '=')