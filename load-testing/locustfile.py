from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wall_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def imports(self):
        self.client.post("/imports", json={'items': [{'id': '3fa85f64-5717-4562-b3fc-2c963f66a222',
                                                      'name': 'sunt',
                                                      'type': 'CATEGORY',
                                                      'parentId': None,
                                                      'price': None},
                                                     {'id': '3fa85f64-5717-4562-b3fc-2c963f66a333',
                                                      'name': 'ut adipisicing Duis',
                                                      'type': 'OFFER',
                                                      'parentId': '3fa85f64-5717-4562-b3fc-2c963f66a222',
                                                      'price': 26}],
                                           'updateDate': '2022-05-28T21:12:01.000Z'}
                         )

    @task
    def delete(self):
        self.client.delete("/delete/3fa85f64-5717-4562-b3fc-2c963f66a222")

    @task
    def node(self):
        self.client.get("/nodes/3fa85f64-5717-4562-b3fc-2c963f66a222")

    @task
    def sales(self):
        self.client.get("/sales", params={'date': '2022-05-29T12:00:00.000Z'})
