# Aether Scientific Calculator 🧮

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://uday-kanshiya-calculator-app-f3wpyf.streamlit.app/)

Aether Scientific is a stunningly designed, premium, high-fidelity scientific calculator web application built with Python and Streamlit. It features safe mathematical parsing, beautiful glassmorphic UI aesthetics, a click-to-load history panel, and an interactive 2D function plotter.

🔗 **Live Demo:** [uday-kanshiya-calculator-app-f3wpyf.streamlit.app](https://uday-kanshiya-calculator-app-f3wpyf.streamlit.app/)

---

## ✨ Features

- **🔒 Safe Evaluation**: Uses Python's Abstract Syntax Tree (`ast`) to safely evaluate expressions, completely mitigating code-injection vulnerabilities typical of raw `eval()`.
- **📐 Flex Angle System**: Instantly toggle between **Degrees** and **Radians** for all trigonometric, inverse trigonometric, and hyperbolic calculations.
- **🕒 Click-to-Load History**: Stores your last 20 calculations. Click any history card to instantly reload its expression and results back to the screen.
- **📈 2D Function Plotter**: Plot any mathematical function of `x` (e.g. `sin(x) * x` or `x^2 - 4`) over a custom interval, featuring robust math domain safety skipping (e.g. automatically ignoring division-by-zero points).
- **🎨 Glassmorphic Premium UI**: Overrides Streamlit's default layouts with custom Outfit & Orbitron typography, neon LED glow indicators, and tactile glass buttons.

---

## 🗂️ Project Structure

```
scientific_calculator/
├── app.py              # Main UI flow, keypads, and tabs
├── calculator_core.py  # AST evaluation parser
├── styling.py          # Premium glassmorphic CSS styling rules
└── README.md           # Project presentation & setup guidelines
```

---

## 🚀 Setup and Installation

### 1. Pre-requisites
Ensure you have Python installed (Python 3.8+ recommended).

### 2. Install dependencies
Clone the repository and install the required modules:
```bash
pip install streamlit pandas
```

### 3. Start the application
Run the Streamlit application:
```bash
python -m streamlit run app.py
```
Streamlit will automatically launch the app in your default browser at `http://localhost:8501`.

---

## 🛠️ Supported Core Operations

- **Logarithmic**: `log(x)` / `log10(x)` (common log base 10), `ln(x)` (natural log base e), `log2(x)` (binary log base 2)
- **Trigonometric**: `sin(x)`, `cos(x)`, `tan(x)`
- **Inverse Trig**: `asin(x)`, `acos(x)`, `atan(x)`
- **Hyperbolic**: `sinh(x)`, `cosh(x)`, `tanh(x)`
- **Power & Roots**: `x^y` (power), `x^2` (square), `sqrt(x)` (square root), `cbrt(x)` (cubic root)
- **Algebraic**: Factorial `fact(x)`, Absolute `abs(x)`, Modulo `%`, Exponential `exp(x)`
- **Constants**: `pi` ($\pi$), `e`
