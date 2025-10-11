from rest_framework import serializers
from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.subtitle = validated_data.get('subtitle', instance.subtitle)
        instance.author = validated_data.get('author', instance.author)
        instance.author_description = validated_data.get(
            'author_description', instance.author_description)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.pages = validated_data.get('pages', instance.pages)
        instance.publisher = validated_data.get(
            'publisher', instance.publisher)
        instance.year = validated_data.get('year', instance.year)
        instance.last_edition = validated_data.get(
            'last_edition', instance.last_edition)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.language = validated_data.get('language', instance.language)
        instance.price = validated_data.get('price', instance.price)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.image_book = validated_data.get(
            'image_book', instance.image_book)
        instance.save()
        return instance
