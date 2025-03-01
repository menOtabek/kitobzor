from rest_framework import serializers
from .models import Banner, Region, District, FAQ, PrivacyPolicy


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name', 'region')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'picture')


class FAQQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'question')



class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer')


class PrivacyPolicyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ('id', 'title')


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ('id', 'title', 'description')
