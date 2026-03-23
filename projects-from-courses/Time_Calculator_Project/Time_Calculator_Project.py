def add_time(start, duration, start_day = "False"):

    # definujemy zmienne
    start_minutes = 0
    start_hours = 0

    duration_minutes = 0
    duration_hours = 0

    
    # wyczytujemy godziny i minutry z duration i zamieniamy na int do obliczeń
    splited_duration = duration.split(":")

    duration_minutes = int(splited_duration[1])
    duration_hours = int(splited_duration[0])

    #wyczytujemy godziny i minuty początkowe i zamieniamy na int oraz sprawdzamy PM i AM 
    splited_start = start.split(":")
    minutes_string = splited_start[1]
    splited_start2 = minutes_string.split(" ")

    start_minutes =int(splited_start2[0]) 
    start_hours = int(splited_start[0])
    AM_PM = splited_start2[1]

    
    #jeśli PM to godziny początkowe +12
    if AM_PM == "PM":
        start_hours = start_hours + 12

    #dodajemy godziny startowe i godziny z duration
    new_hours = start_hours + duration_hours
    new_minutes = start_minutes + duration_minutes


    #dodajemy godzinę jeśli minuty wieksże niż 60
    if new_minutes >= 60:
        new_hours += 1
        new_minutes -= 60

    #obliczamy ilość dni
    days = new_hours // 24

    #obliczamy godzinę w danym dniu
    new_hours = new_hours % 24

    #zmienamy format minut na XX
    new_minutes = '%02d'% new_minutes

    #generujemy godzine w string i opisujemy wyjątki
    if new_hours > 13:
        new_hours -= 12
        new_time = str(new_hours) + ":" + str(new_minutes) + " PM"
    elif new_hours >= 12 and new_hours <13:
        new_time = str(new_hours) + ":" + str(new_minutes) + " PM"
    
    elif new_hours >= 0 and new_hours <1:
        new_hours = 12
        new_time = str(new_hours) + ":" + str(new_minutes) + " AM"

    else:
        new_time = str(new_hours) + ":" + str(new_minutes) + " AM"

    
    #słownik
    dni_tygodnia = {
        "Monday":0,
        "Tuesday":1,
        "Wednesday":2,
        "Thursday":3,
        "Friday":4,
        "Saturday":5,
        "Sunday":6
    }

    #jeśli podano dni tygodnia to obliczamy i generujemy
    if start_day != "False":
        #zmieniamy wejściową zmeinną żeby pasowała do słownika (case sensitivity)
        star_day_processed = start_day[0].upper() + start_day[1:].lower()

        #pozyskujemy liczbę dnia tygodnia
        start_day_number = dni_tygodnia[star_day_processed]
        
        end_day_number = 0
        end_day_number += days
        end_day_number += start_day_number
        end_day_number = end_day_number % 7
        
        #szukamy nazwę liczby dnia tygodnia w słowniku
        day_number = [i for i,j in dni_tygodnia.items() if j == end_day_number]

       #dodajemy dzień tygodnia do displaya
        new_time += ", " + day_number[0]



    #w zalężności ile dni upłynęło wypisujemy na disp
    if days == 1:
        new_time += " (next day)"
    elif days > 1:
        new_time += f" ({days} days later)"

    return new_time
 
 

print(add_time('3:30 PM', '22:12','Monday'))