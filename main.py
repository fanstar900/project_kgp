import socket
import threading
import rsa
import sys


def clear_last_line():
   
    sys.stdout.write('\x1b[1A') # Move the cursor up one line
    
    sys.stdout.write('\x1b[2K')# Clear the line




public_key, private_key= rsa.newkeys(1024)
public_key_parter = None

choice = input('''What you want to connect to 
    press 1. Host
    press 2. Client
''')

if choice =='1':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates a node for communication
    server.bind( (socket.gethostbyname(socket.gethostname()) , 8080) )
    server.listen(1) # argument 1 restricts no. of connections
    client, _ = server.accept()
    client.send( public_key.save_pkcs1("PEM"))   #sends host public key to the client  (e,n)
    public_key_partner = rsa.PublicKey.load_pkcs1(client.recv(1024)) #receives the public key of the client
    

elif choice=='2':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect (( socket.gethostbyname(socket.gethostname()), 8080))
    public_key_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))  #receives the public key of the host
    client.send( public_key.save_pkcs1("PEM")) #sends client public key to the host   (e,n)


else : 
    exit()

def sending_messages (client) :
    while True:
        message = input("")
        clear_last_line()   # clears the input message immediately after sending it (for better looks of the interface)

        client.send(rsa.encrypt(message.encode(),public_key_partner))  #encrypts using partner public key and sends the message
        print("YOU: "+message)   # displays what you have written above


def receiving_messages (client):
    while True:
        print("Partner: "+ rsa.decrypt(client.recv(1024), private_key).decode())  #receives,decrypts using private key and decodes the message

threading.Thread(target= sending_messages, args=(client,)).start()    #starts the sending message thread
threading.Thread(target= receiving_messages, args= (client,)).start()    #starts the receiving message thread