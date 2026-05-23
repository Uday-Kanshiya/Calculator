import streamlit as st
import pandas as pd
from calculator_core import SafeEvaluator
from styling import inject_custom_css

# Page Configuration for modern premium feel
st.set_page_config(
    page_title="Aether Scientific Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject our custom glassmorphic dark styling
inject_custom_css()

# Initialize session state variables
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'error' not in st.session_state:
    st.session_state.error = ""
if 'history' not in st.session_state:
    st.session_state.history = []
if 'angle_mode' not in st.session_state:
    st.session_state.angle_mode = "Radians"

def evaluate_now():
    """
    Evaluates the current formula expression in session state, 
    updating result/error and adding to calculation history.
    """
    expr = st.session_state.expression.strip()
    if not expr:
        st.session_state.result = ""
        st.session_state.error = ""
        return
        
    evaluator = SafeEvaluator(angle_mode=st.session_state.angle_mode)
    try:
        val = evaluator.evaluate(expr)
        if val == "":
            st.session_state.result = ""
            st.session_state.error = ""
            return
            
        if isinstance(val, float):
            # Format float output nicely
            if val.is_integer():
                formatted = str(int(val))
            elif abs(val) < 1e-6 or abs(val) > 1e9:
                formatted = f"{val:.6e}"
            else:
                formatted = f"{val:.8g}"
        else:
            formatted = str(val)
            
        st.session_state.result = formatted
        st.session_state.error = ""
        
        # Add success to history
        item = {"formula": expr, "result": formatted}
        if not st.session_state.history or st.session_state.history[-1] != item:
            st.session_state.history.append(item)
            if len(st.session_state.history) > 20:
                st.session_state.history.pop(0)
    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.result = ""

def handle_click(label):
    """
    Handles standard and complex button clicks on the interactive keypad.
    """
    if label == "AC":
        st.session_state.expression = ""
        st.session_state.result = ""
        st.session_state.error = ""
    elif label == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
    elif label == "=":
        evaluate_now()
    elif label == "+/-":
        expr = st.session_state.expression
        if expr:
            if expr.startswith("-(") and expr.endswith(")"):
                st.session_state.expression = expr[2:-1]
            else:
                st.session_state.expression = f"-({expr})"
    elif label == "1/x":
        expr = st.session_state.expression
        if expr:
            st.session_state.expression = f"1/({expr})"
        else:
            st.session_state.expression = "1/("
    elif label == "x²":
        st.session_state.expression += "^2"
    elif label == "xʸ":
        st.session_state.expression += "^"
    elif label == "n!":
        st.session_state.expression += "fact("
    elif label in ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "sqrt", "cbrt", "exp", "log", "ln", "log2", "abs"]:
        st.session_state.expression += f"{label}("
    else:
        st.session_state.expression += label

