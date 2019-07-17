# UID: 180128022

# Importing all the modules
import re
import operator
import array
import pickle
import sys
import getopt
import time

# Creating a class for arguments from commandline

class cmd:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:], "s") # Referenced from ir_engine.py
        opts = dict(opts)
        self.exit = True   
        
        if "-s" in opts:
            self.model = "word" # For word
            self.model = "char" # For character
                  
# Creating a Node for Huffman Implementation
class nodeHuffman:
    def __init__(self, probvalue, stringvalue):
        self.rootnode = None
        self.probvalue = probvalue
        self.left = None
        self.right = None
        self.stringvalue = stringvalue
        
# Creating a class for every other method        
class codeHuffman:
    def __init__(self, infile): # For opening the file and reading it
        self.infile = infile # Used to remove the .txt for .pkl to run against test-harness.py
        self.replacer = self.infile.replace(".txt", "")
        self.filename = open(infile) 
        self.filename = self.filename.read()
        
    
    def letter_count(self): # For finding out individual characters
        file = self.filename
        individualWord = re.findall(r"[a-zA-Z]|[^A-Za-z]", file) # For RegEx operation
        charDict = {}
        for char in individualWord: 
            if char in charDict: 
                charDict[char] += 1 # If found, add to the count
            else:
                charDict[char] = 1 # If not found, put 1 against it
        char_dict = {}
        for char, freq in charDict.items():
            char_dict[char] = freq
            self.word_dict = char_dict
            self.word_dict["EOF"] = 1 # Defining the End-of-File
        self.individualWord = individualWord
        return self.word_dict, self.individualWord 
        
    
    def word_count(self): # Similar operations as above for individual words
        file = self.filename
        individualWord = re.findall(r"[a-zA-Z]+|[^A-Za-z]", file)
        wordDict = {}
        for word in individualWord:
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1
        word_dict = {}
        for words, freq in wordDict.items():
            word_dict[words] = freq
            self.word_dict = word_dict
            self.word_dict["EOF"] = 1
        self.individualWord = individualWord
        
        return self.word_dict, self.individualWord  

    
    def tree_Huffman(self): # For creating a tree
        tree = []
        # Sorting in increasing order of frequencies
        self.sorted_wd = dict(sorted(self.word_dict.items(), key=operator.itemgetter(1)))
        self.sorted_wd = [(key, value/sum(self.sorted_wd.values())) for key, value in self.sorted_wd.items()]
        # Running an iteration for appending strings and probabilities
        for i in self.sorted_wd:
            tree.append(nodeHuffman(i[1],i[0]))
        leaf_nodes = []
        while(len(tree)!=1):
            # Extracting two elements with the lowest frequencies
            first_element = tree.pop(0)
            second_element = tree.pop(0)
            # Mapping parent-child
            combination = nodeHuffman(first_element.probvalue + second_element.probvalue, "rootnode")
            first_element.rootnode = combination
            second_element.rootnode = combination
            combination.left = first_element
            combination.right = second_element
            tree.append(combination)
            # Re-sorting, based on combined frequencies
            self.sorted_tree = sorted(tree, key = operator.attrgetter("probvalue"))
            # Finding out first and second elements
            if (first_element.stringvalue != "rootnode"):
                leaf_nodes.append(first_element)
            if (second_element.stringvalue != "rootnode"):
                leaf_nodes.append(second_element)
        # Code block to assign "0" or "1"
        dictionary = {}
        for x in leaf_nodes:
            code = ""
            nonupdatedstring = x.stringvalue # Saving the value to a variable before updating
            while(True):
                if x.rootnode == None:
                    break
                else:
                    if x.rootnode.left == x:
                        code += "1"
                    else:
                        code += "0"
                    x = x.rootnode
            dictionary[nonupdatedstring] = code[::-1] # We are reverse-traversing
        # Writing the file using Pickle
        file = open("{}-symbol-model.pkl".format(self.replacer), "wb") 
        pickle.dump(dictionary, file)
        file.close()
        self.dictionary = dictionary
        return(self.dictionary)     
                  
    
    def encoder(self): # Encoding the string 
        final_string = ""
        for sym in self.individualWord:
            final_string += self.dictionary[sym]
        final_string += self.dictionary["EOF"] # Adding End-of-File for decoding later-on
        self.final_string = final_string
        return self.final_string
            
    def bit_func(self): # Construction of proper binary representation
        codearray = array.array("B")
        length = (8 - len(self.final_string)%8) # For finding out the number of zeros to be added
        for bit in range(0, length):
            self.final_string += "0"
        for bit in range(0, len(self.final_string), 8):
            c = self.final_string[bit:bit+8]
            codearray.append(int(c,2)) # Integer base 2 representation
        self.codearray = codearray
        # For writing compressed symbol model text to a file
        file = open("{}.bin".format(self.replacer), "wb")
        codearray.tofile(file)
        file.close()
        
# MAIN
if __name__ == "__main__":
    
    config = cmd()
    # from test-harness.py
    arg_one = sys.argv[2] 
    arg_two = sys.argv[3]
    search = codeHuffman(arg_two)
    if config.model == arg_one:
        dictionary_char, indi_words = search.letter_count()
    else:
        dictionary_words, indi_words = search.word_count()
    timer_start = time.clock()
    dictionary_tree = search.tree_Huffman()
    timer_stop = time.clock()
    print("The time (in sec) taken for building the symbol model: ", timer_stop-timer_start)
    timer_start = time.clock()
    dictionary_encoder = search.encoder()
    dictionary_bit = search.bit_func()
    timer_stop = time.clock()
    print("The time (in sec) taken for encoding the input file given the model: ", timer_stop-timer_start)