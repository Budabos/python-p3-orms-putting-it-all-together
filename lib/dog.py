import sqlite3

with sqlite3.connect('lib/dogs.db') as CONN:
    CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
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
        sql = """
            DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)
        CONN.commit()
        
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?,?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    @classmethod
    def create(cls,name,breed):
       dog = cls(name, breed) 
       dog.save()
       return dog

    @classmethod
    def new_from_db(cls, row):
        id = row[0]
        name = row[1]
        breed = row[2]
        dog = cls(name, breed, id)
        return dog
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """

        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs
            WHERE name =? LIMIT 1
        """

        CURSOR.execute(sql, (name,))
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs[0] if dogs else None
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs
            WHERE id =?
        """
        
        CURSOR.execute(sql, (id,))
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs[0] if dogs else None
            
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT * FROM dogs
            WHERE name =? AND breed =? LIMIT 1
        """

        CURSOR.execute(sql, (name, breed))
        rows = CURSOR.fetchall()
        dogs = []
        for row in rows:
            dog = cls.new_from_db(row)
            dogs.append(dog)
        if len(dogs) == 0:
            dog = cls(name, breed)
            dog.save()
            return dog
        else:
            return dogs[0]
    
    def update(self):
        sql = """
            UPDATE dogs
            SET name =?, breed =?
            WHERE id =?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()