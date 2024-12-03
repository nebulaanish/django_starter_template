import uuid

from django.db import models

from django.utils import timezone


class ActiveDataManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """Abstract base model that includes common fields for all models.

    Attributes
        idx (UUIDField): Primary key for the model, automatically generated UUID.
        created_at (DateTimeField): Timestamp of when the object was created, set automatically.
        updated_at (DateTimeField): Timestamp of the last update, set automatically.
        deleted_at (DateTimeField): Timestamp of when the object was marked as deleted, can be null or blank.
        is_deleted (BooleanField): Flag indicating whether the object is marked as deleted, default is False.

    Meta
        abstract (bool): Indicates that this model is abstract and should not be created as a database table.

    """

    idx = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ActiveDataManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Override the delete method to mark the object as deleted instead of deleting it from the database.
        This allows for soft deletion of objects, where they are not actually removed from the database but marked
        as deleted.
        """
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()
        return "Data has been successfully deleted."
