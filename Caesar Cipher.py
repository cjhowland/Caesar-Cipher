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



# Testing
if __name__ == '__main__':
    plaintext = Message('Happy Birthday!')
    print(plaintext.get_message_text())
    print(plaintext.apply_shift(1))
    print(plaintext.apply_shift(18))

