# UID: 180128022

# Importing Pickle module
import pickle
import time
import sys

# Creating a class that has all the methods
class decompressorHuffman:
    def __init__(self, dictionary_decompress, codearray_decompress): # .pkl and .bin as arguments
        self.dictionary_decompress = dictionary_decompress
        self.codearray_decompress = codearray_decompress
        self.replacer = self.codearray_decompress.replace(".bin", "")
    
    def dictionary_reader(self): # "Pickle" to read data from dictionary
        dictionary_decompressed = open(self.dictionary_decompress, "rb")
        dictionary_decompressed = pickle.load(dictionary_decompressed)
        self.dictionary_decompressed = dictionary_decompressed
        
    
    def array_reader(self): # Reading the compressed file
        codearray_decompressed = open(self.codearray_decompress, "rb")
        codearray_decompressed = codearray_decompressed.read()
        self.codearray_decompressed = codearray_decompressed
        
    
    def binary_converter(self): # For binary operations
        final_binary_string = ""
        for byte in self.codearray_decompressed:
            binary_string = bin(byte)
            binary_string = binary_string[2:] # Removing the first two characters in a string
            pad = ""
            for zero in range(0, 8 - len(binary_string)):
                pad += "0" # Zero padding
            binary_string = pad + binary_string
            final_binary_string += binary_string
        self.final_binary_string = final_binary_string

    def decoder(self): # For getting the original string
        decoded_string = ""
        # Swapping the keys and values
        final_reversed_dictionary = dict((value, key) for key, value in self.dictionary_decompressed.items())
        check = ""
        for digit in self.final_binary_string:
            check += digit
            # Try/Catch block to handle the error
            try:
                sym = final_reversed_dictionary[check]
                decoded_string += sym
                check = ""
            except KeyError:
                continue
        # Writing the decompressed original string to a new file
        file = open("{}-decompressed.txt".format(self.replacer), "w")
        file.write(decoded_string.replace("EOF","")) # Removing the End-of-File marker
        file.close()
        

timer_start = time.clock()
# From test-harness.py
arg_one = sys.argv[0] 
arg_two = sys.argv[1]
new_arg_two = arg_two.replace(".bin", "") 
# Creating instance of the class
search = decompressorHuffman("{}-symbol-model.pkl".format(new_arg_two), arg_two)
dict_reader = search.dictionary_reader()
arr_reader = search.array_reader()
converter = search.binary_converter()
decoder = search.decoder()
timer_stop = time.clock()
print("The time (in sec) taken for decoding the compressed file: ", timer_stop-timer_start)