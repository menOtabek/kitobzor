from __future__ import annotations
import functools
import operator
from typing import List, Type

from django.db.models import Q
from django.db.models.enums import Choices
from django.utils.translation import gettext as _
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .choices import PolicyType, BookType, OwnerType, CoverType
from .translit import latin_to_cyrillic, cyrillic_to_latin


def generate_openapi_choice_query_param(
        name: str, choices: Type[Choices]
) -> list[OpenApiParameter]:
    return [
        OpenApiParameter(
            name=name,
            description='Filter by Type. Available options: ' + (
                ', '.join([
                    f"{choice.value} - {choice.label}"
                    for choice in choices
                ])
            ),
            required=False,
            type=OpenApiTypes.STR
        )
    ]


NOT_ACCEPTED_VALUES = ['', 'null', 'undefined']


class BaseCustomFilter(BaseFilterBackend):
    FIELDS = []
    RANGE_FIELDS = []
    DATE_FIELDS = []
    SEARCH_FIELDS = []
    ORDERING_FIELDS = []
    search_param = 'q'

    def filter_queryset(self, request, queryset, view):
        filters = {}

        filters.update(self._apply_exact_filters(request))
        filters.update(self._apply_range_filters(request))
        filters.update(self._apply_date_filters(request))

        if filters:
            queryset = queryset.filter(**filters)

        queryset = self._apply_exclude_filter(request, queryset)
        queryset = self._apply_search_filter(request, queryset)

        return queryset

    def _apply_exact_filters(self, request):
        filters = {}
        for field in self.FIELDS:
            param_value = request.query_params.get(field['name'], None)
            if param_value in NOT_ACCEPTED_VALUES:
                raise ValidationError(
                    _("Invalid filter value: %(value)s") % {"value": param_value}
                )
            if param_value is not None:
                try:
                    if field['type'] == bool:
                        param_value = param_value.lower() == 'true'
                    elif field['type'] == int and field['name'] == 'status':
                        filters['status__in'] = param_value.split(',')
                        continue
                    elif field['type'] == int:
                        param_value = int(param_value)
                    elif field['type'] == float:
                        param_value = float(param_value)
                    elif field['type'] == str:
                        param_value = str(param_value)
                    else:
                        raise ValidationError(
                            _("Invalid type for field: %(field_name)s") % {"field_name": field['name']}
                        )
                except ValueError:
                    raise ValidationError(
                        _("Invalid format for field %(field_name)s. Expected %(expected_type)s.") % {
                            "field_name": field['name'],
                            "expected_type": field['type']
                        }
                    )
                filters[f'{field["name"]}__exact'] = param_value
        return filters

    def _apply_range_filters(self, request):
        filters = {}
        for field in self.RANGE_FIELDS:
            min_value = self.validate_query_param(request, f"{field['name']}_min", expected_type=float)
            max_value = self.validate_query_param(request, f"{field['name']}_max", expected_type=float)

            if min_value is not None:
                filters[f"{field['name']}__gte"] = min_value
            if max_value is not None:
                filters[f"{field['name']}__lte"] = max_value
        return filters

    def _apply_date_filters(self, request):
        filters = {}
        for field in self.DATE_FIELDS:
            type = field.get('type')
            start_date = self.validate_query_param(request, f"{field['name']}_from", expected_type='date')
            end_date = self.validate_query_param(request, f"{field['name']}_to", expected_type='date')

            if start_date:
                if type:
                    filters[f"{field['name']}__gte"] = start_date
                else:
                    filters[f"{field['name']}__date__gte"] = start_date
            if end_date:
                if type:
                    filters[f"{field['name']}__lte"] = end_date
                else:
                    filters[f"{field['name']}__date__lte"] = end_date
        return filters

    def _apply_exclude_filter(self, request, queryset):
        exclude = request.query_params.get('exclude', None)
        if exclude:
            try:
                exclude = list(map(int, exclude.split(',')))
                queryset = queryset.exclude(id__in=exclude)
            except ValueError:

                raise ValidationError(
                    _("Invalid exclude parameter format. Must be comma-separated integer IDs.")
                )
        return queryset

    def _apply_search_filter(self, request, queryset):
        query = request.query_params.get(self.search_param)
        if not (query and self.SEARCH_FIELDS):
            return queryset

        tokens = self._tokenise(query)
        q_obj = functools.reduce(
            operator.or_,
            (self._token_lookup(tok) for tok in tokens)
        )
        return queryset.filter(q_obj)

    def _tokenise(self, text: str) -> List[str]:
        return [t for t in text.lower().split() if t]

    @functools.lru_cache(maxsize=1024)
    def _translit_variants(self, token: str) -> tuple[str, str, str]:
        return token, latin_to_cyrillic(token), cyrillic_to_latin(token)

    def _token_lookup(self, token: str) -> Q:
        variants = self._translit_variants(token)
        return functools.reduce(
            operator.or_,
            (
                Q(**{f"{field}__icontains": v})
                for field in self.SEARCH_FIELDS
                for v in variants
            ),
        )

    def validate_query_param(self, request, param_name, expected_type):
        value = request.query_params.get(param_name, None)

        if not value or value in NOT_ACCEPTED_VALUES:
            return None

        try:
            if expected_type == int:
                return int(value)
            elif expected_type == float:
                return float(value)
            elif expected_type == 'date':
                from datetime import datetime
                return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError(
                _("Invalid format for %(param)s. Expected %(type)s.") % {
                    "param": param_name,
                    "type": expected_type
                }
            )
        return None

    @classmethod
    def generate_query_parameters(cls):
        parameters = []

        # Exact filters
        for field in cls.FIELDS:
            parameters.append(OpenApiParameter(
                name=field['name'],
                description=field['description'],
                required=False,
                type=OpenApiTypes.STR if field['type'] == str else OpenApiTypes.INT
            ))

        # Range filters
        for field in cls.RANGE_FIELDS:
            parameters.append(OpenApiParameter(
                name=f"{field['name']}_min",
                description=f"Min {field['description']}",
                required=False,
                type=OpenApiTypes.NUMBER
            ))
            parameters.append(OpenApiParameter(
                name=f"{field['name']}_max",
                description=f"Max {field['description']}",
                required=False,
                type=OpenApiTypes.NUMBER
            ))

        # Date filters
        for field in cls.FIELDS:
            param_type = (
                OpenApiTypes.BOOL if field['type'] is bool
                else OpenApiTypes.STR if field['type'] is str
                else OpenApiTypes.INT
            )
            parameters.append(OpenApiParameter(
                name=field['name'],
                description=field['description'],
                required=False,
                type=param_type
            ))

        parameters.append(OpenApiParameter(name='exclude',
                                           description='Exclude IDs (comma-separated)',
                                           required=False,
                                           type=OpenApiTypes.STR))
        parameters.append(
            OpenApiParameter(name='q', description='Search by keywords',
                             required=False,
                             type=OpenApiTypes.STR))

        parameters.append(OpenApiParameter(
            name='ordering',
            description='Fields available for ordering: ' + ', '.join(
                cls.ORDERING_FIELDS),
            required=False,
            type=OpenApiTypes.STR
        ))
        return parameters


