# 💣 Minesweeper

A sleek, dark-themed Minesweeper game built with Python and Pygame, featuring procedurally generated audio, screen shake effects, and neon-colored UI.

## 🎮 Features

- **16×16 grid** with 30 mines — a classic intermediate layout
- **Safe first click** — mines are never placed on or adjacent to your first reveal
- **Neon number colors** for a modern dark UI aesthetic
- **Screen shake** on mine detonation
- **Procedurally generated explosion sound** — no audio files needed
- **Animated flickering fire** on triggered mines
- **Play Again / Exit** buttons on game end


## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/minesweeper.git
   cd minesweeper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python minesweeper.py
   ```

---

## 🕹️ Controls

| Action              | Input                        |
|---------------------|------------------------------|
| Reveal cell         | Left Click                   |
| Place / Remove flag | Right Click                  |
| Play Again          | Click button                 |
| Exit                | Click button or close window |

## 📁 Project Structure

```
minesweeper/
├── minesweeper.py      # Main game file
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           
```

---

## 🛠️ Built With

- [Python](https://www.python.org/) — Core language
- [Pygame](https://www.pygame.org/) — Game engine & audio
- 'array' module — Procedural audio buffer generation
