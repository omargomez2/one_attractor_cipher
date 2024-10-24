#-----------------
# Basic cipher of JSON objects using one Lorenz attractor
# osgg.net
#-----------------

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import random
import json

# Lorenz parameters
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0

# Define the Lorenz system
def lorenz_attractor(state, t):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Parameters for integration
dt = 0.01  # Time step
T = 50     # Total time
t = np.arange(0, T, dt)

# Random initial conditions for the Lorenz attractor
def random_initial_conditions():
    return [
        random.uniform(-20.0, 20.0),  # x: larger random range for more variability
        random.uniform(-30.0, 30.0),  # y: larger random range
        random.uniform(5.0, 50.0)     # z: different range for more random behavior
    ]

initial_conditions = random_initial_conditions()
print(f"Initial conditions: {initial_conditions}")

# Integrate the Lorenz attractor system
states = odeint(lorenz_attractor, initial_conditions, t)

# Function to convert a string into a list of integers representing ASCII values
def string_to_ascii_list(s):
    return [ord(c) for c in s]

# Function to convert a list of integers (ASCII values) back to a string
def ascii_list_to_string(lst):
    return ''.join(chr(i) for i in lst)

# XOR encryption function for a JSON string
def xor_encrypt_json(json_str, key):
    ascii_vals = string_to_ascii_list(json_str)
    return [val ^ key[i % len(key)] for i, val in enumerate(ascii_vals)]

# Encrypt a JSON object
json_obj = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "role": "admin"
}
print(f"Original JSON: {json_obj}")


# Convert JSON object to string
json_str = json.dumps(json_obj)

# Use the x-values of the Lorenz attractor as the key for encryption
key_stream = np.abs(states[:len(json_str)]).astype(int)[:, 0] % 256

# Encrypt the JSON string
ciphered_ascii_list = xor_encrypt_json(json_str, key_stream)
print(f"Encrypted JSON (ASCII list): {ciphered_ascii_list}")

# Decrypt the JSON string by applying the same XOR operation
def xor_decrypt_json(encrypted_list, key):
    decrypted_ascii = [val ^ key[i % len(key)] for i, val in enumerate(encrypted_list)]
    return ascii_list_to_string(decrypted_ascii)

# Decrypt the message
decrypted_json_str = xor_decrypt_json(ciphered_ascii_list, key_stream)
decrypted_json_obj = json.loads(decrypted_json_str)

print(f"Decrypted JSON object: {decrypted_json_obj}")
