import streamlit as st
import numpy as np
import plotly.graph_objects as go  # Usamos Graph Objects para personalizar más fácil

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

# Convertir la función para que acepte arreglos de NumPy de forma segura
f_vectorizada = np.vectorize(f)

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
    
    # Generar datos para la gráfica usando numpy y la función segura
    x_vals = np.linspace(limite_a - 1, limite_b + 1, 200)
    y_vals = f_vectorizada(x_vals)
    
    # --- CONSTRUCCIÓN DEL GRÁFICO INTERACTIVO CON PLOTLY ---
    fig = go.Figure()
    
    # 1. Añadir la curva de la función
    fig.add_trace(go.Scatter(
        x=x_vals, 
        y=y_vals, 
        mode='lines', 
        name=f"f(x) = {funcion_str}",
        line=dict(color='blue')
    ))
    
    # 2. Si se encontró la raíz, marcarla con un punto rojo interactivo
    if raiz is not None:
        fig.add_trace(go.Scatter(
            x=[raiz], 
            y=[f(raiz)], 
            mode='markers', 
            name=f'Raíz (~{raiz:.2f})',
            marker=dict(color='red', size=10, symbol='circle')
        ))
    
    # 3. Personalizar el diseño (Eje X en cero, cuadrícula y títulos)
    fig.update_layout(
        title="Representación Gráfica de la Función",
        xaxis_title="Eje X",
        yaxis_title="Eje Y",
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified", # Muestra los datos de forma limpia al pasar el cursor
        showlegend=True
    )
    
    # Añadir una línea guía horizontal en Y=0 (Eje X)
    fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
    
    # Mostrar el gráfico usando la función nativa de Streamlit para Plotly
    st.plotly_chart(fig, use_container_width=True)
