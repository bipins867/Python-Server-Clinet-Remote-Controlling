#Encoder
from collections import OrderedDict 
from re import sub
 
def encode(text):
    '''
    Doctest:
        >>> encode('WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW')
        '12W1B12W3B24W1B14W'    
    '''
    return sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1),
               text)
 
def decode(text):
    '''
    Doctest:
        >>> decode('12W1B12W3B24W1B14W')
        'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
    '''
    return sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)),
               text)

 
def runLengthEncoding(input): 

  
    # Generate ordered dictionary of all lower 
    # case alphabets, its output will be  
    # dict = {'w':0, 'a':0, 'd':0, 'e':0, 'x':0} 
    dict=OrderedDict.fromkeys(input, 0) 
    print(dict)
    # Now iterate through input string to calculate  
    # frequency of each character, its output will be  
    # dict = {'w':4,'a':3,'d':1,'e':1,'x':6} 
    for ch in input: 
        dict[ch] += 1
    print(dict)
    # now iterate through dictionary to make  
    # output string from (key,value) pairs 
    output = '' 
    for key,value in dict.items(): 
         output = output + key + str(value) 
    return output 
   
# Driver function 
if __name__ == "__main__": 
    input="wwwwaaadexxxxxx"
    print (runLengthEncoding(input)) 
