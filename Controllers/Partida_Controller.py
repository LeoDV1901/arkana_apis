from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Partida import Partida
from Extensions import mongo

class PartidaController:

    @staticmethod
    def crear():
        """
        Crea una nueva partida.
        
        Flujo:
        1. Lee el JSON recibido desde el cliente.
        2. Convierte los datos al modelo Partida.
        3. Inserta el documento en la colección 'partidas'.
        """
        data = request.json
        partida = Partida(data).__dict__  # Convertir el modelo a diccionario
        mongo.db.partidas.insert_one(partida)  # Guardar en MongoDB

        return jsonify({"msg": "Partida registrada"}), 201

    @staticmethod
    def obtener_todas():
        """
        Obtiene todas las partidas registradas.
        
        - Convierte cada ObjectId en string para que sea serializable en JSON.
        """
        partidas = list(mongo.db.partidas.find())

        # Convertir ObjectId → string
        for p in partidas:
            p["_id"] = str(p["_id"])

        return jsonify(partidas)

    @staticmethod
    def obtener(id):
        """
        Obtiene una partida específica por su ID.
        
        - Si no existe, retorna error 404.
        - Si existe, convierte el _id a string y la retorna.
        """
        p = mongo.db.partidas.find_one({"_id": ObjectId(id)})

        if not p:
            return jsonify({"error": "No encontrada"}), 404

        p["_id"] = str(p["_id"])
        return jsonify(p)
