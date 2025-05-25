class Reserva:
    def __init__(self, id, huesped_id, habitacion_id, fecha_entrada, fecha_salida, estado):
        self.id = id
        self.huesped_id = huesped_id
        self.habitacion_id = habitacion_id
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado = estado
