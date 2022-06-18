import tarantool
from schema import *


class TarantoolUnits:

    def __init__(self):
        self.host = "localhost"
        self.port = 3301
        self.username = "guest"
        self.password = None
        self.space = 'units'

        self.connection: tarantool.Connection = tarantool.connect(self.host, self.port, user=self.username)

    def select(self, id):
        return self.connection.select(self.space, (id,))

    def insert(self, su: ShopUnit):
        try:
            self.connection.insert(self.space, (su.id, su.name, su.date, su.parentId, su.type, su.price, su.children))
            return True
        except tarantool.error.DatabaseError:
            return False

    def delete(self, id):
        try:
            if not self.select(id):
                return False
            self.connection.delete(self.space, id)
            return True
        except tarantool.error.DatabaseError:
            return False

    def call(self, func_name, *args):
        return self.connection.call(func_name, args)


if __name__ == '__main__':

    tu_db = TarantoolUnits()

    print(tu_db.insert(ShopUnit(id="3fa85f64-5717-4562-b3fc-2c963f66a333", name="Оффер 1",
                                date="2022-05-28T21:12:01.000Z",
                                parentId="3fa85f64-5717-4562-b3fc-2c963f66a111", type="OFFER", price=8, children=[])))
    print(tu_db.insert(ShopUnit(id="3fa85f64-5717-4562-b3fc-2c963f66a222", name="Оффер 1",
                                date="2022-05-28T21:12:01.000Z",
                                parentId="3fa85f64-5717-4562-b3fc-2c963f66a111", type="OFFER", price=4, children=[])))
    print(tu_db.insert(ShopUnit(id="3fa85f64-5717-4562-b3fc-2c963f66a444", name="Оффер 1",
                                date="2022-05-28T21:12:01.000Z",
                                parentId="3fa85f64-5717-4562-b3fc-2c963f66a111", type="OFFER", price=12, children=[])))

    print(tu_db.delete("123"))

    print(tu_db.select("3fa85f64-5717-4562-b3fc-2c963f66a444"))
    print(tu_db.call("get_mean_sum", "3fa85f64-5717-4562-b3fc-2c963f66a333"))

