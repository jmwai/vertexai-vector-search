# Generated by Django 5.1.1 on 2024-09-26 11:09

import pgvector.django.vector
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vectors', '0003_alter_product_image_embedding_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_embedding',
            field=pgvector.django.vector.VectorField(dimensions=384, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='title_embedding',
            field=pgvector.django.vector.VectorField(dimensions=384, null=True),
        ),
    ]