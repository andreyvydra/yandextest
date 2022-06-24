from rest_framework import serializers

from core.scripts import get_average_price
from restapi.models import OfferAndCategory


class OfferAndCategoryListingField(serializers.RelatedField):
    def to_representation(self, value):
        data = {
            'type': value.type,
            'name': value.name,
            'id': value.uuid,
            'price': value.price,
            'parentId': value.parent_id,
            'date': value.date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
        }
        if value.type == OfferAndCategory.ElementTypes.OFFER:
            data['children'] = None
        else:
            many_children = value.children.all()
            data['price'] = get_average_price(value)
            data['children'] = [self.to_representation(children) for children in many_children]
        return data


class OfferAndCategorySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_uuid')
    parentId = serializers.SerializerMethodField('get_parent_id')
    price = serializers.SerializerMethodField('get_price')
    date = serializers.SerializerMethodField('get_date')
    children = OfferAndCategoryListingField(many=True, read_only=True)

    def get_uuid(self, obj):
        return obj.uuid

    def get_parent_id(self, obj):
        return obj.parent_id

    def get_price(self, obj):
        if obj.type != OfferAndCategory.ElementTypes.OFFER:
            return get_average_price(obj)
        return obj.price

    def get_date(self, obj):
        return obj.date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'

    class Meta:
        model = OfferAndCategory
        fields = (
            'type',
            'name',
            'id',
            'price',
            'parentId',
            'date',
            'children'
        )
