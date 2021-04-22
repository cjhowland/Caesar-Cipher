import string

class Message(object):
    '''
    A type with methods to display and change the plaintext message, create a shifted dictionary, and apply a shift to encode the message.
    
    Example Usage:
    >>> plaintext = Message('Happy Birthday')
    >>> msg.get_message_text()
    'Happy Birthday!'
    >>> msg.apply_shift(1)
    'Ibqqz Cjsuiebz!'
    >>> msg.apply_shift(18)
    'Zshhq Tajlzvsq!'
    '''

    def __init__(self, text):
        '''
        Initializes an object of type Message.

        Inputs:
            - text (string): the text of the message (can include punctuation)
        '''
        self.text = text

    def __repr__(self):
        '''
        Textual representation of the object which could be used to recreate the object.
        '''
        return f'{self.text}'

    def get_message_text(self):
        '''
        Used to safely access the data attribute message_text outside of the class.

        Outputs:
            - message_text (string)
        '''
        return self.text

    def change_message_text(self, new_text):
        '''
        Setter method to safely update and change the text of a message.

        Input:
            - new_text (string): new text to change the message to
        '''
        self.text = new_text


    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to shift each plaintext letter by a fixed value. Letters remain in their
        original case, and those shifted beyond the end of the alphabet wrap to the beginning of the alphabet.

        Input:
            - shift (int): The amount by which to shift every letter in the alphabet.
        Output:
            - (dict): maps every letter (string) to another letter (string)
        '''
        alphabet_lower = list(string.ascii_lowercase)*2     # list of lowercase letters (doubled for wrap-around shifts beyond z)
        alphabet_upper = list(string.ascii_uppercase)*2     # list of uppercase letters (doubled for wrap-around shifts beyond Z)
        alphabet_dict = {letter:alphabet_lower[n+(shift%26)] for n, letter in enumerate(string.ascii_lowercase)}        # dictionary assigning each lowercase letter to its corresponding shifted letter
        alphabet_dict.update({letter:alphabet_upper[n+(shift%26)] for n, letter in enumerate(string.ascii_uppercase)})  # updated with dictionary assigning each uppercase letter to its corresponding shifted letter
        return alphabet_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the shift amount
        given by "shift". Returns a new string of the encrypted message.

        Input:
            - shift (int): The amount by which to shift every letter in the
                message.
        Output:
            - (string): The message text with all letters shifted by the
                desired amount.
        '''
        dict_shifted = Message.build_shift_dict(self.text,shift)  # call function to create shifted dictionary
        cipher = ''                                               # define an empty string in which to place the encoded message
        for i in range(len(self.text)):
            if self.text[i] in dict_shifted:                      # if the given character is a letter, add its corresponding 
                cipher += str(dict_shifted[self.text[i]])         #     shifted letter to the empty string
            else:
                cipher += str(self.text[i])                       # if the given character is not a letter (i.e. punctuation),
        return cipher                                             #     add it to the encoded message string as is




class PlainMsg(Message):
    '''
    This subclass focuses on converting plaintext messages into encrypted messages and easily modifying the content.

    Example Usage:
    >>> msg = PlainMsg('Hello, World!', 5)
    >>> print(msg.get_encrypted_msg())
    # 'Mjqqt, Btwqi!'
    >>> msg.change_shift(23)
    >>> print(msg.get_encrypted_msg())
    # 'Ebiil, Tloia!'
    '''

    def __init__(self, text, shift):
        '''
        Initializes a PlainMsg type object, inheriting from the Message parent class.

        Inputs:
            - text (string): the plain message text
            - shift (int): the amount the encrypted message to to be shifted

        A PlainMsg object inherits from Message and has 4 total attributes:
            - self.message_text (string, determined by input)
            - self.shift (integer, determined by input)
            - self.shift_dict (dictionary, created using shift)
            - self.encrypted_msg (string, created using shift)
        '''
        Message.__init__(self,text)
        self.message_text = text
        self.shift = shift
        self.shift_dict = Message.build_shift_dict(self,shift)
        self.encrypted_msg = Message.apply_shift(self,shift)

    def get_shift(self):
        ''' 
        Safely access the self.shift attribute outside the class.

        Outputs:
            - (integer): the value of self.shift
        '''
        return self.shift

    def change_shift(self, new_shift):
        '''
        Changes self.shift of the PlainMsg object and updates all other attributes which depend on self.shift.

        Input:
            - new_shift (integer): new value to shift all the letters by
        Output:
            - Nothing
        '''
        self.shift = new_shift
        self.shift_dict = Message.build_shift_dict(self,self.shift)
        self.encrypted_msg = Message.apply_shift(self,self.shift)

    def get_encrypted_msg(self):
        '''
        Safely acces the self.encrypted_msg attribute outside the class

        Outputs:
            - (string): the value of self.encrypted_msg
        '''
        return self.encrypted_msg





