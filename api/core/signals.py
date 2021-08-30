from django.contrib import auth
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=auth.get_user_model())
def set_username(sender, instance, **_kwargs):
    instance.username = instance.username or instance.email
