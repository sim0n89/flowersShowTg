from django.db import models


class Flower(models.Model):
    flower_name = models.CharField(max_length=250)

    def __str__(self):
        return self.flower_name

    class Meta:
        verbose_name = "Цветок"
        verbose_name_plural = "Цветы"


class Product(models.Model):
    name = models.CharField(max_length=250, null=False, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    price = models.FloatField(null=False, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    status = models.BooleanField(default=True, verbose_name="Статус")
    product_to_category = models.ManyToManyField("Category", verbose_name="Категория")
    compound = models.ManyToManyField("Flower", verbose_name="Состав")
    images = models.ManyToManyField("Image", verbose_name="Картинки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Image(models.Model):
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.image

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class Category(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Client(models.Model):
    tlg_id = models.CharField(max_length=50, verbose_name="ID телеграмм")
    name = models.CharField(max_length=250, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Order(models.Model):
    order_create = models.DateTimeField(auto_now_add=True)
    time_to_delievery = models.DateTimeField(null=True)
    address = models.CharField(max_length=250)
    total_price = models.FloatField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    order_status = models.CharField(default="new", max_length=250)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Product_to_order:
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product_price = models.FloatField()
