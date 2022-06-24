import datetime
import json
from uuid import UUID

import dateutil.parser
from rest_framework import generics, mixins, response
from rest_framework.views import APIView

from core.responses import (error_invalid_schema_of_document_or_data,
                            error_item_not_found, success_delete,
                            success_import)
from core.scripts import change_parents_date
from restapi.models import OfferAndCategory
from restapi.serializers import OfferAndCategorySerializer


class OfferAndCategoryView(APIView):
    serializer_class = OfferAndCategorySerializer

    def get(self, request, *args, **kwargs):
        try:
            UUID(kwargs['uuid'])
        except ValueError:
            return error_invalid_schema_of_document_or_data()

        queryset = OfferAndCategory.objects.filter(uuid=kwargs['uuid'])
        if not queryset:
            return error_item_not_found()

        serializer_for_queryset = OfferAndCategoryView.serializer_class(
            instance=queryset[0],
            many=False
        )

        return response.Response(serializer_for_queryset.data)


class LatestOfferAndCategoryView(generics.ListAPIView):
    queryset = OfferAndCategory.objects.filter(
        type=OfferAndCategory.ElementTypes.OFFER,
    )
    serializer_class = OfferAndCategorySerializer

    def get(self, request, *args, **kwargs):
        if 'date' not in request.GET:
            return error_invalid_schema_of_document_or_data()

        date = datetime.datetime. \
            strptime(request.GET['date'], '%Y-%m-%dT%H:%M:%S.%fZ')

        queryset = self.get_queryset()
        queryset.filter(
            date__lte=date,
            date__gte=date - datetime.timedelta(hours=10)
        )

        serializer_for_queryset = OfferAndCategoryView.serializer_class(
            instance=queryset,
            many=True
        )

        return response.Response(serializer_for_queryset.data)


class OfferAndCategoryImports(generics.ListCreateAPIView):
    queryset = OfferAndCategory.objects.all()
    serializer_class = OfferAndCategorySerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)

        try:
            date = dateutil.parser.isoparse(data['updateDate'])
        except Exception as e:
            print(e)
            return error_invalid_schema_of_document_or_data()

        for item in data['items']:
            try:
                offer_and_category = OfferAndCategory.objects.filter(uuid=item['id'])
                if offer_and_category:
                    offer_and_category = offer_and_category[0]
                else:
                    offer_and_category = OfferAndCategory(uuid=item['id'])

                offer_and_category.type = item['type']
                offer_and_category.name = item['name']
                offer_and_category.parent_id = item['parentId']
                offer_and_category.date = date

                if item['parentId']:
                    change_parents_date(item['parentId'], date)

                if OfferAndCategory.ElementTypes.OFFER == item['type']:
                    if item['price'] < 0:
                        return error_invalid_schema_of_document_or_data()
                    offer_and_category.price = item['price']
                elif 'price' in item:
                    return error_invalid_schema_of_document_or_data()

                offer_and_category.save()
            except Exception as e:
                print(e)
                return error_invalid_schema_of_document_or_data()

        return success_import()


class OfferAndCategoryDelete(mixins.DestroyModelMixin,
                             generics.GenericAPIView):
    queryset = OfferAndCategory.objects.all()
    serializer_class = OfferAndCategorySerializer
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        try:
            UUID(kwargs['uuid'])
        except ValueError:
            return error_invalid_schema_of_document_or_data()

        item = OfferAndCategory.objects.filter(uuid=kwargs['uuid'])
        if not item:
            return error_item_not_found()

        item = item[0]
        item.delete()

        return success_delete()
