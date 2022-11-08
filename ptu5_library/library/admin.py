from django.contrib import admin
from . import models

class BookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra: 0

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = (BookInstanceInline, )

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    readonly_fields = ('unique_id', )
    can_delete = False

    fieldsets = (
        ('General', {'fields': ('unique_id', 'book')}),
        ('Availability', {'fields': (('status', 'due_back'),)}),
    )


class AuthorAdmin(admin.ModelAdmin):
    # padarome galimybę rūšiuoti pagal pavardžių ir vardų laukus iš admino
    list_display=('first_name', 'last_name')
    list_display_links=('last_name', )


# Register your models here.
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookInstance, BookInstanceAdmin)
