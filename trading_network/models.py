from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=200, verbose_name="Название продукта")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    """Модель звена торговой сети"""

    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название звена")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="Уровень иерархии")

    # Контактные поля прямо в модели NetworkNode
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    products = models.ManyToManyField(
        Product,
        verbose_name="Продукты"
    )
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        related_name='children'
    )
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Задолженность перед поставщиком"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_level_display()}: {self.name}"

    def save(self, *args, **kwargs):
        """Автоматическое определение уровня иерархии на основе поставщика"""
        if not self.pk or 'supplier' in kwargs.get('update_fields', []):
            if self.supplier:
                self.level = self.supplier.level + 1
                if self.level > 2:
                    self.level = 2
            else:
                self.level = 0
        super().save(*args, **kwargs)