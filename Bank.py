from json import dump as json_dump
from mysql import connector 
class Admin:
    """A class that encapsulates the admin type user. 
    Provides root level modification to the database, and other admin features."""
    def __init__(self,ID: str,passwd: str)-> None:
        """
        __init__ Method to create an Admin object. Accepts the credentials and creates the object.

        User after creating the object can use .login() and .signup() methods which can be used accordingly.

        Args:
            ID (str): Identification number of the admin object.
            passwd (str): Password of the admin object.
            host (str): Hostname of the database server.
        """
        self.__PASSWD = passwd
        self.__ID = ID
        self.__CONNECTION = connector.connect(user="python",host="localhost",passwd="Python")
        self.__PERMISSIONS: dict()
    def login(self):
        """
        login Logs the admin object into the database.

        Takes the credentials from the constructor and checks if there is a record with the same ID in the database.
        If no record exists, it returns error message else returns a confirmation message.
        """
        #self.__CONNECTION.execute("SELECT")
        pass
    
    def signup(self):
        """
        signup Creates a new admin object and stores it in the database.

        Takes the credentials from the constructor and checks if there is a record with the same ID. If yes, it returns a simple warning else returns a confirmation message.
        """
        #self.__CONNECTION.execute("INSERT INTO ADMIN")
        pass
    
    