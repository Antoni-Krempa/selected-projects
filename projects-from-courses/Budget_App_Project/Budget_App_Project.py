import math

class Category:

    def __init__(self,name):
        self.name = name
        self.ledger = []
        self.sum_amount = 0
        

    def deposit(self, amount, description=""):
        self.sum_amount += amount
        return self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self,amount,description=""):
        if self.check_funds(amount):
            self.sum_amount -= amount
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False

    def get_balance(self):
        return self.sum_amount

    def transfer(self,amount,budget_category):
        if self.check_funds(amount):
            self.withdraw(amount,f'Transfer to {budget_category.name}')
            budget_category.deposit(amount,f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self,amount):
        if self.sum_amount < amount:
            return False
        else:
            return True
        

    def gwiazdki(self,name):
        dl = len(self.name)
        return math.ceil((30-dl)/2)

    def napis(self):

        gwiazdki = self.gwiazdki(self.name) * '*'
        glowny_string = ''
        nazwa_kategorii = self.name
        ilosc_spacji = 0
        total = 0


        for slownik in self.ledger:
            ilosc_spacji = 30 - (len(slownik.get('description',0)[:23]) + len(f"{slownik.get('amount',0):.2f}"))        

            glowny_string += slownik.get('description',0)[:23] + ilosc_spacji*' ' + f"{slownik.get('amount',0):.2f}" + '\n' 

            total += slownik.get('amount',0)

        total = round(total,2)
        
        result = gwiazdki + nazwa_kategorii + gwiazdki + '\n' + glowny_string + 'Total: '  + f"{total:.2f}"

        return result

    def __str__(self):
        result = self.napis()


        return result 




def create_spend_chart(categories):

    sum_money = 0
    sum_category = []
    percent_category = []
    string = ''
    circles = []
    final = ''
    
    #Obliczanie procentów
    for category in categories:
        temporary = 0
        for slownik in category.ledger:
            if slownik.get('amount') < 0:
                temporary += slownik.get('amount')
            else:
                continue
        sum_category.append(temporary)

    sum_money = sum(sum_category)

    for category in sum_category:
        percent_category.append(math.floor(((category*10)/sum_money)))
        

    


    

    len_percent_category = len(percent_category)

    #Tworzenie kółeczek
    for wiersz in range (11):
        temporary2 = ''
        for kolumna in range (len_percent_category):
            if percent_category[kolumna] >= wiersz:
                temporary2 += ' o '
            else:
                temporary2 += '   '
        circles.append(temporary2)
            
    #kółeczka + kolumna procentów         
    for i in range (11):
        string += f"{'' if i == 0 else ' ' if i!=10 else '  '}{100-i*10}|{circles[10-i]} \n"


    category_names = []
    category_names_wiersz = []
    #Tworzenie listy z nazwami kont
    for category in categories:
        temporary3 = []
        
        for i in range (len(category.name)):
            temporary3.append(category.name[i])
        category_names.append(temporary3)


    longest_category = 0

    #Wyznaczanie dlugosci najdłuższej nazwy
    for category in categories:
        if len(category.name) > longest_category:
            longest_category = len(category.name)
        else:
            continue

    #Tworzenie nazw kolumnowych
    for wiersz in range (longest_category):
        temporary4 = ''
        for kolumna in range (len_percent_category):
            try:
                if category_names[kolumna][wiersz]:
                    temporary4 += f" {category_names[kolumna][wiersz]} "
                else:
                    temporary4 += '   '
            except:
                temporary4 += '   '
        category_names_wiersz.append(temporary4)

    #Łączenie nazw kolumnowych     
    string2 = ''
    for i in range(longest_category):
        newline = '\n' if i != longest_category-1 else ''
        string2 += f"    {category_names_wiersz[i]} {newline}"   
        

    #Całość razem
    final = "Percentage spent by category\n" + string + f"    {(len(circles[1])+1)*'-'}" + '\n' + string2



    return  str(final)


#przykład użycia
food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
auto = Category('Auto')
auto.deposit(1000, 'deposit')
auto.withdraw(500, 'repair')

print(food)

lista_kont = [clothing, food,auto]
print(create_spend_chart(lista_kont))