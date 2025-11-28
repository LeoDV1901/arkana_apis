import os
# Se especifican las rutas del intérprete Python que usará PySpark
os.environ["PYSPARK_PYTHON"] = r"C:\Users\marco\miniconda3\envs\ejemplo\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\marco\miniconda3\envs\ejemplo\python.exe"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min, sum, round as spark_round
from pymongo import MongoClient
import certifi
from datetime import datetime

def correr_spark():
    # ----------------------------
    # 1. Conectar a MongoDB
    # ----------------------------
    # Se crea un cliente Mongo con conexión segura usando certificado CA
    client = MongoClient(
        "mongodb+srv://marcosj9807_db_user:GQ3MEg7vIKovKO0z@arkana.ge1yf3l.mongodb.net/arkana?retryWrites=true&w=majority&appName=Spark",
        tls=True,
        tlsCAFile=certifi.where()
    )

    db = client["arkana"]
    coleccion = db["estadisticas"]
    coleccion_global = db["estadisticas_globales"]

    # Obtiene todos los registros sin incluir el _id
    registros = list(coleccion.find({}, {"_id": 0}))

    if not registros:
        print("No hay datos en la colección.")
        return

    # ----------------------------
    # 2. Limpiar/convertir datos (Decimal128 -> float)
    # ----------------------------
    # Convierte valores tipo Decimal128 a float para evitar errores de Spark
    for r in registros:
        for k, v in r.items():
            try:
                r[k] = float(v)
            except:
                pass

    # ----------------------------
    # 3. Crear sesión Spark
    # ----------------------------
    # Se crea la sesión Spark con configuraciones adicionales para manejo de fallas
    spark = SparkSession.builder \
        .appName("Spark_Estadisticas_Simples") \
        .master("local[*]") \
        .config("spark.python.worker.faulthandler.enabled", "true") \
        .config("spark.sql.execution.pyspark.udf.faulthandler.enabled", "true") \
        .getOrCreate()

    # ----------------------------
    # 4. Crear DataFrame
    # ----------------------------
    # Se cargan los datos en Spark como DataFrame
    df = spark.createDataFrame(registros)

    print("\nDatos cargados (solo 5 filas para debug):")
    df.limit(5).show(truncate=False)

    # ----------------------------
    # 5. Estadísticas simples
    # ----------------------------

    # Número total de registros
    total_registros = df.count()
    print(f"\nTotal de registros: {total_registros}")

    # Cálculo de promedios de métricas principales
    promedios_df = df.select(
        avg("partidas_ganadas").alias("promedio_ganadas"),
        avg("partidas_perdidas").alias("promedio_perdidas"),
        avg("cartas_usadas").alias("promedio_cartas"),
        avg("ranking").alias("promedio_ranking")
    )
    promedios = promedios_df.collect()[0].asDict()

    print("\nPromedios:")
    promedios_df.show(truncate=False)

    # Cálculo de valores máximos y mínimos
    extremos_df = df.select(
        max("partidas_ganadas").alias("max_ganadas"),
        min("partidas_ganadas").alias("min_ganadas"),
        max("ranking").alias("ranking_max"),
        min("ranking").alias("ranking_min")
    )
    extremos = extremos_df.collect()[0].asDict()

    print("\nMáximos y mínimos:")
    extremos_df.show(truncate=False)

    # Cálculo del winrate global
    winrate_df = df.select(
        spark_round(
            sum("partidas_ganadas") /
            (sum("partidas_ganadas") + sum("partidas_perdidas")) * 100,
            2
        ).alias("winrate_global")
    )
    winrate_global = winrate_df.collect()[0]["winrate_global"]

    print("\nWinrate global:")
    winrate_df.show(truncate=False)

    # Cálculo de cartas utilizadas por partida de cada usuario
    df2 = df.withColumn(
        "cartas_por_partida",
        col("cartas_usadas") / (col("partidas_ganadas") + col("partidas_perdidas"))
    )
    print("\nCartas usadas por partida:")
    df2.select("id_usuario", "cartas_por_partida").show(5, truncate=False)

    # Top 5 de jugadores con mejor ranking
    top5_rank = df.orderBy(col("ranking").desc()).select("id_usuario", "ranking").limit(5)
    top5_ranking = [row.asDict() for row in top5_rank.collect()]

    print("\nTop 5 jugadores con mejor ranking:")
    top5_rank.show(truncate=False)

    # Cálculo de winrate por usuario
    df3 = df.withColumn(
        "winrate",
        spark_round(
            (col("partidas_ganadas") / (col("partidas_ganadas") + col("partidas_perdidas"))) * 100,
            2
        )
    )

    # Top 5 de winrate
    top5_winrate_df = df3.orderBy(col("winrate").desc()).select("id_usuario", "winrate").limit(5)
    top5_winrate = [row.asDict() for row in top5_winrate_df.collect()]

    print("\nJugadores con mejor winrate:")
    top5_winrate_df.show(truncate=False)

    # ----------------------------
    # 6. Guardar resultados en MongoDB
    # ----------------------------
    # Se crea un documento con todas las métricas para almacenarlo en otra colección
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

    print("\nDatos guardados en la colección 'estadisticas_globales'.")
    print("\nProceso finalizado.")

if __name__ == "__main__":
    correr_spark()