# Functions to accompany CipherMsg

def load_words():
    '''
    A function to import a dictionary of valid words with which to compare decrypted words.

    Outputs:
        - (list of strings): list of lowercase valid words
    '''

    f = open('words.txt', 'r')                                           # open text file containing word dictionary
    wordlist = []                                                        # initialize an empty list to which to append the words
    for line in f:                                                       # splits the letters between a space into a string,
        wordlist.extend([word.lower() for word in line.split(' ')])      #     converts all letters to lowercase, and adds all
    f.close()                                                            #     words to the empty list
    return wordlist                                                      # closes the file and returns the list of word strings


def get_words(phrase):
    '''
    Splits a phrase or sentence up into a list of individual words, removing all punctation.

    Input:
        - phrase (string): The string to be broken up into words
    Output:
        - (list of strings): list of the individual words without punctuation
    
    Example usage:
    >>> print(get_words("Hello! How are you today, ma'am?"))
    ['Hello', 'How', 'are', 'you', 'today', 'maam']
    '''
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)      # creates a list including both upper- and lowercase letters  
    phrase_list = []                                                            # initializes empty list to which to append striped words
    for i in phrase.split():                                                    # splits phrase into individual words
        character_list = list(i)                                                # converts word string into list of individual characters
        for n in range(len(character_list)):                                    # loops through all individual characters
            if i[n] not in alphabet:                                            # if statement to check if the character is a letter
                character_list.remove(i[n])                                     # if not a letter (puncuation), it is removed
        phrase_list.append(''.join(character_list))                             # appends the words stripped of punctuation to the empty list
    return phrase_list                                                          # returns the list of strings (words without punctuation)


def count_valid_words(potential_words, list_valid_words):
    '''
    Compares the list of potential words to the provided list of valid words, and returns a count of how many of the potential
    words are real words. Ensures that the capitalization of all words matches.

    Inputs:
        - potential_words (list of strings): list of the individual
            words to check if they are real words
        - list_valid_words (list of strings): list of valid words
            read in from the 'words.txt' file 
                - use (load_words())
    Output:
        - (integer): the number of words in potential_words which
            are found to be real valid words
    Example usage:
    >>> valid_words = load_words()
    >>> print(count_valid_words(['merkle', 'identity', 'tloia', 'decentralized'], valid_words))
    2
    '''
    counter = 0                                        # initializes counter at 0
    for word in potential_words:                       # loops through list of potential words from input
        if word.lower() in list_valid_words:           # searches for lowercase-converted word in list of valid words
            counter += 1                               # if the potential word matches an entry in the list of valid words, increases counter by 1
    return counter                                     # after checking all potential words, returns the sum total of the valid words






class CipherMsg(Message):
    '''
    This subclass focuses on decrypting ciphers by identifying the shift with the greatest number of valid words.

    Example Usage:
    >>> cipher_example = CipherMsg('Svnpj dpss nla fvb myvt H av G; pthnpuhapvu dpss nla fvb lclyfdolyl. - Hsilya Lpuzalpu')
    >>> print(cipher_example.decrypt_msg(load_words()))
    Logic will get you from A to Z; imagination will get you everywhere. - Albert Einstein
    '''

    def __init__(self, text):
        '''
        Initializes a CipherMsg object.

        Input:
            - text (string): The messages encrypted text

        A CipherMsg object inherits from Message and has 4 attributes:
            - self.message_text (string, determined from input)
            - self.is_decrypted (bool, initially False)
            - self.best_shift (integer, initially None)
            - self.decoded_msg (string, initially None)
        '''
        Message.__init__(self,text)
        self.text = text
        self.message_text = Message.get_message_text(self)
        self.is_decrypted = False
        self.best_shift = None
        self.decoded_msg = None


    def decrypt_msg(self, valid_words):
        '''
        Decryptes self.message_text by trying every possible shift value and finding the "best" one, where "best" here is the shift
        value that results in the greatest number of valid words found in the resulting decrypted message. If multiple shifts are
        equally "best", then any can be set as the decoded message.

        Updates the attributes of self.is_decrypted, self.best_shift, and self.decoded_msg after finding the best shift and decoding the message. 

        Input:
            - valid_words (list of string): the list of valid English words to compare potential messages to.
        Output:
            - (string): the decoded message string
        '''
        dictionary = load_words()                                           # loads in dictionary
        score = []                                                          # initializes empty list in which to append the 'score': the number of valid words resulting from each shift
        for i in range(26):                                                 # loops through all possible shifts (26)
            shifted_msg = Message.apply_shift(self, i)                      # uses apply_shift method to shift phrase by fixed integer given by i (between 0 and 26)
            shifted_msg_list = get_words(shifted_msg)                       # creates list of strings without punctuation of shifted phrase
            num = count_valid_words(shifted_msg_list, dictionary)           # counts the number of valid words in this shift
            score.append(num)                                               # appends the number of valid words for this shift to empty list
            
        self.best_shift = score.index(max(score))                           # identifies the shift value (given by the index) of the highest score
        self.decoded_msg =  Message.apply_shift(self, self.best_shift)      # applies the shift of the highest score
        self.is_decrypted = True                                            # changes is_decrypted switch to True!

        return self.decoded_msg                                             # returns the decoded message




