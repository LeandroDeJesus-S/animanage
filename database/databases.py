import sqlite3
from sqlite3 import Connection, Cursor
import logging as log

from database.interface import DatabaseInterface, T


class SQLite(DatabaseInterface):
    connection = None
    cursor = None
    connected = False

    @classmethod
    def connect(cls, db: str):
        """cria conexão com a base de dados, e o atributo de instancia 
        self.cursor
        """
        log.info("SQLite connect starting")
        if cls.connected:
            return
        
        try:
            cls.connection = sqlite3.connect(db)
            cls.cursor = cls.connection.cursor()
            cls.connected = True
            log.debug("SQLite successfully connection")
        except Exception as error:
            log.debug("SQLite fail connection, error {}".format(error))
            cls.disconnect()

    @classmethod
    def disconnect(cls):
        """fecha o cursor e encerra a conexão com a base de dados."""
        log.info('SQLite disconnect function starting')
        log.debug(f'Cursor {cls.cursor} | Connection {cls.connection}')
        if not cls.connected:
            return
        
        try:
            if cls.cursor is None: return
            cls.cursor.close()
            log.info('SQLite cursor closed')
        finally:
            if cls.connection is None: return
            cls.connection.close()
            cls.connected = False
            log.info('SQLite Connection closed')
            log.info(f'SQLite Connection status: {cls.connected}')

    @classmethod
    def insert(cls, table: str, fields: tuple[str, ...], values: tuple[T, ...]):
        log.info('SQLite insert function starting')
        log.info(f'SQLite connection status: {cls.connected}')
        log.info(f'SQLite cursor status: {cls.cursor}')
        if cls.cursor is None or cls.connection is None:
            log.warning('Connection or cursor was not created')
            return
            
        cmd_fields = f'("{fields[0]}")' if len(fields) == 1 else fields
        cmd_values = f'("{values[0]}")' if len(values) == 1 else values
        try:
            cmd = f'INSERT OR IGNORE INTO {table} {cmd_fields} VALUES {cmd_values}'
            log.debug(f'command: {cmd}')
            cls.cursor.execute(cmd)
            cls.connection.commit()
            log.info(f'SQLite execute and commit called')
                
        except Exception as error:
            log.error(f'SQLite insert error: {error}')
            log.error(f'SQLite insert error args: {error.args}')
            log.error(f'SQLite insert error cause: {error.__cause__}')
            log.error(f'SQLite insert error context: {error.__context__}')
            log.error(f'SQLite insert error traceback: {error.__traceback__}')
            print('Error:', error)
            cls.disconnect()

    @classmethod
    def select(cls, table: str, limit: int=60, where: str= '',
               like: str='', insensitive: bool=False) -> list[tuple]:
        """faz um select * na base de dados com limit 60 por padrão.
        para retirar o limit basta passar 0 como valor
        Args:
            table (str): nome da tabela do banco de dados
            limit (int, optional): limite de dados para consulta. Defaults to 60.
            where (str, optional): campo para comando where. Defaults to ''.
            like (str, optional): valor da consulta do where. Defaults to ''.
        Raises:
            ValueError: caso limit não seja do tipo int
            SyntaxError: caso 'where' seja enviado sem o 'like' ou o inverso.
        Returns:
            list[tuple]: resultado da consulta
        """
        log.info('select function started')
        log.debug(f'Connection status: {cls.connected}')
        log.debug(f'cursor status: {cls.cursor}')
        if not (cls.connection and cls.cursor):
            log.warning('Connection or cursor was not created')
            return []
        
        if limit and not isinstance(limit, int):
            log.error(f'limit was called and limit is not an integer')
            cls.connection.close()
            log.debug(f'connection connection closed')
            raise ValueError('limit must be an integer')
        
        cmd = f'SELECT * FROM {table}'
        if where and not insensitive:
            cmd += F' WHERE "{where}" LIKE "{like}"'
            
        elif where and insensitive:
            cmd += F' WHERE "{where}" LIKE "%{like}%"'
            
        cmd += f' ORDER BY {where} ASC LIMIT {limit}'
        log.debug(f'command: {cmd}')
        
        try:
            cls.cursor.execute(cmd)
            results = cls.cursor.fetchall()
            log.debug(f'results: {results}')
            return results
        except Exception as error:
            log.error(f'error: {error}')
            log.error(f'args error: {error.args}')
            log.error(f'error traceback: {error.__traceback__}')
            log.error(f'error cause: {error.__cause__}')
            cls.disconnect()
            return []

    @classmethod
    def update(cls, table: str, setField: str,
               setValue: str, whereField: str, whereValue: str):
        """atualiza um campo da base de dados
        Args:
            table (str): nome da tabela
            setField (str): nome do campo que sera alterado
            setValue (str): valor do campo que sera alterado
            whereField (str): nome do campo para identificação
            whereValue (str): valor do campo de identificação
        """
        cmd = f'UPDATE {table} SET {setField}=:setValue WHERE {whereField}=:whereValue'

        value = {'setValue': setValue, 'whereValue': whereValue}
        
        try:
            if not (cls.cursor and cls.connection):
                log.warning(f'cursor or connection was not created')
                return
            
            cls.cursor.execute(cmd, value)
            cls.connection.commit()
        except Exception as error:
            log.error('Error: {}'.format(error))
            cls.disconnect()

    @classmethod
    def delete(cls, table: str, where: str, like: str):
        """deleta um registro do banco de dados
        Args:
            table (str): nome da tabela
            where (str): nome do campo para identificação
            like (str): valor do campo para identificação
        """
        if not (isinstance(where, str) and isinstance(like, str)) and isinstance(table, str):
            cls.disconnect()
            raise TypeError('table, where and like must be strings')
        
        cmd = f'DELETE FROM {table} WHERE {where} LIKE "{like}"'
        log.debug(f'command: {cmd}')
        
        try:
            if not (cls.cursor and cls.connection):
                log.warning(f'cursor or connection was not created')
                return
            
            cls.cursor.execute(cmd)
            cls.connection.commit()
        except Exception as error:
            log.error('Error:'.format(error))
            cls.disconnect()
