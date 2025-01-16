"""
SIECI NEURONOWE DLA KLASYFIKACJI

Autorzy:Jakub Marcinkowski s21021, Dagmara Gibas s22620
Opis problemu:
1. Sieci neuronowe są wszechstronnym narzędziem do rozwiązywania problemów klasyfikacji.
2. Wykorzystano zbiór danych o cukrzycy Pima Indian, aby zbudować model klasyfikacyjny i ocenić jego skuteczność.
3. Porównano skuteczność dwóch różnych rozmiarów sieci neuronowych.
4. Narysowano macierz pomyłek i dodano szczegółowe raporty klasyfikacji.

Instrukcja użycia:
1. Zainstalować Python w wersji 3+ oraz narzędzie pip.
2. Zainstalować wymagane biblioteki za pomocą poleceń:
   pip install pandas
   pip install sklearn
   pip install matplotlib
3. Uruchomić projekt przy pomocy polecenia:
   python <Zadanie_1>.py

Dane użyte w zadaniu:
- https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv
- Framework: scikit-learn
"""
import warnings
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import pandas as pd

# Wyłączenie ostrzeżeń
warnings.filterwarnings('ignore', category=ConvergenceWarning)

# Wczytanie zbioru danych
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv'
data_frame = pd.read_csv(url)
data = data_frame.to_numpy()
X, y = data[:, :-1], data[:, -1]

# Podział danych na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=5, test_size=0.25)

# Definicja dwóch różnych modeli sieci neuronowych
models = {
    "Small Network (5 neurons)": MLPClassifier(
        hidden_layer_sizes=(5,),
        max_iter=100,
        alpha=1e-4,
        solver="adam",
        random_state=1,
        activation="tanh",
    ),
    "Larger Network (10 neurons)": MLPClassifier(
        hidden_layer_sizes=(10,),
        max_iter=100,
        alpha=1e-4,
        solver="adam",
        random_state=1,
        activation="relu",
    )
}

results = {}

for name, model in models.items():
    # Trenowanie modelu
    model.fit(X_train, y_train)

    # Obliczanie wyników
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    y_preds = model.predict(X_test)

    results[name] = {
        "train_score": train_score,
        "test_score": test_score,
        "classification_report": classification_report(y_test, y_preds),
        "confusion_matrix": confusion_matrix(y_test, y_preds, normalize='all')
    }

    # Wyświetlenie wyników
    print(f"\n### Wyniki dla modelu: {name} ###")
    print(f"Dokładność na zbiorze treningowym: {train_score:.4f}")
    print(f"Dokładność na zbiorze testowym: {test_score:.4f}")
    print("\nRaport klasyfikacji:")
    print(results[name]["classification_report"])

    # Rysowanie macierzy pomyłek
    ConfusionMatrixDisplay(results[name]["confusion_matrix"], display_labels=['0', '1']).plot()
    plt.title(f"Macierz pomyłek - {name}")
    plt.show()

# Podsumowanie
print("\n### Porównanie modeli ###")
for name, result in results.items():
    print(f"Model: {name}")
    print(f"Train Accuracy: {result['train_score']:.4f}")
    print(f"Test Accuracy: {result['test_score']:.4f}")
    print("-" * 40)