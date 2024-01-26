import tkinter as tk
import uuid
from tkinter import messagebox, ttk
import sqlite3
import bcrypt
from datetime import datetime

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

form_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def setup_database():
    """
    Konfiguruje bazę danych, tworząc tabele, jeśli nie istnieją.

    :return: None
    """
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id_classification_result TEXT PRIMARY KEY,
        name TEXT,
        surname TEXT,
        date DATETIME,
        gender TEXT,
        age INTEGER,
        smoke INTEGER,
        yellow_fingers INTEGER,
        anxiety INTEGER,
        pressure INTEGER,
        chronic_disease INTEGER,
        fatigue INTEGER,
        allergy INTEGER,
        vitiligo INTEGER,
        alcohol INTEGER,
        cough INTEGER,
        dyspnea INTEGER,
        swallowing INTEGER,
        chest_pain INTEGER,
        proba INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id_client TEXT PRIMARY KEY,
        username TEXT,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()


def log_reg_from():
    """
    Rozpoczyna proces logowania i rejestracji.

    :return: None
    """
    def update_buttons_status(*args):
        if username_var.get() and password_var.get():
            login_button['state'] = tk.NORMAL
            register_button['state'] = tk.NORMAL
        else:
            login_button['state'] = tk.DISABLED
            register_button['state'] = tk.DISABLED

    def register():
        username = username_entry.get()
        password = password_entry.get()

        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        id_client = str(uuid.uuid4())

        try:
            cursor.execute("INSERT INTO accounts (id_client, username, password) VALUES (?, ?, ?)",
                           (id_client, username, password))
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

        if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
            # Zalogowano pomyślnie
            # Możesz teraz przejść do innej części aplikacji, np. wyświetlić formularz
            app_form()
            login_frame.destroy()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowa nazwa użytkownika lub hasło!")

    app.title("Logowanie")

    login_frame = ttk.Frame(app)
    login_frame.pack(padx=10, pady=10)

    username_var = tk.StringVar()
    password_var = tk.StringVar()

    username_var.trace_add("write", update_buttons_status)
    password_var.trace_add("write", update_buttons_status)

    ttk.Label(login_frame, text="Nazwa użytkownika:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    username_entry = ttk.Entry(login_frame, textvariable=username_var)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(login_frame, text="Hasło:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    password_entry = ttk.Entry(login_frame, textvariable=password_var, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    login_button = ttk.Button(login_frame, text="Zaloguj", command=login, state=tk.DISABLED)
    # login_button = ttk.Button(login_frame, text="Zaloguj", command=login)
    login_button.grid(row=2, column=0, padx=5, pady=20)

    register_button = ttk.Button(login_frame, text="Zarejestruj", command=register, state=tk.DISABLED)
    # register_button = ttk.Button(login_frame, text="Zarejestruj", command=register)
    register_button.grid(row=2, column=1, padx=5, pady=20)


def app_form():
    """
    Ta metoda tworzy formularz z serią pytań i pozwala użytkownikowi na przesłanie formularza.

    :return: None
    """
    questions = [
        ("Czy palisz?", "smoke_var"),
        ("Czy masz żółte palce?", "yellow_fingers_var"),
        ("Czy osoba cierpi na lęk?", "anxiety_var"),
        ("Czy odczuwasz presje otoczenia?", "pressure_var"),
        ("Czy zmagasz się z chorobą przewlekłą?", "chronic_disease_var"),
        ("Czy jesteś często zmęczony?", "fatigue_var"),
        ("Czy masz alergie?", "allergy_var"),
        ("Czy chorujesz na bielactwo?", "vitiligo_var"),
        ("Czy spożywasz alkohol?", "alcohol_var"),
        ("Czy męczy cię kaszel??", "cough_var"),
        ("Czy miewasz duszności?", "dyspnea_var"),
        ("Czy masz trudności w połykaniu?", "swallowing_var"),
        ("Czy odczuwasz ból w klatce piersiowej?", "chest_pain_var"),
    ]

    def submit_form():
        """
        Przesyła dane formularza do bazy danych.

        :return: None
        """
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO users (id_classification_result, name, surname, date, gender, age, smoke, yellow_fingers, anxiety,
        pressure, chronic_disease, fatigue, allergy, vitiligo, alcohol, cough, dyspnea, swallowing, chest_pain, proba)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(uuid.uuid4()),
            name_entry.get(),
            surname_entry.get(),
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            gender_combobox.current(),
            age_spinbox.get(),
            form_data[4].get(),
            form_data[5].get(),
            form_data[6].get(),
            form_data[7].get(),
            form_data[8].get(),
            form_data[9].get(),
            form_data[10].get(),
            form_data[11].get(),
            form_data[12].get(),
            form_data[13].get(),
            form_data[14].get(),
            form_data[15].get(),
            form_data[16].get(),
            check_probability()
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Informacje", "Dane zapisane w bazie danych!")

    def check_probability():
        """
        Metoda ta służy do sprawdzania prawdopodobieństwa wystąpienia raka płuc na podstawie podanych danych wejściowych.

        :return: None
        """
        # Wczytanie danych z pliku CSV
        data = pd.read_csv('./newData.csv')

        # Wyświetlenie pierwszych kilku wierszy danych
        print(data.head())

        # Podział danych na zmienne niezależne (X) i zmienną docelową (y)
        X = data.drop('LUNG_CANCER', axis=1)
        y = data['LUNG_CANCER']

        # Podział danych na zbiory treningowe i testowe
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Skalowanie cech
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        print(X_train_scaled[:5], y_train.head())  # Wyświetlenie przykładowych przeskalowanych danych treningowych

        # Trenowanie modelu regresji logistycznej
        logreg = LogisticRegression(random_state=42)
        logreg.fit(X_train_scaled, y_train)

        # Predykcja na zbiorze testowym
        y_pred = logreg.predict(X_test_scaled)

        # Ewaluacja modelu
        accuracy = accuracy_score(y_test, y_pred)
        classification_rep = classification_report(y_test, y_pred)
        confusion = confusion_matrix(y_test, y_pred)

        print(accuracy, classification_rep, confusion)

        def predict_lung_cancer_risk(gender, age, smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease,
                                     fatigue, allergy, wheezing, alcohol_consuming, coughing, shortness_of_breath,
                                     swallowing_difficulty, chest_pain):
            """
            Funkcja przewidująca prawdopodobieństwo zachorowania na raka płuc na podstawie podanych danych wejściowych.

            Argumenty:
            - Wszystkie parametry odpowiadają pytaniom ankiety.

            Zwraca:
            - Prawdopodobieństwo zachorowania na raka płuc.
            """
            # Tworzenie DataFrame na podstawie dostarczonych odpowiedzi z odpowiednimi nazwami kolumn
            features_df = pd.DataFrame(
                data=[[gender, age, smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease,
                       fatigue, allergy, wheezing, alcohol_consuming, coughing, shortness_of_breath,
                       swallowing_difficulty, chest_pain]],
                columns=X.columns)

            # Skalowanie cech
            features_scaled = scaler.transform(features_df)

            # Predykcja prawdopodobieństwa
            probability = logreg.predict_proba(features_scaled)[:, 1]

            return probability[0]

        # Ponowne przetestowanie funkcji
        sample_probability = predict_lung_cancer_risk(gender_combobox.current(), age_spinbox.get(), form_data[4].get(),
                                                      form_data[5].get(), form_data[6].get(), form_data[7].get(),
                                                      form_data[8].get(), form_data[9].get(), form_data[10].get(),
                                                      form_data[11].get(), form_data[12].get(), form_data[13].get(),
                                                      form_data[14].get(), form_data[15].get(), form_data[16].get())
        print(sample_probability)

        messagebox.showinfo("Informacje",
                            f"Prawdopodobieństwo zachorowania na raka płuc {round(sample_probability * 100, 2)}%")

        return sample_probability

    def create_question(frame, label_text, variable_name, row_num):
        """
        Tworzy pytanie w określonej ramce z podanym tekstem etykiety, nazwą zmiennej i numerem wiersza.

        :param frame: Ramka do utworzenia pytania.
        :type frame: tkinter.Frame
        :param label_text: Tekst etykiety dla pytania.
        :type label_text: str
        :param variable_name: Nazwa zmiennej powiązanej z pytaniem.
        :type variable_name: str
        :param row_num: Numer wiersza pytania w ramce.
        :type row_num: int
        :return: None
        :rtype: None
        """
        var = tk.IntVar(value=0)
        ttk.Label(frame, text=label_text).grid(row=row_num, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(frame, text="Tak", variable=var, value=1).grid(row=row_num, column=1, sticky=tk.W)
        ttk.Radiobutton(frame, text="Nie", variable=var, value=0).grid(row=row_num, column=1, sticky=tk.E)
        form_data[row_num] = var

    app.title("Formularz")
    frame = ttk.Frame(app)
    frame.pack(padx=10, pady=10)

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

    # Pytania
    for idx, (question, var_name) in enumerate(questions):
        create_question(frame, question, var_name, idx + 4)

    # przycisk submit na końcu
    submit_button = ttk.Button(frame, text="Zapisz", command=submit_form)
    submit_button.grid(row=17, column=0, columnspan=2, pady=20)

    # przycisk submit na końcu
    submit_button = ttk.Button(frame, text="Prawdopodobieństwo", command=check_probability)
    submit_button.grid(row=17, column=1, columnspan=1, pady=20)


setup_database()
app = tk.Tk()
log_reg_from()

app.mainloop()
