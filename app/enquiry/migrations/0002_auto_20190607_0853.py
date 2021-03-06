# Generated by Django 2.2.2 on 2019-06-07 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner',
            old_name='type',
            new_name='partner_type',
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(choices=[(1, 'Worst'), (2, 'Poor'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')]),
        ),
    ]
