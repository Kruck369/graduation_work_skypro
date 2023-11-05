from rest_framework import serializers
from ads.models import Ad, Comment


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(source='author.first_name')
    author_last_name = serializers.CharField(source='author.last_name')
    author_image = serializers.ImageField(source='author.image')

    class Meta:
        model = Comment
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id')

    class Meta:
        model = Ad
        fields = ['pk', 'title', 'price', 'description', 'image']


class AdDetailSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id', read_only=True)
    phone = serializers.CharField(source='author.phone')
    author_id = serializers.IntegerField(source='author.id')
    author_first_name = serializers.CharField(source='author.first_name')
    author_last_name = serializers.CharField(source='author.last_name')

    class Meta:
        model = Ad
        fields = [
            'pk',
            'title',
            'price',
            'description',
            'image',
            'phone',
            'author_first_name',
            'author_last_name',
            'author_id',
        ]
