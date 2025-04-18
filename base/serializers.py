from rest_framework import serializers
from .models import Banner, Region, District, FAQ, PrivacyPolicy
import html2text

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = District
        fields = ('id', 'name', 'region')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'picture')


class FAQSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer')

    def get_answer(self, obj):
        if obj.answer:
            return html2text.html2text(obj.answer)
        return ""


class PrivacyPolicySerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    class Meta:
        model = PrivacyPolicy
        fields = ('id', 'title', 'description')

    def get_description(self, obj):
        if obj.description:
            return html2text.html2text(obj.description)
        return ""
