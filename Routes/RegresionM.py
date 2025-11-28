from flask import Blueprint, jsonify
from Extensions import mongo
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import io
import base64

regresion_multiple_bp = Blueprint("regresion_multiple", __name__)

@regresion_multiple_bp.route("/", methods=["GET"])
def grafica_regresion_multiple():
    coleccion = mongo.db.estadisticas
    datos = list(coleccion.find({}, {"_id": 0}))

    if not datos:
        return jsonify({"error": "No hay datos almacenados en 'estadisticas'"}), 400

    df = pd.DataFrame(datos)

    # Filtrar columnas numéricas
    df_num = df.select_dtypes(include=["number"])
    if df_num.shape[1] < 3:
        return jsonify({
            "error": "Se requieren al menos 3 columnas numéricas para graficar en 3D"
        }), 400

    # X = todas menos la última columna numérica
    X = df_num.iloc[:, :-1]

    # Y = última columna numérica
    y = df_num.iloc[:, -1]

    # Ajustar el modelo
    modelo = LinearRegression()
    modelo.fit(X, y)

    # Tomamos las primeras dos columnas para el plano 3D
    x1 = X.iloc[:, 0]
    x2 = X.iloc[:, 1]

    x1_range = np.linspace(x1.min(), x1.max(), 20)
    x2_range = np.linspace(x2.min(), x2.max(), 20)

    X1_grid, X2_grid = np.meshgrid(x1_range, x2_range)

    # Promedios para variables extra
    adicionales = []
    if X.shape[1] > 2:
        for i in range(2, X.shape[1]):
            adicionales.append(np.full(X1_grid.size, X.iloc[:, i].mean()))
        adicionales = np.vstack(adicionales)
    else:
        adicionales = np.zeros((0, X1_grid.size))

    # Matriz completa para predicción
    X_pred = np.vstack([
        X1_grid.ravel(),
        X2_grid.ravel(),
        *adicionales
    ]).T

    Z = modelo.predict(X_pred).reshape(X1_grid.shape)

    # ========= Gráfica 3D =========
    fig = go.Figure()

    # Puntos reales
    fig.add_trace(go.Scatter3d(
        x=x1,
        y=x2,
        z=y,
        mode='markers',
        marker=dict(size=4, opacity=0.6),
        name='Datos reales'
    ))

    # Plano del modelo
    fig.add_trace(go.Surface(
        x=X1_grid,
        y=X2_grid,
        z=Z,
        opacity=0.6,
        colorscale='Viridis',
        name='Plano de regresión'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title=X.columns[0],
            yaxis_title=X.columns[1],
            zaxis_title=df_num.columns[-1]
        ),
        title='Regresión Lineal Múltiple (3D)',
        width=900,
        height=700
    )

    # Convertir figura a PNG
    buffer = io.BytesIO()
    fig.write_image(buffer, format="png")  # Requiere kaleido instalado
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    return jsonify({
        "mime": "image/png",
        "imagen": img_base64,
        "intercepto": float(modelo.intercept_),
        "coeficientes": {col: float(c) for col, c in zip(X.columns, modelo.coef_)}
    })
