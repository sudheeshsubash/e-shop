# Generated by Django 4.1.7 on 2023-02-20 05:55

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app1', '0004_alter_customuser_phone_number'),
        ('eshopadmin_app1', '0002_alter_shopdetails_address_alter_shopdetails_place'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopStaff',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eshopadmin_app1.shopdetails')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('admin_app1.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
