# Generated by Django 5.1.1 on 2024-10-02 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='product_image/'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='product_image/'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='product_image/'),
        ),
    ]
