def arithmetic_arranger(problems, show_answers=False):
    tab = []

    if len(problems) >5:
        return 'Error: Too many problems.'


    for problem in problems:
        for i in problem:
            if ( i.isdigit() or i == '+' or i == '-' or i == ' ' or i == '/' or i == '*'):
                continue
            else:
                return 'Error: Numbers must only contain digits.'
        
    
    for problem in problems:

        #podział na plus minus
        if '+' in problem:

            #podział stringa na części []
            x = problem.replace(' ','').split('+')

            #print(x)
            
            #sprawdzamy czy liczby są mniejsze niż 5
            if len(x[1]) >= 5 or len(x[0]) >= 5:
                return('Error: Numbers cannot be more than four digits.')

            #obliczenia do wyniku
            x1 = int(x[0])
            x2 = int(x[1])
            suma = str(x1 + x2)
            
            


            #podział na pół
            mid = len(x)//2

            
            
            #pomiar długości x1 x2
            length1 = len(x[1])
            length0 = len(x[0])

            #różnica długości x1 x2
            delta = abs(length1 - length0)

            
            if show_answers == False:
                
                #bez wyniku
                
                if length0 <= length1:
                    #skalowanie wyniku 
                    delta_wynik = (length1 + 2) - len(suma)
                    

                    new_problem = 2*[' '] + delta*[' '] + x[0:mid] + ['\n']+ ['+'] + [' '] + x[mid:]  + ['\n'] + (length1 + 2)*['-'] 
                else:
                    new_problem = 2*[' '] +  x[0:mid] + ['\n']+ ['+'] + delta*[' '] + [' '] + x[mid:] + ['\n'] + (length0 + 2)*['-']

            #z wynikiem
            else:
                if length0 <= length1:
                    #skalowanie wyniku 
                    delta_wynik = (length1 + 2) - len(suma)

                    new_problem = 2*[' '] + delta*[' '] + x[0:mid] + ['\n']+ ['+'] + [' '] + x[mid:] + ['\n'] + (length1 + 2)*['-'] + ['\n'] + delta_wynik*[' '] + [suma]
                else:
                    delta_wynik = (length0 + 2) - len(suma)
                    new_problem = 2*[' '] +  x[0:mid] + ['\n']+ ['+'] + delta*[' '] + [' '] + x[mid:] + ['\n'] + (length0 + 2)*['-'] + ['\n'] + delta_wynik*[' '] + [suma]
                    

            new_problem = ''.join(new_problem)
            
            tab.append(new_problem)
            
            
        elif '-' in problem:
            x = problem.replace(' ','').split('-')

           

            #sprawdzamy czy liczby są mniejsze niż 5
            if len(x[1]) >= 5 or len(x[0]) >= 5 :
                return('Error: Numbers cannot be more than four digits.')

            #obliczenia do wyniku
            x1 = int(x[0])
            x2 = int(x[1])
            różnica = str(x1 - x2)
            
            mid = len(x)//2
            
            length1 = len(x[1])
            length0 = len(x[0])

            delta = abs(length1 - length0)
            

            if show_answers == False:

                if length0 <= length1:
                    new_problem = 2*[' '] + delta*[' '] + x[0:mid] + ['\n']+ ['-'] + [' '] + x[mid:] + ['\n'] + (length1 + 2)*['-']
                else:
                    new_problem = 2*[' '] +  x[0:mid] + ['\n']+ ['-'] + delta*[' '] + [' '] + x[mid:] + ['\n'] + (length0 + 2)*['-']
            else:

                if length0 <= length1:
                    delta_wynik = (length1 + 2) - len(różnica)
                    new_problem = 2*[' '] + delta*[' '] + x[0:mid] + ['\n']+ ['-'] + [' '] + x[mid:] + ['\n'] + (length1 + 2)*['-'] + ['\n'] + delta_wynik*[' '] + [różnica]
                else:
                    delta_wynik = (length0 + 2) - len(różnica)
                    new_problem = 2*[' '] +  x[0:mid] + ['\n']+ ['-'] + delta*[' '] + [' '] + x[mid:] + ['\n'] + (length0 + 2)*['-'] + ['\n'] + delta_wynik*[' '] + [różnica]


            new_problem = ''.join(new_problem)
            #print(new_problem)
            
            tab.append(new_problem)
        
        elif '*' in problem or '/' in problem:
            return "Error: Operator must be '+' or '-'."
        
    

    #rozbijamy tab na wiersze i łączymy je ze spacjami        

    split_lines = [s.split('\n') for s in tab]
    
    max_lines = max(len(lines) for lines in split_lines)
    
    formatted_lines = []
    for i in range(max_lines):
        output = []
        for lines in split_lines:
            output.append(lines[i])

        formatted_lines.append("    ".join(output))

        
    return "\n".join(formatted_lines)
    


print(arithmetic_arranger(["32 + 8", "1 - 3801", "9999 + 9999", "523 - 49"], True))
