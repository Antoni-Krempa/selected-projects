import snap7
from snap7.util import get_real, set_real, get_bool, set_bool
import tkinter as tk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Classes.data import Data




class Data_bool(Data):

    def __init__(self, type,DB_number, start_byte, byte_length, bit_number, name: str, unit: str, row, column, mode = 'r', show_plot = True, master=None, client=None, conn=None): 
        super().__init__(type,DB_number, start_byte, byte_length, name, unit, row, column, mode, show_plot, master, client, conn)
        self.bit_number = bit_number
        self.previous_value = 0.5
        self.plot_y_1 = -0.2
        self.plot_y_2 = 1.2

    def read_value(self, data):
        return get_bool(data, 0, self.bit_number)

    def custom_initialize_appearance(self):
        if self.value:
            self.label.config(bg="green")
        else:
            self.label.config(bg="red")
    

    def write(self,value):
        if self.mode == 'rw' or self.mode == 'w':
            data = self.client.db_read(self.DB_number, self.start_byte, self.byte_length)
            set_bool(data, 0, self.bit_number, bool(value))
            self.client.db_write(self.DB_number, self.start_byte, data) #start_byte == offset??
        else:
            pass

    def edit(self, event=None):
    
        data = self.client.db_read(self.DB_number, self.start_byte, self.byte_length)
        value = get_bool(data,0,self.bit_number)
        

        if value:
    
            self.write(False)
        else:
    
            self.write(True)


    def send_to_database(self):

        if self.previous_value != self.value:

            self.previous_value = self.value
       
            cursor = self.conn.cursor()
            # przygotuj dane
            Time = datetime.now()
            Tag_name = self.name
            wartosc = float(self.value)
            unit = self.unit
            type1 = self.type

            # zapytanie INSERT
            cursor.execute("INSERT INTO Dane_skrypt_2 (Time, Tag_name, Value, unit, type) VALUES (?, ?, ?, ?, ?)", (Time, Tag_name, wartosc, unit, type1))
            self.conn.commit()  # WAŻNE: zatwierdzenie transakcji

            print("Dane zostały dodane.")