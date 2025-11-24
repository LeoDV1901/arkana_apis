import os
os.environ["PYSPARK_PYTHON"] = r"C:\Users\leeov\AppData\Local\Programs\Python\Python310\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\leeov\AppData\Local\Programs\Python\Python310\python.exe"

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, max, min, sum, round as spark_round
)
from pymongo import MongoClient
import certifi
from datetime import datetime


def correr_spark():

    # ----------------------------
    # 1. Conectar a MongoDB
    # ----------------------------
    client = MongoClient(
        "mongodb+srv://marcosj9807_db_user:GQ3MEg7vIKovKO0z@arkana.ge1yf3l.mongodb.net/arkana?retryWrites=true&w=majority&appName=Spark",
        tls=True,
        tlsCAFile=certifi.where()
    )

    db = client["arkana"]
    coleccion = db["estadisticas"]
    coleccion_global = db["estadisticas_globales"]  # <<--- Nueva colección

    registros = list(coleccion.find({}, {"_id": 0}))

    if not registros:
        print("❌ No hay datos en la colección.")
        return

    # ----------------------------
    # 2. Crear sesión Spark
    # ----------------------------
    spark = SparkSession.builder \
        .appName("Spark_Estadisticas_Simples") \
        .getOrCreate()

    # ----------------------------
    # 3. Crear DataFrame
    # ----------------------------
    df = spark.createDataFrame(registros)

    print("\n📌 Datos cargados:")
    df.show(10, truncate=False)

    # ----------------------------
    # 4. Estadísticas simples
    # ----------------------------

    # Total de registros
    total_registros = df.count()
    print(f"\n📊 Total de registros: {total_registros}")

    # Promedios
    promedios_df = df.select(
        avg("partidas_ganadas").alias("promedio_ganadas"),
        avg("partidas_perdidas").alias("promedio_perdidas"),
        avg("cartas_usadas").alias("promedio_cartas"),
        avg("ranking").alias("promedio_ranking")
    )
    promedios = promedios_df.collect()[0].asDict()

    print("\n📈 Promedios:")
    promedios_df.show()

    # Máximos y mínimos
    extremos_df = df.select(
        max("partidas_ganadas").alias("max_ganadas"),
        min("partidas_ganadas").alias("min_ganadas"),
        max("ranking").alias("ranking_max"),
        min("ranking").alias("ranking_min")
    )
    extremos = extremos_df.collect()[0].asDict()

    print("\n📌 Máximos y mínimos:")
    extremos_df.show()

    # Winrate global
    winrate_df = df.select(
        spark_round(
            sum("partidas_ganadas") /
            (sum("partidas_ganadas") + sum("partidas_perdidas")) * 100,
            2
        ).alias("winrate_global")
    )
    winrate_global = winrate_df.collect()[0]["winrate_global"]

    print("\n🏆 Winrate global:")
    winrate_df.show()

    # Cartas usadas por partida
    df2 = df.withColumn(
        "cartas_por_partida",
        col("cartas_usadas") / (col("partidas_ganadas") + col("partidas_perdidas"))
    )

    print("\n🃏 Cartas usadas por partida (métrica nueva):")
    df2.select("id_usuario", "cartas_por_partida").show(10, truncate=False)

    # Top 5 rankings
    top5_rank = df.orderBy(col("ranking").desc()).select("id_usuario", "ranking").limit(5)
    top5_ranking = [row.asDict() for row in top5_rank.collect()]

    print("\n⭐ Top 5 jugadores con mejor ranking:")
    top5_rank.show(truncate=False)

    # Mejor winrate
    df3 = df.withColumn(
        "winrate",
        spark_round(
            (col("partidas_ganadas") / (col("partidas_ganadas") + col("partidas_perdidas"))) * 100,
            2
        )
    )

    top5_winrate_df = df3.orderBy(col("winrate").desc()).select("id_usuario", "winrate").limit(5)
    top5_winrate = [row.asDict() for row in top5_winrate_df.collect()]

    print("\n🔥 Jugadores con mejor winrate:")
    top5_winrate_df.show(truncate=False)

    # ----------------------------
    # 5. Guardar resultados en MongoDB
    # ----------------------------
    documento_final = {
        "fecha_generado": datetime.utcnow(),
        "total_registros": total_registros,
        "promedios": promedios,
        "extremos": extremos,
        "winrate_global": winrate_global,
        "top5_ranking": top5_ranking,
        "top5_winrate": top5_winrate
    }

    coleccion_global.insert_one(documento_final)

    print("\n💾 Datos guardados en la colección 'estadisticas_globales'.")
    print("\n✔ Finalizado.")


if __name__ == "__main__":
    correr_spark()
