import sqlite3

# Establish a connection to the SQLite database
with sqlite3.connect('lib/dogs.db') as CONN:
    # Create a cursor to execute SQL queries
    CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        # Constructor for the Dog class
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        # Create the 'dogs' table if it doesn't exist
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # Drop the 'dogs' table if it exists
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        # Insert a new dog record into the 'dogs' table
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        # Update the dog instance with the last inserted row ID
        self.id = CURSOR.lastrowid
    
    @classmethod
    def create(cls, name, breed):
        # Create a new dog instance, save it, and return the instance
        dog = cls(name, breed) 
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        # Create a new dog instance from a database row
        id, name, breed = row
        return cls(name, breed, id)
    
    @classmethod
    def get_all(cls):
        # Retrieve all dogs from the 'dogs' table
        sql = """
            SELECT * FROM dogs
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        # Create a list of dog instances from the rows
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs
    
    @classmethod
    def find_by_name(cls, name):
        # Find a dog by name in the 'dogs' table
        sql = """
            SELECT * FROM dogs
            WHERE name = ? LIMIT 1
        """
        CURSOR.execute(sql, (name,))
        rows = CURSOR.fetchall()
        # Return the first dog instance found, or None if not found
        return cls.new_from_db(rows[0]) if rows else None
    
    @classmethod
    def find_by_id(cls, dog_id):
        # Find a dog by ID in the 'dogs' table
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
        """
        CURSOR.execute(sql, (dog_id,))
        rows = CURSOR.fetchall()
        # Return the first dog instance found, or None if not found
        return cls.new_from_db(rows[0]) if rows else None
            
    @classmethod
    def find_or_create_by(cls, name, breed):
        # Find a dog by name and breed, or create a new one if not found
        sql = """
            SELECT * FROM dogs
            WHERE name = ? AND breed = ? LIMIT 1
        """
        CURSOR.execute(sql, (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            dog = cls(name, breed)
            dog.save()
            return dog
    
    def update(self):
        # Update the information of an existing dog in the 'dogs' table
        sql = """
            UPDATE dogs
            SET name = ?, breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
