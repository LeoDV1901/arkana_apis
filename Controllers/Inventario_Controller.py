from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Inventario import Inventario
from Extensions import mongo

class InventarioController:

    @staticmethod
    def agregar():
        """
        Agrega una carta o ítem al inventario de un usuario.

        Flujo:
        1. Se recibe el JSON del cliente.
        2. Se convierte en un objeto Inventario.
        3. Se guarda el documento en la colección 'inventario'.
        """
        data = request.json
        inv = Inventario(data).__dict__  # Convertir el modelo a dict
        mongo.db.inventario.insert_one(inv)  # Insertar en MongoDB

        return jsonify({"msg": "Carta agregada al inventario"}), 201

    @staticmethod
    def obtener_por_usuario(id_usuario):
        """
        Obtiene todos los ítems del inventario de un usuario.

        - Se busca por id_usuario en la colección.
        - Cada ObjectId se convierte a string para permitir respuesta JSON válida.
        """
        items = list(mongo.db.inventario.find({"id_usuario": id_usuario}))

        for item in items:
            item["_id"] = str(item["_id"])

        return jsonify(items)

    @staticmethod
    def eliminar(id):
        """
        Elimina un ítem específico del inventario.

        - Convierte el ID recibido a ObjectId.
        - Elimina el documento correspondiente.
        """
        mongo.db.inventario.delete_one({"_id": ObjectId(id)})

        return jsonify({"msg": "Eliminado del inventario"})