class BaseModelFilter(BaseCustomFilter):
    ORDERING_FIELDS = ['id', 'created_at', 'updated_at']
    FIELDS = [
        {'name': 'id', 'type': int, 'description': 'Filter by ID'},
    ]

    DATE_FIELDS = [
        {'name': 'created_at', 'description': 'Filter by creation date'},
        {'name': 'updated_at', 'description': 'Filter by last updated date'},
    ]


class DistrictFilter(BaseModelFilter):
    FIELDS = BaseModelFilter.FIELDS + [
        {'name': 'region', 'type': int, 'description': 'Filter by region ID'},
    ]

    SEARCH_FIELDS = ['name']


class PrivacyPolicyFilter(BaseModelFilter):
    FIELDS = BaseModelFilter.FIELDS + [
        {'name': 'type', 'type': str, 'description': 'Filter by type'},
    ]

    @classmethod
    def generate_query_parameters(cls):
        parameters = super().generate_query_parameters()
        parameters += generate_openapi_choice_query_param('type', PolicyType)

        return parameters


class SubCategoryFilter(BaseModelFilter):
    FIELDS = BaseModelFilter.FIELDS + [
        {'name': 'category', 'type': int, 'description': 'Filter by category ID'},
    ]

    SEARCH_FIELDS = ['name', 'category__name']


