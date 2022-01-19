from Crypto.Hash import keccak

from TFA import generate_secret
class People:
    def __init__(self, first_name, middle_name, last_name, address,email,dob, phone):
        
        def generate_keypair():
            from Crypto.PublicKey import RSA
            import pickle
            key = RSA.generate(2048)
            private_key = key.export_key()
            file_private = open("private.pem", "wb")
            file_private.write(private_key)
            file_private.close()
            file_private = open("private.pem","rb")
            public_key = key.publickey().export_key()
            file_public = open("receiver.pem", "wb")
            file_public.write(public_key)
            file_public.close()
            file_public = open("receiver.pem", "rb")
            public_key = pickle.load(file_public)
            private_key = pickle.load(file_private)
            return public_key,private_key
            
        
        import TFA
        from datetime import datetime
        key = hash(str((datetime.now().timestamp())))
        token = generate_secret()
        from mariadb import connector
        t = connector.connect(user="python",passwd="Python",database="Bank", host="localhost")
        c = t.cursor()
        c.execute("select * from uuid()")
        uuid = c.fetchone()
        from Hashing import sha256
        uuid = sha256(uuid)
        publickey, privatekey = generate_keypair()
        sql = '''INSERT INTO `People` 
        (`ID`, `FirstName`, `MiddleName`, `LastName`, `DateOfBirth`, `Address`, `Phone`, `Email`, `PublicKey`)
        VALUES (uuid, first_name, middle_name, last_name, address, phone, email, public_key)'''.format(
            uuid=uuid,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            address=address,
            phone=phone,
            email=email,
            public_key=publickey)
        t.commit()
        c.execute(sql)
        
def hash(passwd: str):
    hash = keccak.new(digest_bits=512)
    hash.update(passwd.encode())
    return hash.hexdigest()  # Hashes the password without salt

People(input(),input(),input(),input(),input(),input(),input())