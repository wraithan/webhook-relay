from django.db import models


class Hook(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    owner = models.ForeignKey('profiles.UserProfile', related_name='hooks')
    processors = models.ManyToManyField('core.Processor', through='core.HookProcessorAssoc')
    emitters = models.ManyToManyField('core.Emitter', through='core.HookEmitterAssoc')
    active = models.BooleanField()

    class Meta:
        unique_together = ("slug", "owner")

    def next_action(self, data, step):
        for processor in self.processors.filter(relies_on_step=0):
            processor.process(data, step=1)
        for emitter in self.emitters.filter(relies_on_step=0):
            emitter.emit(data)


class Data(models.Model):
    post_body = models.TextField()
    hook = models.ForeignKey('core.Hook')
    received_at = models.DateTimeField(auto_now_add=True)


class Processor(models.Model):
    name = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)

    def process(self, data, step):
        __import__('tasks.processors.' + self.task_name).process(self.id, data.id, step)


class Emitter(models.Model):
    name = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    fields = models.ManyToManyField('core.EmitterField')

    def emit(self, data, step):
        __import__('tasks.emitters.' + self.task_name).emit.delay(self.id, data.id, step)


class EmitterField(models.Model):
    name = models.CharField(max_length=100)


class HookProcessorAssoc(models.Model):
    hook = models.ForeignKey('core.Hook')
    processor = models.ForeignKey('core.Processor')
    step = models.PositiveIntegerField()
    relies_on_step = models.PositiveIntegerField()
    fields = models.ManyToManyField('core.HookField')


class HookEmitterAssoc(models.Model):
    hook = models.ForeignKey('core.Hook')
    emitter = models.ForeignKey('core.Emitter')
    relies_on_step = models.PositiveIntegerField()
    fields = models.ManyToManyField('core.HookField')

    def field(self, field_name):
        try:
            return self.fields.get(name=field_name).value
        except models.DoesNotExist:
            return None

class HookField(models.Models):
    name = models.CharField(max_length=100)
    value = models.TextField()
