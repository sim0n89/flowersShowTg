from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=250, null=False, verbose_name="Название")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=250, null=False, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    price = models.FloatField(null=False, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")
    status = models.BooleanField(default=True, verbose_name="Статус")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(
        upload_to="images/", default=None, verbose_name="Изображение"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Client(models.Model):
    tlg_id = models.CharField(max_length=50, verbose_name="ID телеграмм")
    name = models.CharField(max_length=250, verbose_name="Имя")
    phone = models.CharField(max_length=50, verbose_name="Телефон")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Order(models.Model):
    order_create = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, blank=True, null=True
    )
    time_to_delievery = models.DateTimeField(null=True)
    address = models.CharField(max_length=250)
    total_price = models.FloatField()
    client = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, null=True)
    order_status = models.CharField(default="new", max_length=250)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
