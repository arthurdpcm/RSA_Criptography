import random
import time
import matplotlib.pyplot as plt
from multiprocessing import Pool

def is_prime(num):
    if num < 2:
        return False
    for divisor in range(2, int(num ** 0.5) + 1):
        if num % divisor == 0:
            return False
    return True

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits) | 1  
        if is_prime(num):
            return num

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    else:
        return x % m


def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537  
    
    d = modinv(e, phi_n)

    return (n, e), (n, d)  


def rsa_encrypt(message, public_key):
    n, e = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def rsa_decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_integers = [pow(char, d, n) for char in encrypted_message]
    decrypted_bytes = bytearray()
    for integer in decrypted_integers:
        decrypted_bytes.extend(integer.to_bytes((integer.bit_length() + 7) // 8, 'big'))
    return decrypted_bytes.decode('utf-8', errors='ignore')


bit_lengths = range(5, 31)
encryption_times = []

message = "Hello, world!"
num_repetitions = 1000  

def test_rsa(bits):
    total_time = 0.0

    print("Starting bit ", bits)
    for _ in range(num_repetitions):
        start_time = time.time()
        public_key, private_key = generate_keys(bits)
        encrypted_message = rsa_encrypt(message, public_key)
        decrypted_message = rsa_decrypt(encrypted_message, private_key)
        end_time = time.time()
        total_time += (end_time - start_time)

    print("Bit ", bits, " done. Total time: ", total_time / num_repetitions)

    return total_time / num_repetitions

if __name__ == '__main__':
    with Pool() as pool:
        result = pool.map(test_rsa, bit_lengths)
        encryption_times.extend(result)

    
    plt.plot(bit_lengths, encryption_times, label='Encryption and Decryption Time', marker='.')
    plt.xlabel('Key Size (bits)')
    plt.ylabel('Time (seconds)')
    plt.title('Key Size vs Encryption/Decryption Time')
    plt.legend()
    plt.show()