class BookFilter(BaseModelFilter):
    ORDERING_FIELDS = BaseModelFilter.ORDERING_FIELDS + ['price', 'publication_year']
    FIELDS = BaseModelFilter.FIELDS + [
        {'name': 'category', 'type': int, 'description': 'Filter by category ID'},
        {'name': 'sub_category', 'type': int, 'description': 'Filter by sub_category ID'},
        {'name': 'shop', 'type': int, 'description': 'Filter by shop ID'},
        {'name': 'posted_by', 'type': int, 'description': 'Filter by posted user ID'},
        {'name': 'type', 'type': str, 'description': 'Filter by type'},
        {'name': 'owner_type', 'type': str, 'description': 'Filter by owner_type'},
        {'name': 'cover_type', 'type': str, 'description': 'Filter by cover_type'},
        {'name': 'is_active', 'type': bool, 'description': 'Filter by is_active'},
        {'name': 'is_used', 'type': bool, 'description': 'Filter by is_used'},
        {'name': 'for_home_page', 'type': bool, 'description': 'Filter by for_home_page'},
    ]

    RANGE_FIELDS = [
        {'name': 'price', 'type': float, 'description': 'Filter price'},
        {'name': 'publication_year', 'type': int, 'description': 'Filter by publication year'},
    ]

    SEARCH_FIELDS = ['name', 'author', 'category__name', 'sub_category__name',]

    # @staticmethod
    # def generate_query_parameters():
    #     return [
    #         OpenApiParameter(name='my_books', type=OpenApiTypes.BOOL, required=False, description="Filter my books"),
    #         OpenApiParameter(name='tag_id', type=OpenApiTypes.INT, required=False, description="Filter by tag"),
    #         OpenApiParameter(name='latitude', type=OpenApiTypes.FLOAT, required=False, description="Latitude"),
    #         OpenApiParameter(name='longitude', type=OpenApiTypes.FLOAT, required=False, description="Longitude"),
    #     ]

    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)

        if request.query_params.get('my_books') is True:
            queryset = queryset.filter(user=request.user)

        tag_id = request.query_params.get('tag_id')
        if tag_id:
            try:
                tag_id = int(tag_id)
                queryset = queryset.filter(tag__id=tag_id)
            except ValueError:
                raise ValidationError(_("Invalid tag_id. Must be integer."))
        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        owner_type = request.query_params.get('owner_type')
        if owner_type == OwnerType.SHOP and lat and lon:
            try:
                user_location = Point(float(lon), float(lat), srid=4326)
                queryset = queryset.filter(shop__point__isnull=False)
                queryset = queryset.annotate(distance=Distance('shop__point', user_location))
                queryset = queryset.order_by('distance')
            except (ValueError, TypeError):
                raise ValidationError(_("Invalid latitude or longitude"))
        if owner_type == OwnerType.USER and lat and lon:
            try:
                user_location = Point(float(lon), float(lat), srid=4326)
                queryset = queryset.filter(user__point__isnull=False)
                queryset = queryset.annotate(distance=Distance('user__point', user_location))
                queryset = queryset.order_by('distance')
            except (ValueError, TypeError):
                raise ValidationError(_("Invalid latitude or longitude"))

        return queryset

    @classmethod
    def generate_query_parameters(cls):
        parameters = super().generate_query_parameters()
        parameters += generate_openapi_choice_query_param('type', BookType)
        parameters += generate_openapi_choice_query_param('owner_type', OwnerType)
        parameters += generate_openapi_choice_query_param('cover_type', CoverType)

        return parameters


