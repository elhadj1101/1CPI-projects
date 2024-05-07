import numpy as np
from sympy import symbols, Eq, solve

# Define the alphabet
alphabet = " #$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃń"


# Encrypt function
def encrypt(plaintext, key_matrix):
    cipher_text_list = []

    for i in range(0, len(plaintext), 2):
        # Convert the plaintext to numerical values
        p1 = alphabet.index(plaintext[i])
        p2 = alphabet.index(plaintext[i + 1]) if i + 1 < len(plaintext) else 0

        plain_matrix = [p1, p2]

        # Apply the Hill Cipher
        cipher_matrix = np.matmul(key_matrix, plain_matrix) % 256
        cipher_text_list += [alphabet[x] for x in cipher_matrix]

    cipher_text = "".join(x for x in cipher_text_list)

    return cipher_text


def inv_mod(det):
    for i in range(256):
        if (i * det) % 256 == 1:
            return i


# Decrypt function
def decrypt(ciphertext, key_matrix):
    plain_text_list = []

    # Calculate the inverse of the key matrix
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = inv_mod(det)

    adj = np.round(det * np.linalg.inv(key_matrix)).astype(int)
    key_inv = (det_inv * adj) % 256
    for x in key_inv:
        for y in x:
            if isinstance(y, float):
                print("matrix elements should be integers")
                return

    for i in range(0, len(ciphertext), 2):
        # Convert the ciphertext to numerical values
        c1 = alphabet.index(ciphertext[i])
        c2 = alphabet.index(ciphertext[i + 1])
        cipher_matrix = [c1, c2]

        # Apply the inverse Hill Cipher
        plain_matrix = np.matmul(key_inv, cipher_matrix) % 256
        plain_text_list += [alphabet[x] for x in plain_matrix]

    plain_text = "".join(x for x in plain_text_list)

    return plain_text


def hill_cipher_attack(known_plain_text, known_cipher):
    # for 2x2 matrix
    key_matrix = None
    if len(known_plain_text) != len(known_cipher):
        print("plain-cipher text should be have the same length")

    for x in range(0, len(known_plain_text), 4):
        plain_substring = known_plain_text[x : x + 4]
        cipher_substring = known_cipher[x : x + 4]
        if len(plain_substring) == len(cipher_substring) == 4:

            plain_indexes = [alphabet.index(x) for x in plain_substring]
            cipher_indexes = [alphabet.index(x) for x in cipher_substring]

            # ---------------------

            x, y, w, z = symbols("x y w z")
            eq1 = Eq(plain_indexes[0] * x + plain_indexes[1] * y, cipher_indexes[0])
            eq2 = Eq(plain_indexes[0] * w + plain_indexes[1] * z, cipher_indexes[1])
            eq3 = Eq(plain_indexes[2] * x + plain_indexes[3] * y, cipher_indexes[2])
            eq4 = Eq(plain_indexes[2] * w + plain_indexes[3] * z, cipher_indexes[3])

            solution = solve((eq1, eq2, eq3, eq4), (x, y, w, z))
            key_matrix = np.array(list(solution.values())).reshape(2, 2)

            print(f"this is key matrix{key_matrix}")
            if key_matrix is not None:
                break


if __name__ == "__main__":
    print(
        "\033[1m"
        + "---------------------------------------------HILL CIPHER ENCRYPTION-----------------------------------------------"
        + "\033[0m"
    )

    key_table = input("Enter your key matrix as a,b,c,d : ").split(",")
    dim = int(len(key_table) ** 0.5)

    if dim * dim != len(key_table):
        print("Key matrix should be squared")

    key_matrix = np.array(key_table, dtype=int).reshape(dim, dim)
    det = int(np.round(np.linalg.det(key_matrix)))
    if np.gcd(det, 256) != 1:
        print("determinant gcd with 256 should be 1")

    else:
        i = ""
        while True:
            plain = input("enter your plain text  : \n")
            cipher = encrypt(plain, key_matrix)
            print(f"this is the encrypted text : {cipher}")
            print(f"this is you decrypted text : {decrypt(cipher , key_matrix)}")
            attack = input(
                "\ndo you want to attack the algorithm with this plain-cipher pair y/n : "
            )
            if attack == "y":
                hill_cipher_attack(plain, cipher)
            i = input(
                "\n\n\n-------------------------------------------------\ntype enter for another try  / exit to finish "
            )
            if i == "exit":
                break
