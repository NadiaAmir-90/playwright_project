from django.db import models


class Test01Model(models.Model):

    id = models.BigAutoField(primary_key=True)

    test_cases= models.CharField(max_length=100,default="")
    url= models.URLField(max_length=255,default="https://www.airbnb.com/")
    passed= models.CharField(max_length=50,default=False)
    comment= models.CharField(max_length=200,default="",blank=True)


    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Test AIRBNB website!"









