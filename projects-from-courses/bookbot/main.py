import string
from stats import word_count,character_count,list_of_dictonaries,print_report,word_count2
import sys


def get_book_test(path):
    with open(path,encoding='utf-8') as f:
        content = f.read()
    return content




def main():

    try:
        path = sys.argv[1]
    except:
        print('Usage: python3 main.py <path_to_book>')
        sys.exit(1)
     
    book_text =  get_book_test(path)
    word_count(book_text)

    char_count = character_count(book_text)
    print(list_of_dictonaries(char_count))
    word_count1 = word_count2(book_text)
    print_report(word_count1,char_count,path)
        



main()