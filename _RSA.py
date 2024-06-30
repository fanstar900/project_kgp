import random
import math

prime = []
public_key = None
private_key = None

def primefiller():    # fills the list prime with prime no.s
    seive = [True]*250    
    seive[0] = False
    seive[1] = False

    for i in range(2,250):
        for i in range( 2*i , 250 , i ):    # this loop ensures that the muliples of i are not primes
            seive[i] = False

    for i in range( 250 ):
        if seive[ i ]:
            prime.append( i )  # adds i to the list of primes if seive[i] is not zero(means it is a multiple of any previous no.)

def pickrandomprime():   # used to pick a prime no. from the list 'prime'
    global prime
    
    rt = prime [ random.randint(0,len(prime)-1)  ]   # we randomly take any prime no. from the list , removes it from the list(so that the next random pick is not the same prime no.), then returns it
    prime.remove( rt )
    return rt
    
def getkeys():
    global public_key
    global private_key
    global n

    primefiller()

    p = pickrandomprime()
    q = pickrandomprime()

    n = p * q
    fi= (p -1)*(q - 1)

    e = 2 
    while True:
        if math.gcd(e, fi) == 1:    #we try to find a number e which is coprime with fi and less than n
            break
        e += 1
 
    # d = (k*Φ(n) + 1) / e for some integer k
    public_key = (e,n)
 
    d = 2
    while True:
        if (d * e) % fi == 1:    #we try to find a number d such that e is the inverse of it given mod n
            break
        d += 1
 
    private_key = (d,n)

    return (public_key,private_key)  # returns a tuple containing tuples of public key(e,n) and private key(d,n)

def encrypted( ascii_value , public_key_partner):  # putting in ascii value of each letter for encryption
    e_partner = public_key_partner[0]
    n_partner = public_key_partner[1]

    encrypted_txt=1
    while(e_partner>0):    # idea is c=M^e(mod n)= [M(mod n)]*[M^(e-1)(mod n)]   || we cannot perform this step directly as it can lead to value overflow(too large number!)
        encrypted_txt *= ascii_value
        encrypted_txt %=n_partner
        e_partner -=1
    return encrypted_txt  # returns encrypted number c corresponding to the ascii value of each letter of the message   ||   c= M^e(mod n)


def encoder(message , public_key_partner):  
    encoded_msg_list = []
    for letter in message:
        encoded_msg_list.append(encrypted(ord(letter) , public_key_partner))
    return encoded_msg_list  #return the list containing encrypted ascii values of each letter of the message
    

def decrypted ( number ):  # argument is individual numbers (encrypted ascii) of the encrypted list
    global private_key
    d = private_key[0]
    n = private_key[ 1]
    decrypted_txt = 1
    
    while d > 0 :    # idea is M=c^d(mod n)= [c(mod n)]*[c^(d-1)(mod n)]   || we cannot perform this step directly as it can lead to value overflow(too large number!)
        decrypted_txt *= number
        decrypted_txt %= n
        d -=1

    return decrypted_txt  # returns the actural ascii value of each character of the message

def decoder( encoded_msg_list ):  


    decoded_msg_list = [] 
    for number in encoded_msg_list: 
        decoded_msg_list.append(decrypted(number))   # creates a list of ascii values of each character of the message

    decoded_msg=''
    for number in decoded_msg_list:  # this loop runs across the previous list and builds a string from the ascii values of each character of the message
        decoded_msg += chr(number)     # 'chr' function converts 'ascii' to 'character'
        
    return decoded_msg   #return the string of original message (this is what we wanted !!!)



