from rest_framework import serializers
from .models import CustomUser, Blog, Topic


class DataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']

class ClientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'email', 'confirmPassword']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirmPassword'):
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class AuthorSerializer(DataSerializer):
    email = serializers.CharField(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


class TopicSerializer (serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['id', 'name', 'created', 'updated' ]



class BlogSerializer (serializers.ModelSerializer):
    topic = TopicSerializer()
    author = AuthorSerializer(required= False)
    
    
    class Meta:
        model = Blog
        fields = ['id', 'topic', 'author', 'body', 'created', 'updated']

    def create(self, validated_data):
        topic_data = validated_data.pop('topic')
        topic, created = Topic.objects.get_or_create(**topic_data)
        blog = Blog.objects.create(topic=topic, author=self.context['request'].user, **validated_data)
        return blog

    def update(self, instance, validated_data):
        topic_data = validated_data.pop('topic', None)
        if topic_data:
            topic_name = topic_data.get('name')
            topic, created = Topic.objects.get_or_create(name=topic_name)
            instance.topic = topic

        # Update other fields
        instance.author = validated_data.get('author', instance.author)
        instance.body = validated_data.get('body', instance.body)
        instance.save()

        return instance


