# Generated by Django 3.1.7 on 2021-05-14 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('auth_', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='customer_order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='order_products', to='api.Gadget'),
        ),
        migrations.AddField(
            model_name='gadget',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_products', to='api.category'),
        ),
        migrations.AddField(
            model_name='gadget',
            name='seller',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sel_products', to='auth_.seller'),
        ),
        migrations.AddField(
            model_name='comment',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.gadget'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.deliveryaddress'),
        ),
    ]
