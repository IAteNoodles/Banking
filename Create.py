
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
        source = mariadb.connect(user="Python",passwd="Python@Bank",database="Bank", host="localhost") #Connects to the database
        database = source.cursor() 
        # Asks for a UUID
        database.execute("select uuid()")
        uuid = database.fetchone()[0]
        # The given date is formatted as YYYY-MM-DD
        year, month, day = dob.split("-")
        dob= datetime(int(year), int(month), int(day))
        print(dob)
        uuid = sha256(uuid)
        print(uuid)
        publickey, privatekey = generate_keypair()
        print(publickey)
        #database.execute("""INSERT INTO Bank.People (ID,FirstName,MiddleName,LastName,DateOfBirth,Address,Phone,Email,PublicKey)
	    #VALUES ('xd2ec756059cdfb4796f9/29e4bf33e193783f2d91e9q36a61e1b81adc164898','dsa','fsa','fds','2003-08-04 00:00:00.000','dsa','asdsa','sdd',0x2D2D2D2D2D424547494E205055424C4943204B45592D2D2D2D2D20202020204D494942496A414E42676B71686B694766773042415145667341414F43415138414D49494243674B43415145417A6E49315641646767574D4B772B7275614B7A722020202020553871706D7066444477755835673375795934306D796F6A374C4C6B78564137426F396A7164746630435957424D4576384D7342584F4C6A6943614743306578202020202034572F2F4156434B6D343666327A6A79526C496943417470332B592F5966554E58665257502F6A512B64356A6B4130347A455470726B6F4938484B624934415A2020202020637779766E70465679574A486C757862724273476934434A6B6E535044653144316A463968646F4B754132516E627A426C63426954454E67426745734B6A3679202020202064422F31594B4C4A2F304351637647636D64767554593668776E36366858782F4A53567A6F53476C64566E782B4F4D522F694241427335576F36567348734455202020202041687142756F6733736C456C5362304946392B7155737377684E77776D49306B6A6D6A517A356C79646C42456D456E74336767314F6A6F62473969566C5A716520202020206E5149444151414220202020202D2D2D2D2D454E44205055424C4943204B45592D2D2D2D2D)""")
        
        '''database.execute("""insert into People(ID,FirstName,MiddleName,LastName,DateOfBirth,Address,Phone,Email,PublicKey) Values ("bd2ec756050cdfb4796f9629e4bf33e1637d3f2d91e9a34a61e1b81adc164898","Abhijit","Kumar","Singh","2003-08-04 00:00:00","Borhapjan","9678781811","thisabhjiithere@gmail.com",
                         '-----BEGIN PUBLIC KEY-----
                              MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAznI1VAdggWMKw+ruaKzr
                              U8qpmpfDDwuX5g3uyY40myoj7LLkxVA7Bo9jqdtf0CYWBMEv8MsBXOLjiCaGC0ex
                              4W//AVCKm46f2zjyRlIiCAtp3+Y/YfUNXfRWP/jQ+d5jkA04zETprkoI8HKbI4AZ
                              cwyvnpFVyWJHluxbrBsGi4CJknSPDe1D1jF9hdoKuA2QnbzBlcBiTENgBgEsKj6y
                              dB/1YKLJ/0CQcvGcmdvuTY6hwn66hXx/JSVzoSGldVnx+OMR/iBABs5Wo6VsHsDU
                              AhqBuog3slElSb0IF9+qUsswhNwwmI0kjmjQz5lydlBEmEnt3gg1OjobG9iVlZqe
                              nQIDAQAB'''
        test=str(dob)
        print(test)
        # We generate a sql statement to insert the data.
        sql = """INSERT INTO Bank.People (ID,FirstName,MiddleName,LastName,DateOfBirth,Address,Phone,Email,PublicKey)
        VALUES ('{uuid}','{first_name}','{middle_name}','{last_name}','{dob}','{address}','{phone}','{email}','{public_key}')""".format(
            uuid=uuid,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            address=address,
            phone=phone,
            email=email,
            public_key=publickey)
        
        # We map the variables to the appropriate keys
        
        print(sql)
        # Executing the statement
        database.execute(sql)
        # Commiting the transaction.
        source.commit()
        
        

#Test
People("Abhijit",
       "Test",
       "Singh",
       "Borhapjan",
       "2003-09-04",
       "thisabhijithere@protonmail.com",
       "9678781811")
#Test