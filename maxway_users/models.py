from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategorya'
        verbose_name_plural = 'Kategoriyalar'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Order(models.Model):
    payment_type = models.IntegerField()
    status = models.IntegerField(null=False, blank=True, default=0)
    address = models.CharField(max_length=250)
    customer = models.ForeignKey(Users, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        customer_name = f"{self.customer.first_name} {self.customer.last_name}" if self.customer else "Anonymous"
        return f"Buyurtma #{self.id} - {customer_name} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']


class OrderProduct(models.Model):
    count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        product_name = self.product.name if self.product else "Unknown Product"
        return f"{product_name} x{self.count} (₽{self.price})"

    class Meta:
        verbose_name = 'Buyurtma Mahsuloti'
        verbose_name_plural = 'Buyurtma Mahsulotlari'
