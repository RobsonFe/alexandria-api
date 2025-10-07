from django.db import models
import uuid


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, help_text="Título do livro")
    subtitle = models.CharField(
        max_length=255, null=True, blank=True, help_text="Subtítulo do livro")
    author = models.CharField(max_length=255, help_text="Autor do livro")
    author_description = models.TextField(
        null=True, blank=True, help_text="Descrição do autor do livro")
    description = models.TextField(
        null=True, blank=True, help_text="Descrição do livro")
    category = models.CharField(
        max_length=255, help_text="Categoria do livro")
    pages = models.IntegerField(
        null=True, blank=True, help_text="Número de páginas do livro")
    publisher = models.CharField(
        max_length=255, null=True, blank=True, help_text="Editora do livro")
    year = models.IntegerField(
        null=True, blank=True, help_text="Ano de publicação do livro")
    last_edition = models.IntegerField(
        null=True, blank=True, help_text="Última edição do livro")
    isbn = models.CharField(max_length=255, null=True,
                            blank=True, help_text="ISBN do livro")
    language = models.CharField(
        max_length=100, null=True, blank=True, help_text="Idioma do livro")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text="Preço do livro")
    is_active = models.BooleanField(
        default=True, null=True, blank=True, help_text="Status do livro")
    image_book = models.ImageField(
        upload_to='books/', null=True, blank=True, help_text='Imagem do livro')
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Data de criação do livro")
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Data de atualização do livro")

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
