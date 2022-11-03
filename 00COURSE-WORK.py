### FIRST ROUGH OUTLINE ###
# Please nevermind the incorrect spelling; am tired

# Docstring aren't serious docstrings but rough estimates of what certain method/class is all about
# Comments set my immediate ideas on how to implement

class CentralFunctions():
    
    '''
    Outlines key functions relevant to each user type. Without interactions though.
    Saves key data both through .csv files and in self.variables.
    Must be dry and designed in mind that all of these methods will be called through input-dictionary interactions.
    (input-dictionary interactions = input() function returns a str and then you put it into a dictionary to call a function)
    '''
    
    # Each method is a handfull so if we find we are repeating actions then feel free to add auxillary methods to help the main ones
    # IMPORTANT: I say .csv file a lot but that doesn't mean that the method must be reading from .csv files directly, but 
    # most likely from the local pandas dataframes formed by read_all_data()
    
    def __init__(self):
        self.active_emergency = None
        self.current_user = None
        self.read_all_data()
        self.functions()
        pass
    
    def read_all_data(self):
        '''
        Essential method for smooth runnning of the software.
        Reads all .csv files into local pandas dataframes upon the start of the program, so we don't have to read and write on the files
        directly a million times.
        '''
        pass
    
    def save(self, file=None):
        '''
        Saves a relvant file when we are done inputting new data.
        I put default value as None so we have a quick trigger to save every file together. If you manage a particular file at a time then 
        what file we are saving should be specified
        '''
        pass
    
    def call_no_of_refugees(self):
        '''
        Reads the .csv file with refugees and returns the number of refugees + no of refugees broken down across camps
        (Potentially can be conditionally configured to also return their quantitative needs upon further request, such as food,
        water and shelter demands and how much we got in the "central hub" + graphs(!) which can be done with pandas but better done with matplotlib)
        '''
        pass
    
    def call_camps(self):
        '''
        Sounds fucking evil, we might need to change the name of the method XD
        Reads the .csv file with camps and returns relevant data.
            > How many camps
            > How many refugees in each
            > Each camp's capacity
            > How many volunteers in each camp
           (> Each camp's resource capacity)
        '''
        pass
    
    def call_volunteers(self):
        '''
        Reads the .csv file with volunteers and returns relevant info
            > How many volunteers
            > How many volunteers in each camp
            > Their names
        Potentially put limiters to view volunteers from one specific camp
        (Potentially add an option to curtail information to bare bones minimum(just username for example or just in one specific camp). Why? 
        So we can use this method in the future for activating and deactivating volunteers in a curtailed form.
        It would be convinient to look at the list of volunteers when you type out a deletion command)
        '''
        pass
    
    def login(self):
        '''
        The only interactive method in this class.
        Defines who is the current user from user input. Will be useful when we get to forming architecture for user interactions.
        Cross refernece with .csv file 
        self.current_user = "vol" OR "adm"
        
        (When admin logs-in a special procedure will active which might create a special volunteer account for the admin to allow the admin
        to have capabilities of volunteers for further convinience. This way we don't have to mix admin's capabilities with volunteers'
        capabilities.)
        (During login I believe admins should have a distinct procedure; creation of their account by themselves, since all the volunteer accounts
        will be created by admins and then only filled by volunteers, so perhaps a separate method would be employed whithin this method to form
        an account creation procedure)
        '''
        # User input will be interpreted and checked via a dictionary of admins and volunteers.
        pass
    
    def users(self):
        '''
        Will read the .csv file with the volunteers and form a dictionary which will be employed by login(), with passwords and logins
        '''
        pass
    
    def functions(self):
        '''
        creates a dictionary of all central functions to be used by admin and volunteer classes
        '''
        pass
    
