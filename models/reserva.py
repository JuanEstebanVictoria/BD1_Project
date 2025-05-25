class Reserva:
    def __init__(self, id, nombre_huesped, habitacion_id, fecha_entrada, fecha_salida, estado, check_in=None, check_out=None, huesped_id=None):
        self.id = id
        self.nombre_huesped = nombre_huesped
        self.habitacion_id = habitacion_id
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado = estado
        self.check_in = check_in
        self.check_out = check_out
        self.huesped_id = huesped_id
