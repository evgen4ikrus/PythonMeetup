from django.db import models


class Flow(models.Model):
    title = models.CharField('Название потока', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Мероприятия"
        verbose_name = "мероприятие"


class Flow_group(models.Model):
    title = models.CharField('Название группы потока', max_length=200)
    start_time = models.TimeField('Время начала',)
    end_time = models.TimeField('Время окончания',)
    presentation_group = models.BooleanField(null=True)
    flow = models.ForeignKey(
        Flow,
        verbose_name='Поток',
        related_name='flow_groups',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Группы блоков по времени"
        verbose_name = "группу блоков по времени"


class Block(models.Model):
    title = models.CharField('Название блока', max_length=200)
    description_addition = models.CharField(max_length=200, blank=True)
    start_time = models.TimeField('Время начала',)
    end_time = models.TimeField('Время окончания',)
    flow_group = models.ForeignKey(
        Flow_group,
        verbose_name='Группа потока',
        related_name='blocks',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.title}: {self.start_time} - {self.end_time}'

    class Meta:
        verbose_name_plural = "Блоки выступлений/перерывы"
        verbose_name = "блок выступлений/перерыв"


class Speaker(models.Model):
    full_name = models.CharField('Полное имя', max_length=150)
    job_title = models.CharField(
        'Где и кем работает',
        max_length=200,
        blank=True
    )
    id_telegram = models.IntegerField('Id telegram')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Спикеры/организаторы"
        verbose_name = "спикера/организатора"


class Presentation(models.Model):
    title = models.CharField('Название выступления', max_length=200)
    speakers = models.ManyToManyField(
        Speaker,
        related_name='presentations',
        verbose_name='Спикер',
        blank=True
    )
    block = models.ForeignKey(
        Block,
        verbose_name='Блок',
        related_name='presentations',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Презантации"
        verbose_name = "презентацию"