class admin(CentralFunctions):
    '''
    Functions relevant to admin user type. Have both dry no-interaction methods and interactive methods to call them for ease of readability.
    '''
    
    def __init__(self):
        CentralFunctions.__init__(self)
        pass
    
    def admin_functions(self): # no interaction
        '''
        creates dictionary of all no-interaction methods used by admin for later interpretation by user-input methods
        '''
        pass
    
    def create_emergency(self, name_of_emergency, type, description, location, start_date, close_date): # no interaction
        '''
        Inputs will all be strings (except maybe dates if we will be allowed to use datetime module)
        Creates a FOLDER with a number of .csv files, all with relevant names.
        self.active_emergency = 'name_of_emergency' <-- this is done so when we close the emergency it would get archieved and all 
                                                        relevant data would be saved with relevant name for ease of use.
        .csv files: <-- .csv files provide PERSISTENCE
            > dataframe with emergency properties outlined in the argument
            > dataframe with all relevant camps (at this stage empty, but only with columns)
            > dataframe with volunteers (at this stage empty, but only with columns)
            > dataframe with refugees (at this stage empty, but only with columns)
        '''
        pass
    
    def close_emergency(self): # no interaction
        '''
        Take the folder and all the data we accumulated in the .csv files and save under a relevant name like "closed emergency XXX"
        Clear all global and local self.variables.
        Stop the entire program (I'm not even sure how to do that from a method tbh, but we'll figure it out)
        
        Advantage of saving all the data under a new name is it won't possibly ever be interacted with by the rest of the program and
        we get to archive the data which is real-life-useful thing to do.
        '''
        pass
    
    def admin_volunteer_commands(self, command): # no interaction
        '''
        Input will be a string which will dictate what command to apply. Why not use a dictionary? Because there will be only three available
        manipulations so it would be less messy to create one big method than three small and a dictionary.
        Commands available:
            > DEACTIVATE
            > REACTIVATE
            > DELETE
        Method will then apply these commands to the volunteer .csv file
        '''
        # have a "status" column in volunteer dataframe which would indicate the account status. The login method would check the status of volunteer
        # before giving or not giving access. This method would simply change that status
        # In the case of delete simply delete the record.
        pass
    
    def write_volunteer(self, username, password, camp): # no interaction
        '''
        Method that will write into the volunteer dataframe adding new volunteers but only with their username and password and camp assigned to.
        Make sure to have a method that will update the users dictionary (either by rerunning the users() method or manually adding a new entry into the 
        existing dictionary)
        
        (When run maybe show the names of exisiting camps for user friendliness)
        '''
        pass
    
    def write_camp(self, name, population_capacity, resource_capacity): # no interaction
        '''
        Write into the camps dataframe adding the camps relevant to the emergency and their properties.
        '''
        pass
    
    def admin_interaction(self):
        '''
        method that will require user input and then interpret it as an executable method. This one will be tricky to design because the following functions must be
        implemented:
            1 When logging in first time call methods in this order:
                > login() <-- special procedures for admins
                > create_emergency() <--  input each piece of data sequentially so it's userfriendly
                > write_camps() <--  input each piece of data sequentially so it's userfriendly
                > write_volunteers() <--  input each piece of data sequentially so it's userfriendly
            2 When logging in subsequently any method should be run regardless of order
            3 At any point the data logging should be cancelled
            4 Every time data is logged we must be write it to .csv files to prevent it from disappearing in case of system failure
            5 When a method is performed we must be able to perform another one and then do it indefinetly
            6 Have a shut off button <-- maybe separate method?
        '''
        # 1 check if there are any files in directory that have something like "EMERGENCY" in the name, if none then you are logging in first time
        #   this should lead to triggering a chain of methods to properly create an emergency
        # 2 check if there are files in the directory with code name like "EMERGENCY" in the name, if there are then read them and basically get the system up to date
        # 3 the entire thing should be in the while loop that should be engineered to loop/jump to any method when commanded. When inputting data, sequentilly, we
        #   we should have an off button like just pressing enter to cancel input, ask user if they mean to stop and then send them back to the neutral method
        #   selection menu
        # 4 Once all data is logged in the local dataframe, show it to the user for confimation, ask if they are satisfied and then if they are save() it
        # 5 smart use of while loops
        pass
    
class volunteer(CentralFunctions):
    '''
    Functions relevant to volunteer user type. Have both dry no-interaction methods and interactive methods to call them for ease of readability
    '''
    
    def __init__(self):
        CentralFunctions.__init__(self)
        pass       
    
    def vol_functions(self): # no interaction
        '''
        creates dictionary of all no-interaction methods used by volunteer for later interpretation by user-input methods
        '''
        pass
    
    def edit_self_info(self, name, phone, age, gender): # no interaction
        '''
        Write into the volunteer dataframe to update info on a particular volunteer
        '''
        pass
    
    def create_profile(self, name, no_of_relatives, medical_needs, camp): # no interaction
        '''
        Write into the refugee dataframe to add refugees family
        '''
        pass
    
    def vol_interaction(self):
        '''
        Puts the no interaction methods together to form an interaface that allows the volunteer to interact with the program. Largely similar to the admin analogue
            > When first logged in make the volunteer fill up the data about them.
            > Allow to call any method at any time
            > Basically have the same capabilities to interact as the admin
        '''
        pass
    
def execute():
    '''
    How does all of this shit work bruh
    '''
    # employ a while loop to keep the program running
    # call login method and methods made to check if there exists an emergency, then use logic to determine how to treat the admin and volunteers
    # depending on who the user is call relevant interaction method
    pass