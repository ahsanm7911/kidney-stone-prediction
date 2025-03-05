from django.db.models.signals import post_delete
from django.dispatch import receiver
from doctors.models import Doctor
from patients.models import Patient

@receiver(post_delete, sender=Doctor)
@receiver(post_delete, sender=Patient)
def delete_user_with_profile(sender, instance, **kwargs):
    """ 
    Deletes the associated user when a Doctor or Patient profile is deleted.
    """
    if instance.user:
        instance.user.delete()