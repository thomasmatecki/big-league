# Generated by Django 3.2.7 on 2021-10-14 01:11
from django.db import migrations
import os
from oauth2_provider.models import AbstractApplication

def init_oauth(apps, _schema_editor):
    application_model = apps.get_model("oauth2_provider", "Application")
    application_model.objects.create(
        name="Next.js App",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uris=os.getenv("REDIRECT_URI"),
        client_type=AbstractApplication.CLIENT_PUBLIC,
        authorization_grant_type=AbstractApplication.GRANT_AUTHORIZATION_CODE,
        skip_authorization=True,
    )

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(init_oauth)
    ]
