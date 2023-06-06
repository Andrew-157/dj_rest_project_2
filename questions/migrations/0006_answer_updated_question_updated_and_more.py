# Generated by Django 4.2.2 on 2023-06-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_alter_question_published_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='published',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='published',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
