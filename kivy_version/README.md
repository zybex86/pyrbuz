# Kivy Version of Suika Game

## Project Description

This project is a Kivy-based implementation of the Suika Game, originally developed using Pygame. The Kivy version aims to provide a more modern interface and better support for touch devices, making it suitable for mobile platforms.

## Recommended Python Version

It is recommended to use **Python 3.10.x** for the best compatibility with Kivy and its dependencies.  
Other Python 3 versions (3.8–3.11) may work, but 3.10 is the most thoroughly tested.

## Project Structure

The project is organized as follows:

```
kivy_version
├── src
│   ├── main.py          # Entry point of the Kivy application
│   ├── game.py          # Main game logic and state management
│   ├── widgets.py       # Custom Kivy widgets for the game
│   ├── config.py        # Configuration settings for the game
│   ├── assets           # Directory containing image assets
│   │   ├── apple.png
│   │   ├── background.png
│   │   ├── cherry.png
│   │   ├── cloud.png
│   │   ├── grapes.png
│   │   ├── melon.png
│   │   ├── orange.png
│   │   ├── peach.png
│   │   ├── pear.png
│   │   ├── persimmon.png
│   │   ├── pineapple.png
│   │   ├── strawberry.png
│   │   └── watermelon.png
│   └── kv
│       └── main.kv      # Kivy language file for UI layout
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
```

## Installation

### Using pyenv (Recommended for All Platforms)

[pyenv](https://github.com/pyenv/pyenv) allows you to easily install and manage multiple Python versions.

#### 1. Install pyenv

- **Linux/macOS:**  
  Follow the instructions at [pyenv installation](https://github.com/pyenv/pyenv#installation).
- **Windows:**  
  Use [pyenv-win](https://github.com/pyenv-win/pyenv-win#installation).

#### 2. Install Python 3.10.x

```sh
pyenv install 3.10.11
```

#### 3. Set Local Python Version for the Project

```sh
cd kivy_version
pyenv local 3.10.11
```

#### 4. Create and Activate a Virtual Environment

```sh
python -m venv kivy_env
# On Windows:
kivy_env\Scripts\activate
# On macOS/Linux:
source kivy_env/bin/activate
```

#### 5. Install the required dependencies

```sh
pip install -r requirements.txt
```

### Manual Setup (If Not Using pyenv)

1. Ensure you have Python 3.10.x installed.
2. Create a virtual environment:
   ```
   python -m venv kivy_env
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     kivy_env\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source kivy_env/bin/activate
     ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Game

To run the game, execute the following command in the terminal:

```
python src/main.py
```

## Features

- Interactive gameplay with various fruit types.
- Collision detection and merging mechanics.
- Customizable settings through the `config.py` file.
- User-friendly interface designed with Kivy.

## Future Improvements

- Enhance graphics and animations.
- Implement sound effects and music.
- Optimize performance for mobile devices.

## How to Run the Game

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the game:
   ```
   python src/main.py
   ```

## How to Port to Android

1. Install [Buildozer](https://github.com/kivy/buildozer) (recommended on Linux):
   ```
   pip install buildozer
   ```
2. Initialize buildozer in your project directory:
   ```
   cd kivy_version
   buildozer init
   ```
3. Edit `buildozer.spec` to include your requirements (e.g., `kivy,numpy,pillow,pyyaml`).
4. Build the APK:
   ```
   buildozer -v android debug
   ```
5. Deploy to a connected Android device:
   ```
   buildozer android deploy run
   ```

For more details, see the [Kivy documentation](https://kivy.org/doc/stable/guide/packaging-android.html).

## License

This project is licensed under the MIT License. See the LICENSE file for more details.