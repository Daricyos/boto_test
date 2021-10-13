from django.db import models


class Users(models.Model):
    tele_id = models.IntegerField("Telegramm id", unique=True, db_column="Telegramm id")
    first_name = models.CharField("First name", null=True, max_length=200, db_column="First name")
    last_name = models.CharField("Last name", null=True, max_length=200, db_column="Last name")
    age = models.IntegerField("Age", null=True,  db_column="Age")
    phone = models.BigIntegerField(default=0, null=True, blank=True, db_column="Phone")

    def __str__(self):
        return f"{self.tele_id}, {self.first_name} {self.last_name}, {self.age}, {self.phone}"


class Product(models.Model):
    name = models.CharField('Product name', max_length=200, db_column='Product name')
    qty = models.IntegerField('Quantity', null=True, db_column='Quantity')
    desc = models.CharField('Desc', max_length=200, db_column='Desc')
    price = models.IntegerField('Price', null=True, db_column='Price')
    img = models.CharField('IMG', max_length=500, db_column='IMG')
    availability = models.IntegerField('Availability', null=True, db_column='Availability')

    def __str__(self):
        return f"{self.id}, {self.name}, {self.qty}, {self.desc}, {self.price}, {self.img}, {self.availability}"
