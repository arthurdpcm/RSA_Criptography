# RSA Encryption Project

**!Warning** Python 3.12 does not accept the kivy version we used.

This project, developed for the final semester of the **Programming and Algorithms** course at Aix-Marseille Université, explores the RSA encryption method. Below are the steps involved in the process:

## How RSA Works
![Diagram](https://github.com/arthurdpcm/RSA_Encription/assets/61255233/4780f5bd-6eb8-44f3-b212-826a6eb03d61)


### Step 1:
<img src="https://github.com/arthurdpcm/RSA_Encription/assets/61255233/7dd104d2-ca02-4ba7-bc96-068e066f5c32" width="800" height="500" />

```python
12616291, 65537
```

### Step 2:
<img src="https://github.com/arthurdpcm/RSA_Encription/assets/61255233/8052aeef-ac92-477e-a58a-303cb6509470" width="800" height="600" />

```python
[2787639, 1567162, 5189040, 5189040, 240842, 9249679, 5535986, 12484563, 240842, 924404, 5189040, 12469187, 4833007]
```

### Step 3:
<img src="https://github.com/arthurdpcm/RSA_Encription/assets/61255233/95eefed8-89bf-440e-bb39-4c346b8094d6" width="800" height="500" />

```python
'Hello, World!'
```


RSA Encription method. There is four files in this repository:
- ## Encrypt.py
  #### This file uses Kivy to create the User Interface and it's where you are going to enter the public key generated by the decrypt.py and write the message to be encrypted.
- ## Decrypt.py
  #### This file uses Kivy to create the User Interface and it's where you are going to enter the key size (bits) to generate the public and private key, and also enter the encrypted message. 
- ## rsa_simulation.py
  #### This file runs the process of encrypting and decrypting multiple times to compare how long it takes to decrypt different key sizes. It also plots the chart of it.
- ## hack_rsa_parallel.py
  #### This file tries to hack using brute force the encrypted message. It runs 10 times from 5 bits to 15 bits to have a better measure of how much time it takes. It also plots the chart of it. 

## Libraries necessary to run the following code:
- pip install kivy (encrypt.py and decrypt.py)
- pip install random
- pip install time
- pip install matplotlib.pyplot (hack_rsa_parallel.py, rsa_simulation.py)
- pip install multiprocessing


## Project made by:
- ### Arthur Duarte https://github.com/arthurdpcm
- ### Luísa Vieira https://github.com/luisa-vieira



# References:
- https://medium.com/@jinkyulim96/algorithms-explained-rsa-encryption-9a37083aaa62
- https://www.techtarget.com/searchsecurity/definition/RSA
