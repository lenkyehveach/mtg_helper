# Generated by Django 3.2.12 on 2022-03-28 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Neo',
            fields=[
                ('name', models.CharField(blank=True, max_length=54, null=True)),
                ('colors', models.CharField(blank=True, max_length=50, null=True)),
                ('coloridentity', models.CharField(blank=True, db_column='colorIdentity', max_length=50, null=True)),
                ('manacost', models.CharField(blank=True, db_column='manaCost', max_length=50, null=True)),
                ('manavalue', models.PositiveIntegerField(blank=True, db_column='manaValue', null=True)),
                ('originaltype', models.CharField(blank=True, db_column='originalType', max_length=50, null=True)),
                ('types', models.CharField(blank=True, max_length=50, null=True)),
                ('subtypes', models.CharField(blank=True, max_length=50, null=True)),
                ('supertypes', models.CharField(blank=True, max_length=50, null=True)),
                ('originaltext', models.TextField(blank=True, db_column='originalText', null=True)),
                ('keywords', models.CharField(blank=True, max_length=50, null=True)),
                ('power', models.PositiveIntegerField(blank=True, null=True)),
                ('toughness', models.PositiveIntegerField(blank=True, null=True)),
                ('rarity', models.CharField(blank=True, max_length=10, null=True)),
                ('setcode', models.CharField(blank=True, db_column='setCode', max_length=3, null=True)),
                ('image_ref', models.CharField(blank=True, max_length=50, null=True)),
                ('cardid', models.AutoField(db_column='cardID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'neo',
                'managed': False,
            },
        ),
    ]
