import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, count as spark_count, desc
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
import matplotlib.pyplot as plt
import os
from Extensions import mongo

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def init_spark():
    """
    Inicializa Spark 4.0.1 con el conector de MongoDB.
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
        spark = init_spark()

        # === Leer colecciones ===
        usuarios = spark.read.format("mongo").option("collection", "usuarios").load()
        cartas = spark.read.format("mongo").option("collection", "cartas").load()
        partidas = spark.read.format("mongo").option("collection", "partidas").load()
        estadisticas = spark.read.format("mongo").option("collection", "estadisticas").load()

        # === Estadísticas simples ===
        total_usuarios = usuarios.count()
        total_cartas = cartas.count()
        total_partidas = partidas.count()

        # === Top cartas más usadas ===
        try:
            if "cartas_usadas" in partidas.columns:
                exploded = partidas.select(explode("cartas_usadas").alias("id_carta"))
                top = (
                    exploded.groupBy("id_carta")
                    .agg(spark_count("*").alias("uso_count"))
                    .orderBy(desc("uso_count"))
                )

                top_cartas_pdf = top.toPandas()
                top_cartas_pdf.to_csv(f"{OUTPUT_DIR}/top_cartas.csv", index=False)
            else:
                top_cartas_pdf = pd.DataFrame()

        except Exception as e:
            top_cartas_pdf = pd.DataFrame()
            print("Error en cálculo de top cartas:", e)

        # === Modelo de regresión lineal para ranking ===
        model_info = {}

        try:
            required_cols = {"partidas_ganadas", "partidas_perdidas", "ranking"}

            if required_cols <= set(estadisticas.columns):

                df = estadisticas.select(
                    col("partidas_ganadas"),
                    col("partidas_perdidas"),
                    col("ranking")
                ).dropna()

                assembler = VectorAssembler(
                    inputCols=["partidas_ganadas", "partidas_perdidas"],
                    outputCol="features"
                )

                df2 = assembler.transform(df)

                lr = LinearRegression(
                    featuresCol="features",
                    labelCol="ranking"
                )

                lr_model = lr.fit(df2)

                model_info = {
                    "coefficients": lr_model.coefficients.tolist(),
                    "intercept": lr_model.intercept,
                    "r2": lr_model.summary.r2,
                    "rmse": lr_model.summary.rootMeanSquaredError
                }

                # === gráfica real vs predicho ===
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
                model_info["error"] = "Faltan columnas necesarias en la colección 'estadisticas'."

        except Exception as e:
            model_info["error"] = str(e)

        spark.stop()

        # === Resultado final ===
        return {
            "total_usuarios": total_usuarios,
            "total_cartas": total_cartas,
            "total_partidas": total_partidas,
            "top_cartas": top_cartas_pdf.to_dict(orient="records"),
            "modelo_regresion": model_info
        }
