# Generated by Django 4.2.5 on 2023-11-21 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'EventStatus',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('attendees', models.IntegerField(default=0)),
                ('event_date', models.DateTimeField()),
                ('notes', models.TextField(blank=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.client')),
                ('event_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='events.eventstatus')),
                ('support_contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='events_handled_by_this_support_contact', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
