from flask import Blueprint, jsonify
from Extensions import mongo
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from sklearn.linear_model import LinearRegression

regresion_bp = Blueprint("regresion_bp", __name__)

# ==========================
# GET: Datos de regresión simple como imagen
# ==========================
@regresion_bp.get("")
def grafica_regresion_simple():
    coleccion = mongo.db.estadisticas
    datos = list(coleccion.find({}, {"_id": 0}))
    df = pd.DataFrame(datos)

    # Filtra solo columnas numéricas
    df_num = df.select_dtypes(include=["number"])

    if df_num.shape[1] < 2:
        return jsonify({"error": "No hay suficientes columnas numéricas para regresión"}), 400

    x = df_num.iloc[:, 0]
    y = df_num.iloc[:, 1]

    modelo = LinearRegression()
    modelo.fit(x.values.reshape(-1, 1), y)

    y_pred = modelo.predict(x.values.reshape(-1, 1))

    plt.figure(figsize=(6,4))
    plt.scatter(x, y, color="blue", label="Datos")
    plt.plot(x, y_pred, color="red", label="Predicción")
    plt.legend()
    plt.title("Regresión Lineal Simple")
    plt.xlabel(df_num.columns[0])
    plt.ylabel(df_num.columns[1])

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    plt.close()

    return jsonify({
        "mime": "image/png",
        "imagen": img_base64
    })
