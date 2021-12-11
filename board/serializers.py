from rest_framework import serializers
from .models import Posts

# https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
class PostsSerializer(serializers.Serializer) :
    id = serializers.IntegerField(read_only = True)
    author = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    def create(self, validated_data):
        return Posts.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
# class PostsSerializer(serializers.ModelSerializer) :
#     class Meta:
#         model = Posts
#         fields = "__all__"
