from rest_framework import serializers
from .models import Region, District, Banner, FAQ, PrivacyPolicy, ContactUs


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ['id', 'name']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'picture']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['id', 'title', 'description']


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('phone', 'message')

    def create(self, validated_data):
        user = self.context['request'].user
        return ContactUs.objects.create(user=user, **validated_data)
