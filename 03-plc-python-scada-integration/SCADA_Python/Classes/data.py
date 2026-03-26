
import snap7
from snap7.util import get_real, set_real, get_bool, set_bool
import tkinter as tk
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyodbc
from tkinter import * 


class Data():

    def __init__(self,type, DB_number, start_byte, byte_length, name: str, unit: str, row, column, mode = 'r', show_plot = True, master=None, client=None, conn=None): 
        self.type = type
        self.DB_number = DB_number
        self.start_byte = start_byte
        self.byte_length = byte_length
        self.name = name
        self.unit = unit
        self.row = row
        self.column = column
        self.mode = mode
        self.show_plot = show_plot
        self.name_label = None
        self.label = None
        self.entry = None
        self.value = None
        self.previous_value = 0.0
        self.plot_y_1 = -60
        self.plot_y_2 = 150
        self.master = master
        self.client = client
        self.conn = conn

        
    def read_value(self, data):
        return get_real(data, 0)
    
    def custom_initialize_appearance(self):
        pass


    def initialize(self):
        data = self.client.db_read(self.DB_number, self.start_byte, self.byte_length)
        value = self.read_value(data)

        
        self.name_label = Label(self.master, text = f'{self.name}: ')
        self.label = Label(self.master, text=f'{value:.2f} {self.unit}')
        
        self.name_label.grid(row = self.row, column =  self.column, sticky = W, pady = 2)
        self.label.grid(row = self.row, column = self.column + 1, sticky = W, pady = 2)

        history_label = Label(self.master, text = f'Wczytaj historię')
        history_label.grid(row = self.row, column =  4, sticky = W, pady = 2)
        history_label.bind("<Button-1>", self.load_history)

        self.custom_initialize_appearance()


        self.x_data = []
        self.y_data = []

        # wykres
        if self.show_plot:
            fig = Figure(figsize=(2.5, 1.5), dpi=100)
            self.ax = fig.add_subplot(111)
            fig.tight_layout()

        
            self.scatter_plot = self.ax.plot([], [])  # puste na start
            self.ax.set_ylim(self.plot_y_1, self.plot_y_2)
            self.ax.set_xlim(0, 500)  # np. ostatnie 20 pomiarów


            self.canvas = FigureCanvasTkAgg(fig, master=self.master)
            self.canvas.get_tk_widget().grid(row=self.row, column=self.column + 2, sticky=W, pady=2)
            self.canvas.draw()



        if self.mode == 'rw' or self.mode == 'w':
            
            self.label.bind("<Button-1>", self.edit)

    def update(self):
        data = self.client.db_read(self.DB_number, self.start_byte, self.byte_length)
        value = self.read_value(data)
        self.label.config(text=f'{value:.2f} {self.unit}')
        self.value = value

        self.custom_initialize_appearance()

        if self.show_plot:
            # dodaj nowy punkt
            if len(self.x_data) > 499:
                self.x_data = []
                self.y_data = []
            self.x_data.append(len(self.x_data))  # np. numer pomiaru
            self.y_data.append(value)

            # odśwież scattera
            self.ax.clear()
            self.ax.plot(self.x_data, self.y_data)
            self.ax.set_ylim(self.plot_y_1, self.plot_y_2)
            self.ax.set_xlim(0, 500)
        
            
            self.canvas.draw()

        self.send_to_database()

    
    def load_history(self, Event = None):
        history = Tk()

        #Opcje okna
        history.title(f"{self.name} history")
        history.configure(background="blue")
        history.minsize(600, 600)
        history.maxsize(800, 1400)
        history.geometry("300x300+50+50")

        cursor = self.conn.cursor()

        # Pobierz dane z bazy tylko dla danego tagu
        query = "SELECT Time, Value FROM Dane_skrypt_2 WHERE Tag_name = ? ORDER BY Time"
        cursor.execute(query, (self.name,))
        rows = cursor.fetchall()

        # Przygotuj dane do wykresu
        self.x = [row.Time for row in rows]
        self.y = [row.Value for row in rows]

        # Wykres
        self.fig1 = Figure(figsize=(7.5, 5), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1 .plot(self.x, self.y)
        self.ax1 .set_title(f'Historia: {self.name}')
        self.ax1 .set_xlabel('Czas')
        self.ax1 .set_ylabel(f'{self.unit}')

        self.fig1.autofmt_xdate()  # ładne daty na osi X

        # Osadź wykres w oknie Tkintera
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=history)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(fill='both', expand=True)

        edition_label = Label(history, text = f'Zmień zakres czasu (YYYY-MM-DD HH:MM:SS;YYYY-MM-DD HH:MM:SS)')
        edition_label.pack( pady = 2)


        self.edition_entry = Entry(history)
        self.edition_entry.pack( pady = 2)

        self.edition_entry.bind("<Return>", self.approve_data_plot)
        self.edition_entry.focus()

    
    def draw_plot(self,start_time, end_time):
        cursor = self.conn.cursor()
        query = """
            SELECT Time, Value FROM Dane_skrypt_2
            WHERE Tag_name = ? AND Time BETWEEN ? AND ?
            ORDER BY Time
        """
        cursor.execute(query, (self.name, start_time, end_time))
        rows = cursor.fetchall()

        # dane
        x = [row.Time for row in rows]
        y = [row.Value for row in rows]

        # aktualizacja wykresu
        self.ax1 .clear()
        self.ax1 .plot(x, y)
        self.ax1 .set_title(f'Historia: {self.name}')
        self.ax1 .set_xlabel('Czas')
        self.ax1 .set_ylabel(self.unit)
        self.fig1.autofmt_xdate()
        self.canvas1.draw()

    def approve_data_plot(self,event=None):
        try:
            time_range = self.edition_entry.get()
            start_str, end_str = [x.strip() for x in time_range.split(';')]
            start_time = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
            self.draw_plot(start_time, end_time)
        except Exception as e:
            print("Błąd parsowania zakresu czasu:", e)

    
    def write(self,value):
        if self.mode == 'rw' or self.mode == 'w':
            data = bytearray(4)
            set_real(data, 0, float(value))
            self.client.db_write(self.DB_number, self.start_byte, data) #start_byte == offset
        else:
            pass

    def edit(self, event=None):
        data = self.client.db_read(self.DB_number, self.start_byte, self.byte_length)
        value = get_real(data,0)
        self.entry = tk.Entry(self.master, font=("Arial", 16))
        self.entry.insert(0, str(value))
        self.entry.grid(row = self.row, column = self.column + 1, sticky = W, pady = 2)
        self.label.grid_forget()

        def approve(event=None):
            
            new_value = float(self.entry.get())
            self.write(new_value)
            self.label.config(text=f'{new_value:.2f} {self.unit}')
            self.entry.destroy()
            self.label.grid(row = self.row, column = self.column + 1, sticky = W, pady = 2)
            
        self.entry.bind("<Return>", approve)
        self.entry.focus()


    def send_to_database(self):

        if (abs(self.previous_value - self.value)) > 0.1:

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
