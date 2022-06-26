import tarantool


class TarantoolDB:

    def __init__(self):
        self.connection = tarantool.connect(host="tarantool", port=3301, user="guest")

    def inserts(self, payload):
        return self.connection.call("insert_units", payload)[0]

    def delete(self, id):
        return self.connection.call("delete_unit", id)[0]

    def get_node(self, id):
        return self.connection.call("get_nodes", id)[0]

    def get_sales(self, date, before_date):
        return self.connection.call("get_sales", date, before_date)[0]
