import sys
from PyQt5.QtWidgets import QApplication,QGridLayout,QPushButton,QWidget,QLabel, QLineEdit, QMessageBox, QShortcut, QCheckBox
import pandas as pd
import logging

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.login_page_UI()
        
        df = pd.read_csv('user_database.csv').set_index('username').astype(str)
        self.volunteer = df.to_dict(orient='index')
        
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
        if self.username.text() in self.volunteer:
            if self.volunteer[self.username.text()]['password'] == self.password.text():
                self.logger.info(f'{self.username.text()} successfully logged in!')
            else:
                self.logger.warning(f"Failed attempt to log into {self.username.text()}'s account.")
        else:
            self.logger.error('User attempted to log into an account which does not exist.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Login()
    sys.exit(app.exec_())