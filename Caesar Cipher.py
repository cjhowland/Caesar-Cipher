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
        alphabet_dict.update({letter:alphabet_upper[n+(shift%26)] for n, letter in enumerate(string.ascii_uppercase)})  # dictionary assigning each uppercase letter to its corresponding shifted letter
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
    This subclass focuses on converting plaintext messages into encrypted
    messages and easily modifying the content.

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
        Initializes a PlainMsg type object, inheriting from the Message parent class

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
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)      # create a list including both upper- and lowercase letters  
    phrase_list = []                                                            # initialize empty list to which to append striped words
    for i in phrase.split():                                                    # split phrase into individual words
        character_list = list(i)                                                # convert word string into list of individual characters
        for n in range(len(character_list)):                                    # loop through all individual characters
            if i[n] not in alphabet:                                            # if statement to check if the character is a letter
                character_list.remove(i[n])                                     # if not a letter (puncuation), it is removed
        phrase_list.append(''.join(character_list))                             # append the words striped of punctuation to the empty list
    return phrase_list                                                          # return the list of strings (words without punctuation)


def count_valid_words(potential_words, list_valid_words):
    '''
    Compares the list of potential words to the provided list of
    valid words, and returns a count of how many of the potential
    words are real words. Ensures that the capitalization of all
    words matches.

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
    counter = 0                                        # initialize counter at 0
    for word in potential_words:                       # loop through list of potential words from input
        if word.lower() in list_valid_words:           # search for lowercase-converted word in list of valid words
            counter += 1                               # if the potential word matches an entry in the list of valid words, increase counter by 1
    return counter                                     # after checking all potential words, return the sum total of the valid words





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
    

