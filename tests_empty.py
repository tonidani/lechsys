from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):
    wait_time = between(0.5, 3.0)
    
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task(1)
    def login_get(self):
        self.client.get("http://localhost:5000/login")

    @task(2)
    def login_post(self):       
        self.client.post("/login",
                            {username:"admin",
                            password:"lol"})

    @task(3)
    def home_get(self):
        self.client.get("http://localhost:5000/home")

    @task(4)
    def users_get(self):
        self.client.get("http://localhost:5000/users")   

    @task(5)
    def users_add__get(self):
        self.client.get("http://localhost:5000/users/add")   


    @task(6)
    def teams_get(self):
        self.client.get("http://localhost:5000/teams/add")  


    @task(7)
    def users_import_get(self):
        self.client.get("http://localhost:5000/users/import")  


    @task(8)
    def users_motoric(self):
        self.client.get("http://localhost:5000/users/1/motoric")  


    @task(9)
    def users_medical(self):
        self.client.get("http://localhost:5000/users/1/medical")  


    @task(10)
    def users_surveys(self):
        self.client.get("http://localhost:5000/users/1/surveys")  


    @task(11)
    def users_resume(self):
        self.client.get("http://localhost:5000/users/1/resume")  


    @task(12)
    def calendar(self):
        self.client.get("http://localhost:5000/calendar")  


    @task(13)
    def surveys(self):
        self.client.get("http://localhost:5000/surveys")  


    @task(14)
    def settings(self):
        self.client.get("http://localhost:5000/settings")  

    @task(14)
    def support(self):
        self.client.get("http://localhost:5000/support")  