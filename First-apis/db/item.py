import pyodbc

class ItemDatabase():
    def __init__(self):
        self.conn = conn = pyodbc.connect('DRIVER={SQL Server};SERVER=Sahil;DATABASE=cafe;')
        self.cursor = self.conn.cursor()

    def get_items(self):
        result =[]
        query = "select * from item"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item = {}
            item['id'] = row[0]
            item['name'] = row[1]
            item['price'] = row[2]
            result.append(item)
        return result         

    def get_item(self, item_id):
        query = f"SELECT * FROM item WHERE id = '{item_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            item = {}
            item['id'] = row[0]
            item['name'] = row[1]
            item['price'] = row[2]
        return [item]

    def update_item(self, id, body):
        query = f"UPDATE item SET price = {body['price']}, name = '{body['name']}' WHERE id = '{id}';"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True

    def add_item(self, id, body):
        query = f"insert into item(id, name, price) values ('{id}', '{body['name']}',{body['price']})"
        self.cursor.execute(query)
        self.conn.commit()

    def delete_item(self,id):
        query = f"DELETE FROM item WHERE id = '{id}';"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return False
        else:
            self.conn.commit()
            return True 



