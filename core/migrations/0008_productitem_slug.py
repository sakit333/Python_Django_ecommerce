# Generated by Django 5.1.1 on 2024-10-02 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_productitem_image4_delete_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='productitem',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]