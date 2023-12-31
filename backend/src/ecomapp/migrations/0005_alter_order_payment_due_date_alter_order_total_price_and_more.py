# Generated by Django 4.2.6 on 2023-10-31 09:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ecomapp", "0004_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="payment_due_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Payment Due Date"),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True, verbose_name="Total Price"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="orderproduct",
            unique_together={("order", "product")},
        ),
    ]
