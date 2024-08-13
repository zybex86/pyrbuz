# Polska wersja Suika Game w Pythonie

## Opis projektu

Aplikacja `pyrbuz` to port `Suika Game` napisany w pythonie. Pierwsza wersja korzysta z `pygame` i jest odwzorowaniem kodu z poradnika https://www.youtube.com/watch?v=In0EvhenzeQ oraz https://www.youtube.com/watch?v=_4kstHyPtSk użytkownika `OB1`. Teksty przetłumaczone na język polski. Późniejsze wersje będą przepisane w Kivy z myślą o działaniu na Androidzie / iOS.

## Wymagania

- pygame == 2.6.0
- python >= 3.12
- pillow == 10.4.0
- numpy == 2.0.1
- pymunk == 6.8.1

## Instalacja

1. Skonfiguruj środowisko pythona (Jeśli Twój system operacyjny to WINDOWS - skorzystaj z poradnika na https://realpython.com/python-coding-setup-windows/#setting-up-core-python-coding-software-in-windows)
2. Stwórz virtualne środowisko `python -m venv pyrbuz` oraz je uruchom (np. `.\pyrbuz\Scripts\activate` dla Windows)
3. Zainstaluj poetry `pip install -U pip setuptools poetry`
4. Odpal aplikację `python suika.py`
