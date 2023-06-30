# Generated by Django 4.2.1 on 2023-06-30 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='image_path',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_products', to=settings.AUTH_USER_MODEL, verbose_name='Создано пользователем'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='Продукт'),
        ),
    ]
