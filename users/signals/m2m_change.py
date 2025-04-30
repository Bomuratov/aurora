# signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from users.models import UserRole

@receiver(m2m_changed, sender=UserRole.code.through)
def update_permissions_on_code_change(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.permissions = [perm.perms for perm in instance.code.all()]
        instance.save(update_fields=["permissions"])
