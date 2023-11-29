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
    decrypted_message = [chr(pow(char, d, n)) for char in encrypted_message]
    return ''.join(decrypted_message)


def hack_private_key_parallel(public_key):
    n, e = public_key
    start_time = time.time()
    possible_d = 2
    while True:
        if pow(e, possible_d, n) == 1:
            end_time = time.time()
            hack_time = end_time - start_time
            return possible_d, hack_time
        possible_d += 1


bit_lengths = range(5, 16)
encryption_times = []
hack_times = []

message = "Hello, world!"
num_repetitions = 10 

def test_rsa(bits):
    total_time = 0.0
    hack_total_time = 0.0
    print("Starting bit ", bits)
    for _ in range(num_repetitions):
        start_time = time.time()
        public_key, private_key = generate_keys(bits)
        encrypted_message = rsa_encrypt(message, public_key)
        decrypted_message = rsa_decrypt(encrypted_message, private_key)
        end_time = time.time()
        total_time += (end_time - start_time)
        
        hacked_private_key, hack_time = hack_private_key_parallel(public_key)
        hack_total_time += hack_time
    print("Bit ", bits, " done. Total time: ", total_time / num_repetitions, " Hack time: ", hack_total_time / num_repetitions)


    return total_time / num_repetitions, hack_total_time / num_repetitions

if __name__ == '__main__':
    with Pool() as pool:
        results = pool.map(test_rsa, bit_lengths)
        for result in results:
            encryption_times.append(result[0])
            hack_times.append(result[1])

    # Plotar os resultados
    plt.plot(bit_lengths, encryption_times, label='Encryption and Decryption Time', marker='.')
    plt.plot(bit_lengths, hack_times, label='Hacking Time', marker='.')
    plt.xlabel('Key size (bits)')
    plt.ylabel('Time (seconds)')
    plt.title('Key Size vs Encryption/Decryption Time')
    plt.legend()
    plt.show()
