

from TFA import generate_secret
class People:
    """
     Class to access People objects

    People is the Parent table in the project. Every other object, other than Account is it's child. 
        For example, both Staff and User inherit its properties. 
    """
    def __init__(self, first_name, middle_name, last_name, address, dob, email, phone):
        """
        Insert into the parent table.

        Args:
            first_name (str): First name of the Person
            middle_name (str): Middle name of the Person
            last_name (str): Last name of the Person
            address (str): Address of the Person
            dob (str): Date of birth of the Person
            email (str): Valid email address of the Person
            phone (str): Valid phone number of the Person
        
        Note: email and phone are required and must be valid as they will be the only ways to recover incase the person loses their private key.
        """
        
        def generate_keypair():
            from Crypto.PublicKey import RSA
            key = RSA.generate(2048)
            private_key = key.export_key() #Generate private key
            public_key = key.publickey().export_key() #Generate public_key
            return public_key.decode("utf-8"),private_key.decode("utf-8") #Decode public and private keys
            
        from Hashing import sha256, sha3
        from datetime import datetime
        key = sha3(str((datetime.now().timestamp())))
        
        import mariadb #Shifted from mysql to mariadb
        source = mariadb.connect(user="python",passwd="Python",database="Bank", host="localhost") #Connects to the database
        database = source.cursor() 
        # Asks for a UUID
        database.execute("select uuid()")
        uuid = database.fetchone()[0]
        # The given date is formatted as YYYY-MM-DD
        year, month, day = dob.split("-")
        dob = datetime(int(year), int(month), int(day))
        uuid = sha256(uuid)
        print(uuid)
        publickey, privatekey = generate_keypair()
        print(publickey)
        
        # We generate a sql statement to insert the data.
        sql = '''INSERT INTO People 
        (ID,FirstName,MiddleName,LastName,DateOfBirth,Address,Phone,Email,PublicKey)
        VALUES ("{uuid}", "{first_name}", "{middle_name}", "{last_name}", "{dob}", "{address}", "{phone}", "{email}", '{public_key}')'''
        
        # We map the variables to the appropriate keys
        sql.format(
            uuid=uuid,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            address=address,
            phone=phone,
            email=email,
            public_key=publickey)
        
        print(sql)
        # Executing the statement
        database.execute(sql)
        # Commiting the transaction.
        source.commit()
        
        

#Test
People("Abhijit",
       "Kumar",
       "Singh",
       "Borhapjan",
       "thisabhijithere@protonmail.com",
       "2003-08-04",
       "9678781811")
#Test