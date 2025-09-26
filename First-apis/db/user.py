import pyodbc

class UserDatabase():
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Sahil;DATABASE=cafe;')
        self.cursor = self.conn.cursor()

    
    def get_user(self, user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        self.cursor.execute(query)    
        user = {}
        result = self.cursor.fetchone()
        if result is not None:
            user['id'], user['username'], user['password'] = result 
            return user

    
    def add_user(self, username, password):
        query = f"insert into users(username, password) values ('{username}','{password}')"
        try:
            self.cursor.execute(query)
            self.conn.commit()
            return True
        except pyodbc.IntegrityError:
            return False

    def delete_user(self,id):
        query = f"DELETE FROM users WHERE id = {id};"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True 


    def verify_user(self, username, password):
        query = f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"  
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]