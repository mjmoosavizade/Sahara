from django.db import models
from django.utils.text import slugify 

class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True, verbose_name='والد')
    category_title = models.CharField(max_length=255, verbose_name='نام دسته بندی')
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_title