
def caesars_cipher(text, shift):
    return "".join([chr((ord(c) - 97 + shift) % 26 + 97) for c in text])

def reverse_caesars_cipher(text, shift):
    return "".join([chr((ord(c) - 97 - shift) % 26 + 97) for c in text])

def gen_primes(n) -> list[int]:
    # generates all primes up to n
    primes = []
    for i in range(2, n + 1):
        for j in range(2, i):
            if i % j == 0:
                break
        else:
            primes.append(i)
    return primes


if __name__ == "__main__":
    key = 3
    text = "abc"
    print(caesars_cipher(text, key))
    print(reverse_caesars_cipher(caesars_cipher(text, key), key))


    print(gen_primes(1000000))



'''
    a b c d e f g h i j k l m n o p q r s t u v w x y z

    
algorithm 

key 
'''

