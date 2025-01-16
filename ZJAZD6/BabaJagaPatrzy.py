# TYTUŁ: COMPUTER VISION
#
# AUTORZY: Jakub Marcinkowski s21021 i Dagmara Gibas s22620
#
# OPIS PROBLEMU:
# 1. Zbudować prototyp maszyny do gry w "Baba Jaga patrzy" - wybrane funkcjonalności:
# - Narysować celownik na twarzy celu
# - Nie strzelać gdy uczestnik się poddaje
#
# INSTRUKCJA PRZYGOTOWANIA ŚRODOWISKA
# 1. Zainstalować interpreter python w wersji 3+ oraz narzędzie pip
# 2. Pobrać projekt
# 3. Uruchomić wybraną konsolę/terminal
# 4. Zainstalować wymagane biblioteki za pomocą komend:
# pip install cv2
# pip install mediapipe
# 5. Podłączyć do komputera kamerkę internetową
# 6. Przejść do ścieżki z projektem (w systemie linux komenda cd)
# 7. Uruchomić projekt przy pomocy polecenia:
# python .\BabaJagaPatrzy.py

"""
Opis algorytmu:
- przechwytywanie wideo z kamery
- znajdowanie pozycji oczu
- obliczyć pozycję między oczami
- Znajdź pozycję nadgarstków
- określ, czy dana osoba się poddaje - jeśli oba nadgarstki znajdują się nad jej oczami
- jeśli osoba się podda, nie wyciągaj lunety snajperskiej
- w przeciwnym razie narysuj lunetę snajperską między oczami
"""

import cv2
import mediapipe as mp

# Inicjalizacja modułów MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Otwieranie kamery
cap = cv2.VideoCapture(0)

# Użycie MediaPipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, image = cap.read()  # Odczyt klatki z kamery
        if not ret:
            print("Nie można odczytać klatki z kamery.")
            break

        # Przetwarzanie obrazu
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Sprawdzenie, czy wykryto landmarki
        if results.pose_landmarks is not None:
            try:
                # Współrzędne oczu
                left_eye_pos = results.pose_landmarks.landmark[1]
                right_eye_pos = results.pose_landmarks.landmark[4]
                between_eyes_x = ((left_eye_pos.x + right_eye_pos.x) / 2) * image.shape[1]
                between_eyes_y = ((left_eye_pos.y + right_eye_pos.y) / 2) * image.shape[0]

                # Współrzędne nadgarstków
                left_wrist_y = results.pose_landmarks.landmark[15].y * image.shape[0]
                right_wrist_y = results.pose_landmarks.landmark[16].y * image.shape[0]

                # Logika poddania się
                surrender = False
                if left_wrist_y <= between_eyes_y and right_wrist_y <= between_eyes_y:
                    surrender = True
                    print("poddaje sie")

                # Rysowanie na obrazie
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if not surrender:
                    cv2.circle(image, (int(between_eyes_x), int(between_eyes_y)), 10, (255, 255, 0), thickness=2, lineType=cv2.FILLED)
            except Exception as e:
                print(f"Błąd podczas przetwarzania landmarków: {e}")

        else:
            print("Nie wykryto postawy w bieżącej klatce.")

        # Wyświetlanie obrazu
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        if cv2.waitKey(2) & 0xFF == 27:  # Klawisz 'ESC' do zamknięcia
            break

# Zwolnienie kamery
cap.release()
cv2.destroyAllWindows()
