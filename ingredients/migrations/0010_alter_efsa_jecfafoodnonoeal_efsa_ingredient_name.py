# Generated by Django 5.0.1 on 2025-04-14 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0009_alter_toxricld50_is_toxicity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="efsa_jecfafoodnonoeal",
            name="efsa_ingredient_name",
            field=models.TextField(
                blank=True, null=True, verbose_name="EFSA Ingredient Name"
            ),
        ),
    ]
