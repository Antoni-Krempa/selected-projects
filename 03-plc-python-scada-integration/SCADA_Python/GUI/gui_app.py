from pyodbc import connect
from tkinter import * 
import tkinter as tk
from Connections.sql_database import connection_string
from Connections.csv_database import load_data_from_csv, append_data_to_csv
from Connections.plc import connection
from Classes.data import Data
from Classes.data_bool import Data_bool
import pyodbc


#tworenie labeli
def initialize_label(master,client,variables_list):

    add_label = Label(master, text = f'Dodaj zmienną: ')
    add_label.grid(row = 0, column =  5, sticky = W, pady = 2)

    add_entry = Entry(master)
    add_entry.grid(row = 0, column = 6, pady = 2)

    add_entry.bind("<Button-1>", lambda event: save(add_entry, client, event))
    
    for variable in variables_list:
        variable.initialize()
    
#odświeżanie labeli
def update_label(master,client,conn):

    global variables_list, loaded_variables_count

    # Sprawdź czy pojawiła się nowa zmienna
    updated_list = load_data_from_csv("Data/Dane.csv", master, client, conn)
    if len(updated_list) > loaded_variables_count:
        variables_list = updated_list
        loaded_variables_count = len(variables_list)
        for variable in variables_list:
            if variable.label is None:
                variable.initialize()

    for variable in variables_list:
        variable.update()

    

    master.after(100, lambda: update_label(master, client, conn))

def save(entry,client,event=None):
    
    def approve(event=None):
            
        new_variable = entry.get()
        data_row = [x.strip() for x in new_variable.split(",")]

        
        try:
            test_obj = Data(
                type=data_row[0],
                DB_number=int(data_row[1]),
                start_byte=int(data_row[2]),
                byte_length=int(data_row[3]),
                
                name=data_row[5],
                unit=data_row[6],
                row = 0,
                column= 0,
                mode=data_row[7]
                )
            # Testowy odczyt – jeśli tu wywali, nie zapisujemy
            _ = client.db_read(test_obj.DB_number, test_obj.start_byte, test_obj.byte_length)

        except Exception as e:
            print(f"Błąd przy testowaniu zmiennej: {e}")
            return


        append_data_to_csv("Data/Dane.csv", data_row)
        entry.delete(0, tk.END)
            
    entry.bind("<Return>", approve)
    entry.focus()

    

def app_loop():

    
    client = connection()
    connection_string1 = connection_string()
    conn = pyodbc.connect(connection_string1)

    master = Tk()

    #Opcje okna
    master.title("SCADA")
    master.configure(background="yellow")
    master.minsize(800, 1050)
    master.maxsize(800, 1400)
    master.geometry("300x300+50+50")

    #inicjacja zmiennych z DB
    global variables_list, loaded_variables_count
    variables_list = load_data_from_csv("Data/Dane.csv", master, client, conn)
    loaded_variables_count = len(variables_list)


    initialize_label(master,client,variables_list)
    update_label(master,client,conn)


    master.mainloop()
    conn.close()