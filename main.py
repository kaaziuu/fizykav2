import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
is_run = True

all_commend = [
    'predkosc detektora',
    'odleglosc pr',
    'wiele pomiarow',
    'kierunek',
    'wielkosc',
    'fala',
    'dodaj osr',
    'usun osr',
    'exit'
]
all_center = {}

# ładownie z pamięci wszykich osrodków
with open('save.json', 'r') as f:
    read = f.read()
    all_center = json.loads(read)


# podanie osrodka
def enter_center():
    print(all_center)
    center = input("podaj osrodek: ")
    is_good = True
    # sprawdzenie czy mamy zapisany taki osrodek
    if center in all_center.keys():
        center = all_center[center]
    else:
        try:
            center = float(center)
        except:
            print("nie ma takiego osrodka")
            is_good = False
    return center, is_good


# dodawnie osrodka
def add_center():
    global all_center
    name = input("podaj nazwe osrodka: ")
    name = name.strip(" ")
    speed = float(input("podaj predkosc fali w osrodku: "))
    if not name in all_center.keys():
        all_center[name] = speed

        with open('save.json', 'w') as f:
            json_tab = json.dumps(all_center)
            f.write(json_tab)


# usuwanie osrodka
def remove_center():
    print(all_center)
    name = input("podaj nazwe osrodka ktorego chcesz usunac: ")
    if name in all_center.keys():
        del all_center[name]

        with open('save.json', 'w') as f:
            json_tab = json.dumps(all_center)
            f.write(json_tab)


# obliczanie predkosci detektora/sluchacza
def detector_speed():
    # podanie osrodka
    center, is_good = enter_center()

    #podanie czestotliwosci
    try:
        f = float(input("Podaj czestotliwosc emisji: "))
        f1 = float(input("podaj czestotliwosc zwrotną: "))
    except:
        print('blad w podawaniu danych')
        is_good = False

    # jesli dane sa dobre to obliczenie predkosci oraz wypisanie wyniku
    if is_good:
        v0 = (center*f1)/f-center
        print(v0)


# oblicza odlegosc w prostym przypadku
def how_far(center=None, t=None, print_it=True):
    is_good = True
    if not center:
        center, is_good = enter_center()
    if not t:
        t = float(input("czas powrodu fali: "))

    if is_good:
        dis = center * (t/2)
        if print_it:
            print(dis)
        else:
            return dis

# robienie wiele pomiarow
def multi_calc():
    how_many = int(input("podaj ilosc pomiarow: "))
    wave = float(input("podaj okres fali: "))
    distance_arr = []
    speed_arr = []
    center, good = enter_center()
    old_time = None
    current_time = None
    for i in range(how_many):
        old_time = current_time
        current_time = float(input("podaj czas powrotu fali: "))
        distance_arr.append(how_far(center, current_time, False))
        if old_time:
            rt = -old_time/2 + wave + current_time/2
            speed = (distance_arr[i-1] - distance_arr[i]) / rt
            speed_arr.append(speed)
        else:
            speed_arr.append(None)

    data = pd.DataFrame({"odleglosc": distance_arr, 'predkosc': speed_arr})
    print(data)

# wykres fali
def wave_mt():
    x = np.arange(0, 3, 0.01)
    y = np.sin(4*np.pi*x)
    plt.plot(x, y)
    plt.show()

def direction():
    center, ok = enter_center()
    DT = float(input("Podaj różnice w czasie: "))
    dis = float(input("podaj odleglosc miedzy lewym a prawym detektorem: "))
    # obliczenie sin
    sina = (DT*center)/dis
    # zamiana sinus na kąt
    degrees = np.degrees(sina)
    print(degrees)

def size():
    p0 = float(input("podaj natężenie początkową: "))
    pe = float(input("podaj netężenie jakie wróciło: "))
    r = float(input("podaj odlegosc: "))
    s = (pe*4*np.pi*r**2)/p0
    print(s)

# główna pętla
while is_run:
    # wypisanie wszytkich komend
    print(all_commend)
    command = input("co mam robić: ")
    try:
        command = int(command)
        command = all_commend[command]
    except:
        pass

    if command in all_commend:
        if command == 'exit':
            is_run = False

        if command == 'predkosc detektora':
            detector_speed()

        if command == 'dodaj osr':
            add_center()

        if command == 'odleglosc pr':
            how_far()

        if command == 'usun osr':
            remove_center()

        if command == 'wiele pomiarow':
            multi_calc()

        if command == 'fala':
            wave_mt()

        if command == 'kierunek':
            direction()
        if command == 'wielkosc':
            size()