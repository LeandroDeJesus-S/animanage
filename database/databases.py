import sqlite3
from sqlite3 import Connection, Cursor

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
        if cls.connected:
            return
        
        try:
            cls.connection = sqlite3.connect(db)
            cls.cursor = cls.connection.cursor()
            cls.connected = True
        except Exception as error:
            print('Erro durante conexão à DB:', error)
            cls.disconnect()

    @classmethod
    def disconnect(cls):
        """fecha o cursor e encerra a conexão com a base de dados."""
        if not cls.connected:
            return
        
        try:
            cls.cursor.close()
        finally:
            cls.connection.close()
            cls.connected = False

    @classmethod
    def insert(cls, table: str, fields: tuple[str, ...], values: tuple[T, ...]):
        try:
            cmd = f'INSERT OR IGNORE INTO {table} {fields} VALUES {values}'
            cls.cursor.execute(cmd)
            cls.connection.commit()
        except Exception as error:
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
        if limit and not isinstance(limit, int):
            cls.connection.close()
            raise ValueError('limit must be an integer')
        
        cmd = f'SELECT * FROM {table}'
        if where and not insensitive:
            cmd += F' WHERE "{where}" LIKE "{like}"'
            
        elif where and insensitive:
            cmd += F' WHERE "{where}" LIKE "%{like}%"'
            
        cmd += f' LIMIT {limit}'
        
        try:
            cls.cursor.execute(cmd)
            return cls.cursor.fetchall()
        except Exception as error:
            print('Error:', error)
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
            cls.cursor.execute(cmd, value)
            cls.connection.commit()
        except Exception as error:
            print('Error:', error)
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
        try:
            cls.cursor.execute(cmd)
            cls.connection.commit()
        except Exception as error:
            print('Error:', error)
            cls.disconnect()
