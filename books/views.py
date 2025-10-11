from django.shortcuts import get_object_or_404
from rest_framework import generics
from books.models import Book
from books.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CreateBookView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": serializer.data
        }, status=status.HTTP_201_CREATED)


class UpdateBookView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": serializer.data
        }, status=status.HTTP_200_OK)


class DeleteBookView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "result": {"message": "Livro deletado com sucesso"}
        }, status=status.HTTP_200_OK)


class GetBookView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(self.queryset, id=kwargs.get("pk"))
        return Response({
            "result": self.get_serializer(book).data
        }, status=status.HTTP_200_OK)


class GetAllBooksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        books = self.queryset.all()
        return Response({
            "results": self.get_serializer(books, many=True).data
        }, status=status.HTTP_200_OK)
