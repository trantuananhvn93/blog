# Generated by Django 3.0.5 on 2020-04-26 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_allow_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-published',)},
        ),
        migrations.AlterModelTable(
            name='post',
            table='simple_articles',
        ),
    ]