def read_story(file_name):
    '''
    Reads in the file_name and outputs a string. Takes multiline files and stitches them back together in a single string with line-breaks
    embedded in the string.

    Input:
        - file_name (string): Name of file to read in
    Output:
        - (string): single string of entire file
    '''
    f = open(file_name, 'r')                                   # reads in the file
    lines = f.readlines()                                      # splits the text into separate lines
    f.close()                                                  # closes file
    return ''.join(lines)                                      # returns all items joined together in a string


def encode_story(plaintext_file, new_file_name, shift):
    '''
    Reads in a text file, shifts each letter by a given shift value, and saves the encoded message to a text file.

    Inputs:
    - plaintext_file (string): Name of file to read in
    - new_file_name (string): Name of new file to be created
    Outputs:
    - Nothing (saves the encoded message to a text file)
    '''
    listwords = Message(read_story(plaintext_file))                    # reads in the text file contents as a Message object
    encoded = listwords.apply_shift(shift)                        # applies the given shift
    encoded_txt = open(new_file_name, 'w')                        # opens new text file with writing capability 
    encoded_txt.write(encoded)                                    # writes the encoded message to the new file
    encoded_txt.close()                                           # closes the new file


def decode_story(cipher_file, new_file_name):
    '''
    Determines the proper shift necessary to decode the encrypted story. Writes the resulting decrypted story to the file 'decoded_story.txt'.

    Inputs:
        - cipher_file (string): name of the file to be decrypted
        - new_file_name (string): name of the new file in which to write the decrypted message
    Outputs:
        - None (saves a file with the decryped story)
    '''
    listwords = CipherMsg(read_story(cipher_file))              # reads in the text file as a CipherMsg object
    decoded = listwords.decrypt_msg(load_words())                  # uses the decrypt_msg function to decode the message
    decoded_txt = open(new_file_name, 'w')                         # opens new text file with writing capability
    decoded_txt.write(decoded)                                     # writes the decoded message to the new file
    decoded_txt.close()                                            # closes the new file




# Testing
if __name__ == '__main__':
    # test of the Message class
    plaintext = Message('Happy Birthday!')
    print(plaintext.get_message_text())
    # 'Happy Birthday!'
    print(plaintext.apply_shift(1))
    # 'Ibqqz Cjsuiebz!'
    print(plaintext.apply_shift(18))
    # 'Zshhq Tajlzvsq!'

    # test of the PlainMsg class
    msg = PlainMsg('Hello, World!', 5)
    print(msg.get_encrypted_msg())
    # 'Mjqqt, Btwqi!'
    msg.change_shift(23)
    print(msg.get_encrypted_msg())
    # 'Ebiil, Tloia!'

    # test of the get_words function
    print(get_words("Hello! How are you today, ma'am?"))
    # ['Hello', 'How', 'are', 'you', 'today', 'maam']

    # test of the count_valid_words function
    valid_words = load_words()
    print(count_valid_words(['merkle', 'identity', 'tloia', 'decentralized'], valid_words))
    # 2
    
    # test of the CipherMsg class
    cipher_example = CipherMsg('Svnpj dpss nla fvb myvt H av G; pthnpuhapvu dpss nla fvb lclyfdolyl. - Hsilya Lpuzalpu')
    print(cipher_example.decrypt_msg(load_words()))
    # Logic will get you from A to Z; imagination will get you everywhere. - Albert Einstein

    # test of decode_story function
    decode_story('EncodedCoverLetter.txt', 'DecodedCoverLetter.txt')
    # saves file titled 'DecodedCoverLetter.txt' with entire decoded message

