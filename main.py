import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


def setup_database():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        gender TEXT,
        age INTEGER,
        smoke TEXT,
        yellow_fingers TEXT,
        pressure TEXT,
        chronic_disease TEXT,
        fatigue TEXT,
        allergy TEXT,
        vitiligo TEXT,
        alcohol TEXT,
        cough TEXT,
        dyspnea TEXT,
        swallowing TEXT,
        chest_pain TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()


setup_database()


def register():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Rejestracja", "Rejestracja zakończona sukcesem!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Błąd", "Użytkownik o takiej nazwie już istnieje!")

    conn.close()


def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM accounts WHERE username=?", (username,))
    stored_password = cursor.fetchone()

    conn.close()

    if stored_password and stored_password[0] == password:
        # Zalogowano pomyślnie
        messagebox.showinfo("Logowanie", "Zalogowano pomyślnie!")
        # Możesz teraz przejść do innej części aplikacji, np. wyświetlić formularz
        app_form()
        login_frame.destroy()
    else:
        messagebox.showerror("Błąd", "Nieprawidłowa nazwa użytkownika lub hasło!")


app = tk.Tk()
app.title("Logowanie")

login_frame = ttk.Frame(app)
login_frame.pack(padx=10, pady=10)

ttk.Label(login_frame, text="Nazwa użytkownika:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
username_entry = ttk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(login_frame, text="Hasło:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = ttk.Button(login_frame, text="Zaloguj", command=login)
login_button.grid(row=2, column=0, padx=5, pady=20)

register_button = ttk.Button(login_frame, text="Zarejestruj", command=register)
register_button.grid(row=2, column=1, padx=5, pady=20)


def app_form():
    def submit_form():
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO users (name, surname, gender, age, smoke, yellow_fingers, pressure, chronic_disease, fatigue, allergy, vitiligo, alcohol, cough, dyspnea, swallowing, chest_pain)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name_entry.get(),
            surname_entry.get(),
            gender_combobox.get(),
            age_spinbox.get(),
            smoke_var.get(),
            yellow_fingers_var.get(),
            pressure_var.get(),
            chronic_disease_var.get(),
            fatigue_var.get(),
            allergy_var.get(),
            vitiligo_var.get(),
            alcohol_var.get(),
            cough_var.get(),
            dyspnea_var.get(),
            swallowing_var.get(),
            chest_pain_var.get(),
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Informacje", "Dane zapisane w bazie danych!")

    app.title("Formularz")
    frame = ttk.Frame(app)
    frame.pack(padx=10, pady=10)
    form_data = ['T']

    # Imię
    ttk.Label(frame, text="Imię:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    name_entry = ttk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Nazwisko
    ttk.Label(frame, text="Nazwisko:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    surname_entry = ttk.Entry(frame)
    surname_entry.grid(row=1, column=1, padx=5, pady=5)

    # Płeć
    ttk.Label(frame, text="Płeć:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    gender_combobox = ttk.Combobox(frame, values=["Mężczyzna", "Kobieta"])
    gender_combobox.grid(row=2, column=1, padx=5, pady=5)

    # Wiek
    ttk.Label(frame, text="Wiek:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    age_spinbox = ttk.Spinbox(frame, from_=0, to=100)
    age_spinbox.grid(row=3, column=1, padx=5, pady=5)

    # Czy palisz?
    smoke_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy palisz?").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=smoke_var, value="Tak").grid(row=4, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=smoke_var, value="Nie").grid(row=4, column=1, sticky=tk.E)

    # Czy masz żółte palce?
    yellow_fingers_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy masz żółte palce?").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=yellow_fingers_var, value="Tak").grid(row=5, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=yellow_fingers_var, value="Nie").grid(row=5, column=1, sticky=tk.E)

    # Czy odczuwasz presje otoczenia?
    pressure_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy odczuwasz presje otoczenia?").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=pressure_var, value="Tak").grid(row=6, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=pressure_var, value="Nie").grid(row=6, column=1, sticky=tk.E)

    # Czy zmagasz się z chorobą przewlekłą?
    chronic_disease_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy zmagasz się z chorobą przewlekłą?").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=chronic_disease_var, value="Tak").grid(row=7, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=chronic_disease_var, value="Nie").grid(row=7, column=1, sticky=tk.E)

    # Czy jesteś często zmęczony?
    fatigue_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy jesteś często zmęczony?").grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=fatigue_var, value="Tak").grid(row=8, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=fatigue_var, value="Nie").grid(row=8, column=1, sticky=tk.E)

    # Czy masz alergie?
    allergy_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy masz alergie?").grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=allergy_var, value="Tak").grid(row=9, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=allergy_var, value="Nie").grid(row=9, column=1, sticky=tk.E)

    # Czy chorujesz na bielactwo?
    vitiligo_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy chorujesz na bielactwo?").grid(row=10, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=vitiligo_var, value="Tak").grid(row=10, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=vitiligo_var, value="Nie").grid(row=10, column=1, sticky=tk.E)

    # Czy spożywasz alkohol?
    alcohol_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy spożywasz alkohol?").grid(row=11, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=alcohol_var, value="Tak").grid(row=11, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=alcohol_var, value="Nie").grid(row=11, column=1, sticky=tk.E)

    # Czy męczy cię kaszel?
    cough_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy męczy cię kaszel?").grid(row=12, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=cough_var, value="Tak").grid(row=12, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=cough_var, value="Nie").grid(row=12, column=1, sticky=tk.E)

    # Czy miewasz duszności?
    dyspnea_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy miewasz duszności?").grid(row=13, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=dyspnea_var, value="Tak").grid(row=13, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=dyspnea_var, value="Nie").grid(row=13, column=1, sticky=tk.E)

    # Czy masz trudności w połykaniu?
    swallowing_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy masz trudności w połykaniu?").grid(row=14, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=swallowing_var, value="Tak").grid(row=14, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=swallowing_var, value="Nie").grid(row=14, column=1, sticky=tk.E)

    # Czy odczuwasz ból w klatce piersiowej?
    chest_pain_var = tk.StringVar(value="Nie")
    ttk.Label(frame, text="Czy odczuwasz ból w klatce piersiowej?").grid(row=15, column=0, sticky=tk.W, padx=5, pady=5)
    ttk.Radiobutton(frame, text="Tak", variable=chest_pain_var, value="Tak").grid(row=15, column=1, sticky=tk.W)
    ttk.Radiobutton(frame, text="Nie", variable=chest_pain_var, value="Nie").grid(row=15, column=1, sticky=tk.E)

    # przycisk submit na końcu
    submit_button = ttk.Button(frame, text="Zatwierdź", command=submit_form)
    submit_button.grid(row=17, column=0, columnspan=2, pady=20)


app.mainloop()
