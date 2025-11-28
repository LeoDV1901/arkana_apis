from flask import Blueprint, jsonify
from Extensions import mongo
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Creamos el Blueprint para agrupar las rutas de regresión
regresion_bp = Blueprint("regresion", __name__)

# ============================================================
#   GET /regresion/
#   Genera una gráfica de regresión lineal simple en PNG
# ============================================================
@regresion_bp.route("/", methods=["GET"])
def grafica_regresion_simple():

    # Acceder a la colección "estadisticas" de MongoDB
    coleccion = mongo.db.estadisticas
    datos = list(coleccion.find({}, {"_id": 0}))  # Trae todos los documentos sin el _id

    # Validar si la colección está vacía
    if not datos:
        return jsonify({"error": "No hay datos en la colección 'estadisticas'"}), 400

    # Convertir a DataFrame para poder procesarlo
    df = pd.DataFrame(datos)

    # Filtrar solo columnas numéricas (evita problemas con strings)
    df_num = df.select_dtypes(include=["number"])

    # Eliminar filas con NaN para evitar errores al entrenar el modelo
    df_num = df_num.dropna()

    # Validación mínima: se requieren al menos dos columnas numéricas (X e Y)
    if df_num.shape[1] < 2:
        return jsonify({"error": "Se requieren al menos 2 columnas numéricas"}), 400

    # Tomar la primera columna como X y la segunda como Y
    x = df_num.iloc[:, 0]
    y = df_num.iloc[:, 1]

    # Crear y entrenar el modelo de regresión lineal
    modelo = LinearRegression()
    modelo.fit(x.values.reshape(-1, 1), y)

    # Generar los valores predichos por el modelo
    y_pred = modelo.predict(x.values.reshape(-1, 1))

    # ============================================================
    #   Generación de la gráfica con Matplotlib
    # ============================================================
    plt.figure(figsize=(6, 4))  # Tamaño de la imagen

    # Puntos reales
    plt.scatter(x, y, label="Datos", alpha=0.7)

    # Línea de regresión
    plt.plot(x, y_pred, label="Línea de regresión")

    # Estética del gráfico
    plt.title("Regresión Lineal Simple")
    plt.xlabel(df_num.columns[0])  # Nombre de la columna X
    plt.ylabel(df_num.columns[1])  # Nombre de la columna Y
    plt.legend()

    # ============================================================
    #   Convertir la imagen a formato PNG y luego a base64
    # ============================================================
    buffer = io.BytesIO()                        # Buffer temporal en memoria
    plt.savefig(buffer, format="png", bbox_inches="tight")  # Guardar en buffer
    buffer.seek(0)                               # Regresar al inicio del buffer
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")  # Convertir a base64

    plt.close()  # Cerrar la figura para evitar fugas de memoria

    # ============================================================
    #   Respuesta en formato JSON
    # ============================================================
    return jsonify({
        "mime": "image/png",                     # Tipo de imagen
        "imagen": img_base64,                    # Imagen en base64 lista para frontend
        "intercepto": float(modelo.intercept_),  # Intercepto del modelo
        "coeficiente": float(modelo.coef_[0])    # Coeficiente de la regresión
    })
