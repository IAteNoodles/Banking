from Crypto.Hash import keccak

from TFA import generate_secret
class People:
    def __init__(self, first_name, middle_name, last_name, address,email,dob, phone):
        import TFA
        from datetime import datetime
        key = hash(str((datetime.now().timestamp())))
        token = generate_secret()
        from mysql import connector
        t = connector.connect(user="python",passwd="Python",database="Bank", host="localhost")
        c = t.cursor()
        c.execute("select * from uuid()")
        uuid = c.fetchone()
        sql = '''INSERT INTO PEOPLE (UNIQUE_ID, FIRST_NAME, MIDDLE_NAME, LAST_NAME, ADDRESS, PHONE_NUMBER, EMAIL, DOB, SECURITY_NUMBER, 2FA_TOKEN_ID) VALUES (uuid, first_name, middle_name, last_name, address, phone, email, dob, num, tok)'''.format(first_name=first_name, middle_name=middle_name, last_name=last_name, address=address, email=email, phone=phone, dob=dob, security_number=key, tok=token, uuid = uuid)
        t.commit()
        c.execute(sql)
        
def hash(passwd: str):
    hash = keccak.new(digest_bits=512)
    hash.update(passwd.encode())
    return hash.hexdigest()  # Hashes the password without salt

People(input(),input(),input(),input(),input(),input(),input())