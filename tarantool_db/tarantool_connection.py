import tarantool


class TarantoolDB:

    def __init__(self):
        self.connection = tarantool.connect(host="localhost", port=3301, user="guest")

    def inserts(self, payload):
        return self.connection.call("insert_units", payload)

    def delete(self, id):
        return self.connection.call("delete_unit", id)

    def get_node(self, id):
        return self.connection.call("get_nodes", id)
