import socket
import threading
import pickle
import sys
import _RSA 

public_key , private_key = _RSA.getkeys() 
public_key_partner =  None


def clear_last_line():
    sys.stdout.write('\x1b[1A')  # Move the cursor up one line
    sys.stdout.write('\x1b[2K')  # Clear the line


option= int(input('  What do you want to do ?     1.Host   2. Connect'))

if option==1:
    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)      # creates a node for communication
    server.bind((socket.gethostbyname(socket.gethostname()),8080))  
    server.listen(1)  # argument 1 restricts no. of connections
    client, address = server.accept()   

    client.send(pickle.dumps(public_key))    #sends host public key to the client  (e,n)
    public_key_partner = pickle.loads(client.recv(1024))   #receives the public key of the client




elif option==2:
    client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect( (socket.gethostbyname(socket.gethostname()),8080))     

    public_key_partner = pickle.loads(client.recv(1024))     #receives the public key of the host
    client.send(pickle.dumps(public_key))         #sends client public key to the host   (e,n)

    
else :
    exit(1)

def send_msg(client):
    while True:
        message = input("")
        clear_last_line()        # clears the input message immediately after sending it (for better looks of the interface)
        cypher_txt= _RSA.encoder( message , public_key_partner )    # encrypts the message as a list of numbers
        cypher_txt= pickle.dumps(cypher_txt)     # converts the list in the form of bytes (just for sending it over the network)
        client.send( cypher_txt )      # sends the message
        print('You: {}'.format(message))  # displays what you have written above



def recv_msg(client):
    while True:
        recv_msg = pickle.loads(client.recv(1024))    # receives the message in the form of bytes and converts it in the list form
                                                    # NOTE: here client.recv(1024) receives the message in the form of bytes 
        recv_msg = _RSA.decoder(recv_msg)       # decrypts the message from list form to strings of characters

        print('Partner: {}'.format(  recv_msg  )  )    # displays what client has written

threading.Thread(target= send_msg, args=(client,)).start()   #starts the sending message thread
threading.Thread(target= recv_msg, args=(client,)).start()    #starts the receiving message thread
