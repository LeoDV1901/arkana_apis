import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, count as spark_count, desc
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
import matplotlib.pyplot as plt
import os
from Extensions import mongo

# Carpeta donde se guardarán archivos como CSV o imágenes generadas
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def init_spark():
    """
    Inicializa una sesión de Spark 4.0.1 con el conector de MongoDB ya configurado.

    - Usa las variables de entorno para obtener la URL de conexión a MongoDB.
    - Carga automáticamente el paquete del conector Mongo-Spark.
    """
    return (
        SparkSession.builder
        .appName("EstadisticasSpark")
        .config("spark.mongodb.read.connection.uri", os.getenv("MONGO_URL"))
        .config("spark.mongodb.write.connection.uri", os.getenv("MONGO_URL"))
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:4.0.1")
        .getOrCreate()
    )


class EstadisticasService:

    @staticmethod
    def generar_estadisticas_spark():
        """
        Genera estadísticas globales utilizando Apache Spark.

        Incluye:
        - Conteos de usuarios, cartas y partidas.
        - Cálculo de las cartas más usadas.
        - Entrenamiento de una regresión lineal para predecir ranking.
        """

        # === Inicializar Spark ===
        spark = init_spark()

        # === Leer colecciones desde Mongo ===
        usuarios = spark.read.format("mongo").option("collection", "usuarios").load()
        cartas = spark.read.format("mongo").option("collection", "cartas").load()
        partidas = spark.read.format("mongo").option("collection", "partidas").load()
        estadisticas = spark.read.format("mongo").option("collection", "estadisticas").load()

        # === Estadísticas básicas ===
        total_usuarios = usuarios.count()
        total_cartas = cartas.count()
        total_partidas = partidas.count()

        # ==========================================
        # TOP — Cálculo de cartas más usadas
        # ==========================================
        try:
            # Solo si la columna existe en la colección
            if "cartas_usadas" in partidas.columns:

                # Explode permite convertir listas en múltiples filas
                exploded = partidas.select(explode("cartas_usadas").alias("id_carta"))

                # Contar frecuencia de cada carta y ordenar descendentemente
                top = (
                    exploded.groupBy("id_carta")
                    .agg(spark_count("*").alias("uso_count"))
                    .orderBy(desc("uso_count"))
                )

                # Convertir resultado Spark → Pandas para guardarlo
                top_cartas_pdf = top.toPandas()
                top_cartas_pdf.to_csv(f"{OUTPUT_DIR}/top_cartas.csv", index=False)
            else:
                top_cartas_pdf = pd.DataFrame()

        except Exception as e:
            # En caso de error prevenir que falle todo el pipeline
            top_cartas_pdf = pd.DataFrame()
            print("Error en cálculo de top cartas:", e)

        # ==========================================
        # Modelo de regresión lineal (Spark ML)
        # ==========================================
        model_info = {}
        try:
            # Columnas necesarias para entrenar el modelo
            required_cols = {"partidas_ganadas", "partidas_perdidas", "ranking"}

            # Validar que existan en la colección
            if required_cols <= set(estadisticas.columns):

                # Seleccionar solo columnas necesarias y eliminar filas con NA
                df = estadisticas.select(
                    col("partidas_ganadas"),
                    col("partidas_perdidas"),
                    col("ranking")
                ).dropna()

                # Ensamblar características en un vector (Spark ML requiere esto)
                assembler = VectorAssembler(
                    inputCols=["partidas_ganadas", "partidas_perdidas"],
                    outputCol="features"
                )
                df2 = assembler.transform(df)

                # Configurar el modelo de regresión lineal
                lr = LinearRegression(
                    featuresCol="features",
                    labelCol="ranking"
                )

                # Entrenar el modelo
                lr_model = lr.fit(df2)

                # Guardar métricas del modelo
                model_info = {
                    "coefficients": lr_model.coefficients.tolist(),
                    "intercept": lr_model.intercept,
                    "r2": lr_model.summary.r2,
                    "rmse": lr_model.summary.rootMeanSquaredError
                }

                # === Crear gráfica real vs predicho ===
                preds = lr_model.transform(df2).toPandas()

                plt.figure()
                plt.scatter(preds["ranking"], preds["prediction"])
                plt.xlabel("Ranking real")
                plt.ylabel("Predicción")
                plt.title("Regresión Lineal — Ranking")

                path = f"{OUTPUT_DIR}/regresion_ranking.png"
                plt.savefig(path, dpi=120)
                plt.close()

                model_info["grafica"] = path

            else:
                model_info["error"] = (
                    "Faltan columnas necesarias en la colección 'estadisticas'. "
                    "Se requieren: partidas_ganadas, partidas_perdidas, ranking"
                )

        except Exception as e:
            model_info["error"] = str(e)

        # === Detener Spark ===
        spark.stop()

        # === Construir respuesta final ===
        return {
            "total_usuarios": total_usuarios,
            "total_cartas": total_cartas,
            "total_partidas": total_partidas,
            "top_cartas": top_cartas_pdf.to_dict(orient="records"),
            "modelo_regresion": model_info
        }
