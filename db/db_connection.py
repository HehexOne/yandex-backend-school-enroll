import tarantool

connection = tarantool.connect("localhost", 3301, user="guest")
units = connection.space('units')

# units.insert(("3fa85f64-5717-4562-b3fc-2c963f66a333", "Оффер 1", "2022-05-28T21:12:01.000Z",
#               "3fa85f64-5717-4562-b3fc-2c963f66a111", "OFFER", 8, []))
# units.insert(("3fa85f64-5717-4562-b3fc-2c963f66a222", "Оффер 1", "2022-05-28T21:13:01.000Z",
#               "3fa85f64-5717-4562-b3fc-2c963f66a111", "OFFER", 4, []))
# units.insert(("3fa85f64-5717-4562-b3fc-2c963f66a444", "Оффер 1", "2022-05-28T21:12:01.000Z",
#               "3fa85f64-5717-4562-b3fc-2c963f66a111", "OFFER", 12, []))


print(connection.call("get_mean_sum", "3fa85f64-5717-4562-b3fc-2c963f66a444"))

# "name": "Оффер 1",
#       "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
#       "price": 4,
#       "date": "2022-05-28T21:12:01.000Z",
#       "type": "OFFER",
#       "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111"
