import sys 
from PyQt5.QtWidgets import QApplication,QGridLayout,QPushButton,QWidget,QLabel, QLineEdit, QMainWindow, QVBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
import pandas as pd
import logging
        
class Login(QWidget):
    def __init__(self, database):
        super().__init__()
        self.login_page_UI()
        self.database = database

        logging.basicConfig(filename='logfile.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def login_page_UI(self):
        self.setWindowTitle('Login')
        self.setGeometry(250,250,500,100)

        layout = QGridLayout()
        
        username_label = QLabel('Username:', self)
        password_label = QLabel('Password:', self)

        self.username = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(username_label, 0, 0)
        layout.addWidget(password_label, 1, 0)
               
        layout.addWidget(self.username, 0, 1)
        layout.addWidget(self.password, 1, 1)
        
        button_login = QPushButton('Login', self)

        layout.addWidget(button_login, 2, 0, 2, 2)
        button_login.clicked.connect(self.login_validity)

        self.setLayout(layout)
        self.show()

    def login_validity(self):
        if self.username.text() in self.database:
            user = self.database[self.username.text()]
            if user['password'] == self.password.text() and user['activated'] == True:
                    
                    self.logger.info(f'{self.username.text()} logged in successfully!')
                    self.close()
                    
                    if user['role'] == 'admin':
                        self.admin_page = AdminWindow(self.username.text(), self.database)
                        self.admin_page.show()
                    else:
                        self.volunteer_page = VolunteerWindow(self.username.text(), self.database)
                        self.volunteer_page.show()

            elif user['password'] == self.password.text() and user['activated'] == False:
                self.logger.error(f"{self.username.text()}'s account has been deactivated!")
                errorMsg = QMessageBox()
                errorMsg.setIcon(QMessageBox.Critical)
                errorMsg.setText('Your account has been deactivated, contact the administrator')
                errorMsg.exec_()
            
            else:
                self.logger.warning(f"Failed attempt to log into {self.username.text()}'s account.")
        else:
            self.logger.error('User attempted to log into an account which does not exist.')

class AdminWindow(QMainWindow):
    def __init__(self, username, database):
        super().__init__()
        self.database = database
        self.objName = username

        self.admin_ui()
        
    def admin_ui(self):
        self.setWindowTitle('Admin View')
        self.setGeometry(250,250,500,400)

        layout = QVBoxLayout()
        emergency_plan = QPushButton('Create new emergency plan',self)
        close_plan = QPushButton('Close existing emergency plan',self)
        plan_summary = QPushButton('View existing emergency plan', self)
        activate_account = QPushButton('Activate Volunteer Account',self)
        reactivate_account = QPushButton('Reactivate Volunteer Account',self)
        deactivate_account = QPushButton('Deactivate Volunteer Account',self)
        delete_account = QPushButton('Delete Volunteer Account',self)

        self.console_log = QLabel(f'Welcome back {self.objName}',self)
        self.console_log.setStyleSheet('font: 30pt Courier')
        self.console_log.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.console_log)
        layout.addWidget(emergency_plan)
        layout.addWidget(close_plan)
        layout.addWidget(plan_summary)
        layout.addWidget(activate_account)
        layout.addWidget(reactivate_account)
        layout.addWidget(deactivate_account)
        layout.addWidget(delete_account)
        
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

class VolunteerWindow(QMainWindow):
    def __init__(self, username, database):
        super().__init__()
        self.database = database
        self.objName = username
        self.volunteer_ui()
        
    def volunteer_ui(self):
        self.setWindowTitle('Volunteer View')
        self.setGeometry(250,250,300,100)

        layout = QVBoxLayout()

        edit_personal_info = QPushButton('Edit personal information',self)
        create_emergency_profile = QPushButton('Create a new emergency profile',self)
        
        self.console_log = QLabel(f'Welcome back {self.objName}',self)
        self.console_log.setStyleSheet('font: 30pt Courier')
        self.console_log.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.console_log)
    
        layout.addWidget(edit_personal_info)
        edit_personal_info.clicked.connect(self.personal_details)
        layout.addWidget(create_emergency_profile)
        
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
    
    def personal_details(self):
        name = QInputDialog.getText(self, 'Input Dialog', 'Enter your name: ')
        phone = QInputDialog.getInt(self, 'Input Dialog', 'Phone Number: ')
        availability = QInputDialog.getText(self, 'Input Dialog', 'Till when are you available?: ')
        assigned_camp = QInputDialog.getText(self, 'Input Dialog', 'What camp are you assigned to?: ') 


class test():
    def __init__(self):
        self.user_data = None
    
    def users_login(self):
        '''
        Reads (or if first time logging in creates) users_dataframe.csv.
        Creates self.user_data DataFrame. # when admin wants to call all details of all users they'd use this
        Calls login widget.
        '''
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

        app = QApplication(sys.argv)
        win = Login(users_dict)
        sys.exit(app.exec_())


if __name__ == '__main__':
        
    a = test()
    a.users_login()