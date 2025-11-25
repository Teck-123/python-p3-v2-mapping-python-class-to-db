import sqlite3

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

class Department:
    @classmethod
    def create_table(cls):
        """Create the departments table if it doesn't exist"""
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the departments table if it exists"""
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def save(self):
        """Insert a new row if id is None, Otherwise update existing row"""
        if self.id is None:
            sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.location, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Create and save a new department, return the instance"""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the current instance's row in the db"""
        self.save()

    def delete(self):
        """Delete this department's row from the db"""
        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"
