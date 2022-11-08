from django.db import models
import uuid

# uuid - random generuojamas ID, kad susigeneruoti unukalų indentifikatorių
# Create your models here.


class Genre(models.Model):
    name = models.CharField('name', max_length=200, help_text = "Enter name of the book genre")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField('first_name', max_length = 50)
    last_name = models.CharField('last_name', max_length = 50)

    def __str__(self) -> str:
        return f"{self.first_name}, {self.last_name}"

    def display_books(self):
        return ', '.join(book.title for book in self.books.all())
    display_books.short_description = 'books'


    class Meta:
        # nurodome, kaip bus rūšiuojamas sąrašas. Dažniausiai naudojamas tuple, nes veikia 
        # greičiau, nei sąrašai. bet naudojammi ir sąrašai
        ordering = ['last_name', 'first_name']


class Book(models.Model):
    title = models.CharField('title', max_length=255)
    summary = models.TextField('summary') # Text field yra neribojamas ir jo galima nerašyti
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True,
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols')
    author = models.ForeignKey(
        Author,on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='books',
    )
    genre = models.ManyToManyField(Genre, help_text = "Choose genre(s) for this book", verbose_name='genre(s)')

    def __str__(self) -> str:
        return f'{self.author} - {self.title}'

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'genre'


class BookInstance(models.Model):
    unique_id = models.UUIDField('unique ID', default = uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, verbose_name='book', on_delete = models.CASCADE)
    due_back = models.DateField('due back', null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'manage'),
        ('t', 'taken'),
        ('a', 'available'),
        ('r', 'reserved'),
    )

    status = models.CharField('status', max_length=1, choices=LOAN_STATUS, default='m')
    # price = models.DecimalField("price", max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.unique_id}: {self.book.title}'
    
    class Meta():
        ordering = ['due_back']