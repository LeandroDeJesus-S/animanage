import sqlite3
from sqlite3 import Connection, Cursor

from database.interface import DatabaseInterface, T

class SQLite(DatabaseInterface):
    def __init__(self):
        self.connection: Connection
        self.cursor: Cursor
        self.connected: bool = False

    def connect(self, db: str):
        """cria conexão com a base de dados, e o atributo de instancia 
        self.cursor
        """
        if self.connected:
            return
        
        try:
            self.connection = sqlite3.connect(db)
            self.cursor = self.connection.cursor()
            self.connected = True
        except Exception as error:
            print('Erro durante conexão à DB:', error)
            self.disconnect()

    def disconnect(self):
        """fecha o cursor e encerra a conexão com a base de dados."""
        if not self.connected:
            return
        
        try:
            self.cursor.close()
        finally:
            self.connection.close()
            self.connected = False
    
    def insert(self, table: str, fields: tuple[str, ...], values: tuple[T, ...]):
        try:
            cmd = f'INSERT OR IGNORE INTO {table} {fields} VALUES {values}'
            self.cursor.execute(cmd)
            self.connection.commit()
        except Exception as error:
            print('Erro:', error)
        finally:
            self.disconnect()
                    
    def select(self, table: str, limit: int=60, where: str='', 
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
            self.connection.close()
            raise ValueError('limit must be an integer')
        
        cmd = f'SELECT * FROM {table}'
        if where and not insensitive:
            cmd += F' WHERE "{where}" LIKE "{like}"'
            
        elif where and insensitive:
            cmd += F' WHERE "{where}" LIKE "%{like}%"'
            
        cmd += f' LIMIT {limit}'
        
        try:
            self.cursor.execute(cmd)
            return self.cursor.fetchall()
        except Exception as error:
            print('Error:', error)
            self.disconnect()
            return []
    
    def update(self, table: str, setField: str, 
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
            self.cursor.execute(cmd, value)
            self.connection.commit()
        except Exception as error:
            print('Error:', error)
        finally:
            self.disconnect()
    
    def delete(self, table: str, where: str, like: str):
        """deleta um registro do banco de dados
        Args:
            table (str): nome da tabela
            where (str): nome do campo para identificação
            like (str): valor do campo para identificação
        """
        if not (isinstance(where, str) and isinstance(like, str)) and isinstance(table, str):
            self.disconnect()
            raise TypeError('table, where and like must be strings')
        
        cmd = f'DELETE FROM {table} WHERE {where} LIKE "{like}"'
        try:
            self.cursor.execute(cmd)
            self.connection.commit()
        except Exception as error:
            print('Error:', error)
        finally:
            self.disconnect()
