from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
# импорт кастомного поля для модели
from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    # инструктор курса
    owner = models.ForeignKey(User, related_name="courses_created")
    subject = models.ForeignKey(Subject, related_name="courses")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    students = models.ManyToManyField(User,
                                      related_name="courses_joined",
                                      blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # значение поля будет рассчитано относительно course, это начит что
    # к новому модулю этого же самого курса order будет увеличен на 1
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return "{}. {}".format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module, related_name="contents")
    # значение поля будет рассчитано относительно module, это начит что
    # к новому контенту этого же самого модуля order будет увеличен на 1
    order = OrderField(blank=True, for_fields=['module'])
    # обобщенная связь будет использоватся только для указаных моделей
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('order',)


class BaseContent(models.Model):
    # имя обратной связи обязательно должно быть уникальным
    # в абстрактной модели можно задавать так %(class)s_related
    # где вместо class будет отображатся имя дочерней модели этого класса
    owner = models.ForeignKey(User, related_name="%(class)s_related")
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        # загружается шаблон из указаного пути и возвращается
        # объект Template. Также указывается словарь контекста
        # который будет использован при рендеринге шаблона.
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name),
                                                                {'content_object': self})

    def __str__(self):
        return self.title


class Text(BaseContent):
    content = models.TextField()


class File(BaseContent):
    file = models.FileField(upload_to="files")


class Image(BaseContent):
    file = models.FileField(upload_to="images")


class Video(BaseContent):
    url = models.URLField()