class ShopFilter(BaseModelFilter):
    ORDERING_FIELDS = BaseModelFilter.ORDERING_FIELDS + ['star']
    FIELDS = BaseModelFilter.FIELDS + [
        {'name': 'owner', 'type': int, 'description': 'Filter by owner ID'},
        {'name': 'region', 'type': int, 'description': 'Filter by region ID'},
        {'name': 'district', 'type': int, 'description': 'Filter by district ID'},
        {'name': 'is_active', 'type': bool, 'description': 'Filter by is_active'},
    ]

    RANGE_FIELDS = [
        {'name': 'star', 'type': float, 'description': 'Filter star range'},
    ]

    SEARCH_FIELDS = ['name', 'phone_number']

    # @staticmethod
    # def generate_query_parameters():
    #     return [
    #         OpenApiParameter(name='latitude', type=OpenApiTypes.FLOAT, required=False, description="Latitude"),
    #         OpenApiParameter(name='longitude', type=OpenApiTypes.FLOAT, required=False, description="Longitude"),
    #     ]

    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)


        lat = request.query_params.get('latitude')
        lon = request.query_params.get('longitude')
        if lat and lon:
            try:
                user_location = Point(float(lon), float(lat), srid=4326)
                queryset = queryset.filter(point__isnull=False)
                queryset = queryset.annotate(distance=Distance('point', user_location))
                queryset = queryset.order_by('distance')
            except (ValueError, TypeError):
                raise ValidationError(_("Invalid latitude or longitude"))

        return queryset


class BookCommentFilter(BaseModelFilter):
    FIELDS = BaseModelFilter.FIELDS + [
        {'name': 'book', 'type': int, 'description': 'Filter by book ID'},
        {'name': 'user', 'type': int, 'description': 'Filter by user ID'},
        {'name': 'parent', 'type': int, 'description': 'Filter by parent ID'},
    ]


"""
class TaxiOrderFilter(BaseModelFilter):
    ORDERING_FIELDS = BaseModelFilter.ORDERING_FIELDS + ['agreed_time', 'amount', 'weight', 'per_passenger_amount']

    FIELDS = BaseModelFilter.FIELDS + [
        {'name': 'origin_region', 'type': int, 'description': 'Filter by origin_region ID'},
        {'name': 'destination_region', 'type': int, 'description': 'Filter by destination_region ID'},
        {'name': 'creator', 'type': int, 'description': 'Filter by creator ID'},
        {'name': 'driver', 'type': int, 'description': 'Filter by driver ID'},
        {'name': 'car', 'type': int, 'description': 'Filter by car ID'},
        {'name': 'status', 'type': str, 'description': 'Filter by status'},
        {'name': 'payment_type', 'type': str, 'description': 'Filter by payment_type'},
        {'name': 'type', 'type': str, 'description': 'Filter by type'},
        {'name': 'car_size', 'type': str, 'description': 'Filter by car_size'},
        {'name': 'load_type', 'type': str, 'description': 'Filter by load_type'},
        {'name': 'approach_type', 'type': str, 'description': 'Filter by approach_type'},
        {'name': 'canceled_by_whom', 'type': str, 'description': 'Filter by canceled_by_whom'},
        {'name': 'has_baggage', 'type': bool, 'description': 'Filter by has_baggage'},
        {'name': 'has_air_conditioner', 'type': bool, 'description': 'Filter by has_air_conditioner'},
        {'name': 'tariff', 'type': int, 'description': 'Filter by tariff ID'}
    ]

    RANGE_FIELDS = [
        {'name': 'amount', 'type': float, 'description': 'Filter amount'},
        {'name': 'per_passenger_amount', 'type': float, 'description': 'Filter per passenger amount'},
    ]

    DATE_FIELDS = BaseModelFilter.DATE_FIELDS + [
        {'name': 'agreed_time', 'description': 'Filter by agreed time', 'type': 'date'},
    ]

    # SEARCH_FIELDS = ['id']

    @classmethod
    def generate_query_parameters(cls):
        parameters = super().generate_query_parameters()
        parameters += generate_openapi_choice_query_param('status', OrderStatus)
        parameters += generate_openapi_choice_query_param('payment_type', PaymentType)
        parameters += generate_openapi_choice_query_param('type', OrderType)
        parameters += generate_openapi_choice_query_param('car_size', CarSize)
        parameters += generate_openapi_choice_query_param('load_type', CarLoadType)
        parameters += generate_openapi_choice_query_param('approach_type', ApproachType)
        parameters += generate_openapi_choice_query_param('canceled_by_whom', CancelOrderByWhom)
        # parameters.append(OpenApiParameter(name='short', type=bool,
        #                                    description='If `true`, you will get short product info'))
        # parameters.append(OpenApiParameter(name='total', type=bool,
        #                                    description='If `true`, you will get product with total_quantity in warehouses'))
        # parameters.append(OpenApiParameter(name='isExists', type=bool,
        #                                    description='If `true`, you will get only products which total_quantity > 0'))
        return parameters
        """