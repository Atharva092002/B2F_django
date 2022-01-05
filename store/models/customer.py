from django.db import models

class Customer(models.Model):
    name=models.CharField(max_length=20)
    uname=models.CharField(max_length=20)
    email=models.EmailField()
    pwd=models.CharField(max_length=200)

    def register(self):
        self.save()
    
    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        else:
            return False
    
    @staticmethod
    def get_customer_by_username(username):
        return Customer.objects.get(uname=username)

