from rest_framework.metadata import SimpleMetadata

from collections import OrderedDict

from django.utils.encoding import force_text

from rest_framework import serializers


class ChoicesMetadata(SimpleMetadata):

    def determine_metadata(self, request, view):
        metadata = super(ChoicesMetadata, self).determine_metadata(request, view)

        field_info = OrderedDict()

        for field_name, field in view.get_serializer().fields.items():
            choices = OrderedDict()
            if (not isinstance(field, (serializers.RelatedField, serializers.ManyRelatedField))
                and hasattr(field, 'choices')):
                choices['choices'] = [
                    {
                        'value': choice_value,
                        'display_name': force_text(choice_name, strings_only=True)
                    }
                    for choice_value, choice_name in field.choices.items()
                ]
                field_info[field_name] = choices
        
        metadata['selections'] = field_info
        return metadata