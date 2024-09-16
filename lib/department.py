import sqlite3

# Ensure CURSOR and CONN are defined and initialized
from __init__ import CURSOR, CONN

class Department:
    def __init__(self, name, location, id=None):
        self.name = name
        self.location = location
        self.id = id

    @classmethod
    def create_table(cls):
        '''Creates the departments table if it does not exist.'''
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        '''Drops the departments table if it exists.'''
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        '''Saves the instance to the database.'''
        if self.id is None:
            # Insert new department
            sql = """
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.location))
            self.id = CURSOR.lastrowid
            CONN.commit()
        else:
            # Update existing department
            self.update()

    @classmethod
    def create(cls, name, location):
        '''Creates a new department instance and saves it to the database.'''
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        '''Updates the instance's corresponding database row.'''
        if self.id is not None:
            sql = """
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.location, self.id))
            CONN.commit()

    def delete(self):
        '''Deletes the instance's corresponding database row.'''
        if self.id is not None:
            sql = "DELETE FROM departments WHERE id = ?"
            CURSOR.execute(sql, (self.id,))
            CONN.commit()
            self.id = None

