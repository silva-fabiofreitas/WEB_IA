from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MindMap(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField() 

    def __str__(self):
        return self.name


class Iris(models.Model):
    sepal_length = models.FloatField(db_comment='flor azul')
    sepal_width = models.FloatField(db_comment='flor rosa')
    petal_length = models.FloatField()
    petal_width = models.FloatField()
    variety = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.variety}: {self.sepal_length}, {self.sepal_width}, {self.petal_length}, {self.petal_width}"
    


