import sys
from pathlib import Path
from unidecode import unidecode
import string
import unicodedata
from operator import itemgetter
from string import ascii_uppercase

### ENCRYPTER and DECRYPTER ###

def encrypter(mensagem, senha):
    res = ""
    for i in range(0, len(mensagem)):
        ord_char_msg = ord(mensagem[i]) - ord('A')
        ord_char_sen = ord(senha[i%len(senha)]) - ord('A')
        res = res + chr( ((ord_char_msg + ord_char_sen) % 26) + ord('A') )
    return res

def decrypter(criptograma, senha):
    res = ""
    for i in range(0, len(criptograma)):
        ord_char_crip = ord(criptograma[i]) - ord('A')
        ord_char_sen = ord(senha[i%len(senha)]) - ord('A')
        res = res + chr( ((ord_char_crip - ord_char_sen +26) % 26) + ord('A') )
    return res

### FREQUENCY-BASED ATTACK ###

PT_LETTERS_FREQUENCY = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57, 'F': 1.02,
    'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40, 'K': 0.02, 'L': 2.78,
    'M': 4.74, 'N': 5.05, 'O': 10.73, 'P': 2.52, 'Q': 1.20, 'R': 6.53,
    'S': 7.81, 'T': 4.34, 'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21,
    'Y': 0.01, 'Z': 0.47
}

EN_LETTERS_FREQUENCY = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

def file_to_clean_string(path):
    res = ""
    f = open(path, encoding="utf-8")
    text = f.read()
    f.close()
    text = unicodedata.normalize("NFD", text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    for c in text:
        if c.isalpha():
            res = res+c.upper()
    return res

def index_of_coincidence(text):
    size = len(text)
    char_occurences = {c: text.count(c) for c in text}
    sum = 0
    for c in char_occurences:
        occurence = char_occurences[c]
        sum = sum + occurence*(occurence-1)
    return sum / (size*(size-1))

def best_keylength_guesses(encrypted_text, max_keylength_size=10):
    res = []
    for keylength in range(1, max_keylength_size):
        slices = []
        for i in range(keylength):
            slices.append(encrypted_text[i::keylength])
        ic_of_slices = [index_of_coincidence(s) for s in slices]
        sum_of_ic_of_slices = 0
        for ic in ic_of_slices:
            sum_of_ic_of_slices += ic
        average_ic = sum_of_ic_of_slices / keylength
        res.append([keylength, average_ic])
    res = sorted(res, key=itemgetter(1), reverse=True)
    return res

def best_shift(slice, letters_frequency):
    size_of_slice = len(slice)
    min_chi2 = float('inf')
    best_shift_value = 0
    
    if size_of_slice == 0:
        return 0

    for shift in range(0,26):
        shifted_slice = ""
        for c in slice:
            shifted_c = (ord(c)-ord('A')-shift) % 26
            shifted_slice = shifted_slice + chr(shifted_c+ord('A'))
        occurrence_num_of_shifted_slice = {c: shifted_slice.count(c) for c in ascii_uppercase}
        expected_occurrence_num = {c: (letters_frequency[c]*size_of_slice)/100 for c in ascii_uppercase}

        chi2 = 0 
        for c in ascii_uppercase:
            actual_c_occurrence_num = occurrence_num_of_shifted_slice[c]
            expected_c_occurrence_num = expected_occurrence_num[c]
            if expected_c_occurrence_num > 0:
                chi2 = chi2+ (  ((actual_c_occurrence_num - expected_c_occurrence_num)**2)
                        / expected_c_occurrence_num   )
        if chi2< min_chi2:
            best_shift_value = shift
            min_chi2 = chi2

    return best_shift_value

def get_key(encrypted_text, keylength, letters_frequency):
    key = ''
    for i in range(0,keylength):
        slice = encrypted_text[i::keylength]
        best_shift_value = best_shift(slice, letters_frequency)
        key = key + chr(best_shift_value + ord('A'))
    return key


def main():
    if(sys.argv[1] == 'encrypt'):
        print(encrypter(sys.argv[2], sys.argv[3]))
    elif(sys.argv[1] == 'decrypt'):
        print(decrypter(sys.argv[2], sys.argv[3]))
    elif(sys.argv[1] == 'get_key'):
        print("Encrypting file...")
        clean_string = file_to_clean_string(sys.argv[2])
        encrypted_string = encrypter(clean_string, sys.argv[3])
        print("Guessing key...")
        keylength_guesses = best_keylength_guesses(encrypted_string)

        if(sys.argv[4] == 'PTBR'):
            letters_frequency = PT_LETTERS_FREQUENCY
        elif(sys.argv[4] == 'EN'):
            letters_frequency = EN_LETTERS_FREQUENCY

        key = get_key(encrypted_string, keylength_guesses[0][0], letters_frequency)
        print("Guesses key: "+key)

        print("### DECRYPTED TEXT ###")
        print(decrypter(encrypted_string, key))


main()