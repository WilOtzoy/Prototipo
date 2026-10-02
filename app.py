import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuración del título y descripción en la web
st.title("🧮 Solucionador de Métodos Numéricos")
st.markdown("Ejemplo práctico interactivo usando el **Método de Bisección**.")

# 2. Creación de una barra lateral para los controles de entrada
st.sidebar.header("Parámetros del Método")
funcion_str = st.sidebar.text_input("Ingresa la función f(x):", value="x**3 - 4*x - 9")
limite_a = st.sidebar.number_input("Límite inferior (a):", value=2.0)
limite_b = st.sidebar.number_input("Límite superior (b):", value=3.0)
tolerancia = st.sidebar.number_input("Tolerancia:", value=0.001, format="%.4f")

# Definir la función matemáticamente usando el texto ingresado
def f(x):
    return eval(funcion_str)

# 3. Lógica del algoritmo de Bisección
def biseccion(a, b, tol):
    if f(a) * f(b) >= 0:
        return None, "Error: f(a) y f(b) deben tener signos opuestos."
    
    c = a
    iteraciones = 0
    while (b - a) / 2.0 > tol:
        c = (a + b) / 2.0
        if f(c) == 0.0:
            break
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iteraciones += 1
    return c, f"Raíz aproximada encontrada en {iteraciones} iteraciones."

# 4. Ejecución del cálculo y despliegue de resultados
raiz, mensaje = biseccion(limite_a, limite_b, tolerancia)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resultados del Cálculo")
    if raiz is None:
        st.error(mensaje)
    else:
        st.success(mensaje)
        st.metric(label="Raíz calculada (x)", value=f"{raiz:.5f}")
        st.metric(label="Valor de f(x) en la raíz", value=f"{f(raiz):.5f}")

with col2:
    st.subheader("Visualización Gráfica")
    # Generar datos para la gráfica usando numpy
    x_vals = np.linspace(limite_a - 1, limite_b + 1, 200)
    y_vals = f(x_vals)
    
    # Construir el gráfico con matplotlib
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=f"f(x) = {funcion_str}", color="blue")
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8) # Eje X
    
    if raiz is not None:
        ax.plot(raiz, f(raiz), 'ro', label=f'Raíz (~{raiz:.2f})') # Punto de la raíz
        
    ax.legend()
    ax.grid(True)
    
    # Mostrar el gráfico de Matplotlib directamente en la interfaz web de Streamlit
    st.pyplot(fig)
