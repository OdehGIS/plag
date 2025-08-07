ciphertext=input("Enter the Cipher Text: ")
def decrypt_caesar(ciphertext):
    for shift in range(1, 26):
        decrypted = ''
        for char in ciphertext:
            if char.isalpha():
                shifted = chr((ord(char.upper()) - 65 - shift) % 26 + 65)
                decrypted += shifted
            else:
                decrypted += char
        print(f"Shift {shift}: {decrypted}")
      
    
decrypt_caesar(ciphertext)


