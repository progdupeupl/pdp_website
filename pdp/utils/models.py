# coding: utf-8

"""Module containing functions to be used on models."""


def has_changed(instance, field, manager='objects'):
    """Check if a field has changed in a model.

    May be used in a model.save() method.

    Returns:
        True if the field is not the same as in the database, False elsewise.

    """
    # If the model does not exist, we can say it has changed
    if not instance.pk:
        return True

    # We retreive the manager of the model for the given instance
    manager = getattr(instance.__class__, manager)

    # We get the field of our database object using the manager
    old = getattr(manager.get(pk=instance.pk), field)

    # We compare instance's field and database-retrieved object's field
    return not getattr(instance, field) == old