# ----------------- SIDEBAR PANEL -----------------
with st.sidebar:
    st.markdown('<h2 style="color:#00f2fe; margin-bottom:5px;">Aether Scientific</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b; font-size:0.9rem; margin-bottom:20px;">Premium High-Fidelity Math System</p>', unsafe_allow_html=True)
    
    # 1. Angle mode toggle
    st.markdown('<p class="sci-label">📐 Angle Configuration</p>', unsafe_allow_html=True)
    st.session_state.angle_mode = st.radio(
        "Angle Mode",
        ["Radians", "Degrees"],
        label_visibility="collapsed"
    )
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # 2. History section
    st.markdown('<p class="sci-label">🕒 Calculation History</p>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown('<p style="color:#64748b; font-size:0.9rem;">No calculations recorded yet.</p>', unsafe_allow_html=True)
    else:
        # Show history list
        for idx, item in enumerate(reversed(st.session_state.history)):
            # Formatted list
            click_key = f"hist_{idx}"
            st.markdown(f"""
            <div class="history-item">
                <div class="history-formula">{item['formula']}</div>
                <div class="history-result">= {item['result']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Load Formula", key=f"btn_h_{idx}", use_container_width=True):
                st.session_state.expression = item['formula']
                st.session_state.result = item['result']
                st.session_state.error = ""
                st.rerun()
                
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear History", key="clear_hist", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)

    # 3. Help Cheatsheet
    st.markdown('<p class="sci-label">📖 Math Core Cheatsheet</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <strong>Functions:</strong><br>
        <code>sin(x)</code>, <code>cos(x)</code>, <code>tan(x)</code><br>
        <code>asin(x)</code>, <code>acos(x)</code>, <code>atan(x)</code><br>
        <code>sinh(x)</code>, <code>cosh(x)</code>, <code>tanh(x)</code><br>
        <code>log(x)</code>, <code>ln(x)</code>, <code>log2(x)</code><br>
        <code>sqrt(x)</code>, <code>cbrt(x)</code>, <code>fact(x)</code><br>
        <code>abs(x)</code>, <code>exp(x)</code><br>
        <strong>Constants:</strong><br>
        <code>pi</code> ($\pi$), <code>e</code>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✨ Logarithmic calculations (log, ln, log2) are fully supported!")

# ----------------- MAIN LAYOUT -----------------

tab1, tab2 = st.tabs(["🧮 Interactive Calculator", "📈 2D Function Plotter"])

with tab1:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #fff; margin-bottom: 20px; font-weight:500;">Aether Math Deck</h3>', unsafe_allow_html=True)
    
    # 1. Custom LED Display Screen
    formula_display = st.session_state.expression if st.session_state.expression else "0"
    if st.session_state.error:
        result_display = f'<div class="screen-error">{st.session_state.error}</div>'
    else:
        result_display = f'<div class="screen-result">{st.session_state.result if st.session_state.result else "0"}</div>'
        
    st.markdown(f"""
    <div class="led-screen">
        <div class="screen-formula">{formula_display}</div>
        {result_display}
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Active Formula Text Field (keyboard user entry)
    st.text_input(
        "✏️ Direct keyboard entry / formula editor:",
        key="expression",
        on_change=evaluate_now,
        placeholder="Type here or click tactile buttons below..."
    )
    
    st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)
    
    # 3. Interactive Keypad Grid Matrix (8 Rows x 5 Columns)
    keypad = [
        [("(", "sci"), (")", "sci"), ("xʸ", "sci"), ("⌫", "clear"), ("AC", "clear")],
        [("sin", "sci"), ("cos", "sci"), ("tan", "sci"), ("sqrt", "sci"), ("π", "sci")],
        [("asin", "sci"), ("acos", "sci"), ("atan", "sci"), ("cbrt", "sci"), ("e", "sci")],
        [("sinh", "sci"), ("cosh", "sci"), ("tanh", "sci"), ("abs", "sci"), ("%", "sci")],
        [("log", "sci"), ("ln", "sci"), ("log2", "sci"), ("n!", "sci"), ("exp", "sci")],
        [("7", "num"), ("8", "num"), ("9", "num"), ("÷", "op"), ("1/x", "sci")],
        [("4", "num"), ("5", "num"), ("6", "num"), ("×", "op"), ("x²", "sci")],
        [("1", "num"), ("2", "num"), ("3", "num"), ("-", "op"), ("+/-", "sci")],
        [("0", "num"), (".", "num"), ("+", "op"), ("=", "eq"), ("exp", "sci")]
    ]
    
    for row_idx, row in enumerate(keypad):
        cols = st.columns(5)
        for col_idx, (label, btn_type) in enumerate(row):
            with cols[col_idx]:
                is_eq = (btn_type == "eq")
                if st.button(
                    label, 
                    key=f"btn_{row_idx}_{col_idx}",
                    type="primary" if is_eq else "secondary",
                    use_container_width=True
                ):
                    handle_click(label)
                    st.rerun()
                    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="calc-card" style="max-width: 800px;">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #fff; margin-bottom: 20px; font-weight:500;">Interactive 2D Function Plotter</h3>', unsafe_allow_html=True)
    
    st.markdown("<p style='color:#94a3b8; font-size:0.95rem; margin-bottom:20px;'>Define a function of <strong>x</strong> to plot over a specified interval. Enjoy beautiful, high-resolution rendering with dynamic scaling.</p>", unsafe_allow_html=True)
    
    # 1. Function formula input
    func_input = st.text_input(
        "Enter Function f(x)", 
        value="sin(x) * x", 
        key="plot_func",
        placeholder="e.g. sin(x) * x + cos(2*x) or x^2 - 4"
    )
    
    # 2. X Bounds and configuration
    col1, col2, col3 = st.columns(3)
    with col1:
        xmin = st.number_input("Domain Minimum (X Min)", value=-10.0, step=1.0, key="plot_xmin")
    with col2:
        xmax = st.number_input("Domain Maximum (X Max)", value=10.0, step=1.0, key="plot_xmax")
    with col3:
        num_pts = st.slider("Plot Resolution (Points)", min_value=50, max_value=500, value=250, step=50, key="plot_res")
        
    st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
    
    if st.button("📊 Plot Function", type="primary", use_container_width=True, key="btn_plot"):
        # Validate inputs
        if xmin >= xmax:
            st.error("Domain Error: X Min must be strictly less than X Max.")
        elif not func_input.strip():
            st.error("Invalid Input: Please enter a valid function of x.")
        else:
            evaluator = SafeEvaluator(angle_mode=st.session_state.angle_mode, variables={})
            
            x_vals = []
            y_vals = []
            has_errors = False
            err_msg = ""
            
            # Linearly spaced x evaluation
            step = (xmax - xmin) / (num_pts - 1)
            for i in range(num_pts):
                x_val = xmin + i * step
                # Bind variable x
                evaluator.variables = {'x': x_val, 'X': x_val}
                try:
                    y_val = evaluator.evaluate(func_input)
                    if isinstance(y_val, (int, float)):
                        x_vals.append(x_val)
                        y_vals.append(y_val)
                except Exception as e:
                    has_errors = True
                    err_msg = str(e)
                    continue
            
            if not x_vals:
                st.error(f"Plot Error: Could not compute any real-numbered outputs. Reason: {err_msg}")
            else:
                # Create pandas dataframe and plot
                df = pd.DataFrame({"x": x_vals, "f(x)": y_vals})
                df.set_index("x", inplace=True)
                
                # Success banner
                st.markdown(f'<div class="info-card">Successfully rendered <strong>f(x) = {func_input}</strong> in <strong>{st.session_state.angle_mode}</strong> mode.</div>', unsafe_allow_html=True)
                
                # Streamlit line chart is fully responsive, interactive, and beautifully integrated
                st.line_chart(df, height=380)
                
                if has_errors:
                    st.warning("⚠️ Warning: Certain points in the domain had math evaluation errors (e.g. division by zero, values outside of domain, or complex numbers) and were automatically skipped.")

    st.markdown('</div>', unsafe_allow_html=True)
