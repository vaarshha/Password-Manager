from Cryptodome.Cipher import AES 
from Crypto import Random
import base64
from Crypto.Protocol.KDF import PBKDF2
import base64
import random
from password_strength import PasswordPolicy
import os

from db_queries import *
from dotenv import load_dotenv

load_dotenv()

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=1,  # need min. 2 digits
    special=1,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)

def password_strength(password):
	if policy.test(password)==[]:
		return True
	else:
		return False

salt = b'E\xb0\x884\xd46'

def get_private_key(password):
	salt = b"this is a salt"
	kdf = PBKDF2(password, salt, 64, 1000)
	key = kdf[:32]
	return key
 
 
def encrypt(raw, password="varsha"):
	BLOCK_SIZE = 16
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
	
	private_key = get_private_key(password)
	raw = pad(raw)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	string = (iv + cipher.encrypt(raw.encode("utf8")))
	return base64.b64encode(string).decode("utf8")

def decrypt(enc, password="varsha"):
	unpad = lambda s: s[:-ord(s[len(s) - 1:])]
	private_key = get_private_key(password)
	enc = base64.b64decode(enc)
	iv = enc[:16]
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(enc[16:]))

def verify_pass(entered_password):
    master_password= os.getenv("MASTER_PASSWORD")
    if entered_password == decrypt(master_password).decode('utf-8'):
        return True
    
def generate_password():
	phrase = input("Enter a phrase: ")
	phrase = phrase.replace(" ","")
	while len(phrase)<8:
		print("***Enter a longer phrase [Atleast 8 characters excluding spaces]***")
		phrase = input("Enter a phrase: ")
		phrase = phrase.replace(" ","")
	res = ''.join(random.choice((str.upper, str.lower))(char) for char in phrase)
	spl_chars=['*','$','%','#','@']
	res+=str(int(random.random()*1000//1))
	res+=random.choice(spl_chars)
	return res

# def add_pass(obj):
# 	website = input("Enter website name: ")
# 	if obj.find_rec(website):
# 		print("Password already logged for website. Update or delete instead")
# 		return 
# 	username = input("Enter username: ")
# 	choice = input("A. Enter password \nB. Create password: ")
# 	if choice == 'A':
# 		password = input("Password: ")
# 		while not password_strength(password):
# 			print("**Password is weak**")
# 			password = input("Password: ")
# 		obj.insert_rec(website,username,encrypt(password))
# 	elif choice=='B':
# 		obj.insert_rec(website,username,encrypt(generate_password()))
# 	else:
# 		print("Invalid choice")

def retrieve_pass(obj):
	website = input("Enter website name: ")
	res = obj.find_rec(website)
	if res:
		print(f"website: {website} userid:{res[0][1]} password:{decrypt(res[0][2]).decode('utf-8')} Last update: {datetime.date(res[0][3])}")
	else:
		print("Not found")

def update_password(obj):
	website = input("Enter website name: ")
	choice = input("A. Enter password \nB. Create password: ")
	if choice == 'A':
		password = input("Password: ")
		while not password_strength(password):
			print("**Password is weak**")

			password = input("Password: ")
		obj.update_entry(website,encrypt(password))
	elif choice=='B':
		obj.update_entry(website,encrypt(generate_password()))

def delete_pass(obj):
	website = input("Website: ")
	obj.delete_entry(website)