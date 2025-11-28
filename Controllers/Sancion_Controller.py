from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Sancion import Sancion
from Extensions import mongo

class SancionController:

    @staticmethod
    def crear():
        """
        Crear una nueva sanción para un usuario.
        - Obtiene el JSON enviado por el cliente.
        - Lo convierte en un objeto Sancion.
        - Lo guarda en la colección 'sanciones'.
        """
        data = request.json
        sancion = Sancion(data).__dict__  # Convertimos el modelo a diccionario
        mongo.db.sanciones.insert_one(sancion)  # Guardar en la DB
        return jsonify({"msg": "Sanción aplicada"}), 201

    @staticmethod
    def obtener_por_usuario(id_usuario):
        """
        Obtener todas las sanciones asociadas a un usuario específico.
        - Busca por 'id_usuario' en la colección.
        - Convierte los ObjectId en strings para evitar problemas con JSON.
        """
        sanciones = list(mongo.db.sanciones.find({"id_usuario": id_usuario}))

        # Convertir _id de ObjectId → string
        for s in sanciones:
            s["_id"] = str(s["_id"])

        return jsonify(sanciones)

    @staticmethod
    def eliminar(id):
        """
        Eliminar una sanción por su ID.
        - Convierte el ID recibido a ObjectId.
        - Elimina la sanción de la colección.
        """
        mongo.db.sanciones.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Sanción eliminada"})
