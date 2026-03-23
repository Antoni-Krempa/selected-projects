import string

def word_count(text):
    count = len(str.split(text))
    print(f'{count} words found in the document')

def character_count(text):
    dict = {}
    for letter in text.lower():
        if letter not in dict:
            dict[letter] = 1
        else:
            dict[letter] += 1

    return dict

def sort_function(i):
    return i['num']

def word_count2(text):
    count = len(str.split(text))
    return count



def list_of_dictonaries(dict):
    list = [{'char':letter, 'num':count} for letter,count in dict.items()]
    list.sort(reverse = True,key = sort_function)

    return list

def print_report(word_count,char_count,path):
    print('============ BOOKBOT ============')
    print(f'Analyzing book found at {path}...')
    print('----------- Word Count ----------')
    print(f'Found {word_count} total words')
    print('--------- Character Count -------')
    for dict in list_of_dictonaries(char_count):
        if dict['char'].isalpha():
            print(f'{dict["char"]}: {dict["num"]}')
        else:
            continue
    print('============= END ===============')

    
    