from conexion import Conexion
from logger_base import log

class CursorPool:
    def __init__(self):
        self._conexion = None
        self._cursor = None

    def __enter__(self):
        log.debug('Inicio del metodo with __enter__')
        self._conexion = Conexion.obtenerConexion()
        self._cursor = self._conexion.cursor()
        return self._cursor

    def __exit__(self, tipo_excepcion, valor_excepcion, detalle_excepcion):
        log.debug('Se ejecutara metodo __exit__')
        if self._conexion:
            self._conexion.rollback()
            log.error(f'Ocurrio una excepcion : {detalle_excepcion} {tipo_excepcion} {valor_excepcion}')
        else:
            self._conexion.commit()
            log.debug('Commit de la transaccion')
        self._conexion.close()
        Conexion.liberarConexion(self._conexion)

if __name__ == '__main__':
   with CursorPool() as cursor:
       log.debug('Dentro del bloque with')
       cursor.execute('select * from persona')
       log.debug(cursor.fetchall())