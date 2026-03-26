import csv
from Classes.data_bool import Data_bool
from Classes.data import Data


def load_data_from_csv(filename,master, client, conn):
    data_objects = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i,row in enumerate(reader):
            obj_type = row.get('type').strip().lower()
            DB_number = int(row['DB_number'])
            start_byte = int(row['start_byte'])
            byte_length = int(row['byte_length'])
            name = row['name']
            unit = row['unit']
            mode = row.get('mode', 'r').strip() # domyślnie 'r' jeśli brak
            value = row.get('show_plot', '').strip()
            show_plot = bool(int(value)) if value.isdigit() else True
            if obj_type == 'bool':
                bit_number = int(row['bit_number'])
                data_objects.append(Data_bool(obj_type,DB_number, start_byte, byte_length, bit_number, name, unit, i, 0, mode, show_plot, master = master, client = client, conn =conn))
            else:
                data_objects.append(Data(obj_type,DB_number, start_byte, byte_length, name, unit, i, 0, mode, show_plot, master = master, client = client, conn =conn))
    return data_objects



def append_data_to_csv(filename, data_row):
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_row)
