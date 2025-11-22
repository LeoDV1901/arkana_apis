class CartaNFC:
    def __init__(self, data):
        self.id_carta = data.get("id_carta")
        self.propietario_actual = data.get("propietario_actual")
        self.historial_propietarios = data.get("historial_propietarios", [])
