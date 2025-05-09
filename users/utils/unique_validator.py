from django.db import DataError
from rest_framework.utils.representation import smart_repr
from users.exceptions.validation_error import ValidateErrorException

def qs_exists(queryset):
    try:
        return queryset.exists()
    except (TypeError, ValueError, DataError):
        return False


def qs_filter(queryset, **kwargs):
    try:
        return queryset.filter(**kwargs)
    except (TypeError, ValueError, DataError):
        return queryset.none()


class UniqueValidator:
    message = ('This field must be unique.')
    requires_context = True

    def __init__(self, queryset, message=None, lookup='exact', code=None):
        self.queryset = queryset
        self.message = message or self.message
        self.lookup = lookup
        self.code = code

    def filter_queryset(self, value, queryset, field_name):
        filter_kwargs = {'%s__%s' % (field_name, self.lookup): value}
        return qs_filter(queryset, **filter_kwargs)

    def exclude_current_instance(self, queryset, instance):
        if instance is not None:
            return queryset.exclude(pk=instance.pk)
        return queryset

    def __call__(self, value, serializer_field):
        # Determine the underlying model field name. This may not be the
        # same as the serializer field name if `source=<>` is set.
        field_name = serializer_field.source_attrs[-1]
        # Determine the existing instance, if this is an update operation.
        instance = getattr(serializer_field.parent, 'instance', None)

        queryset = self.queryset
        queryset = self.filter_queryset(value, queryset, field_name)
        queryset = self.exclude_current_instance(queryset, instance)
        if qs_exists(queryset):
            raise ValidateErrorException(detail=self.message, code=self.code)

    def __repr__(self):
        return '<%s(queryset=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.queryset)
        )

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.message == other.message
                and self.requires_context == other.requires_context
                and self.queryset == other.queryset
                and self.lookup == other.lookup
                )
