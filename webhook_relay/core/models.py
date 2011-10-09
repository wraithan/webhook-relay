from django.db import models
from imp import load_source


class Hook(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    owner = models.ForeignKey('profiles.UserProfile', related_name='hooks')
    processors = models.ManyToManyField('core.Processor', through='core.HookProcessorAssoc')
    emitters = models.ManyToManyField('core.Emitter', through='core.HookEmitterAssoc')
    active = models.BooleanField()

    class Meta:
        unique_together = ("slug", "owner")

    def next_action(self, data, just_completed=None):
        for processor in self.hookprocessorassoc_set.filter(relies_on=just_completed):
            processor.process(data)
        for emitter in self.hookemitterassoc_set.filter(relies_on=just_completed):
            emitter.emit(data)


class Data(models.Model):
    post_body = models.TextField()
    hook = models.ForeignKey('core.Hook')
    received_at = models.DateTimeField(auto_now_add=True)


class HasFields(models.Model):
    class Meta:
        abstract = True

    def field(self, field_name):
        try:
            return self.fields.get(name=field_name).value
        except models.DoesNotExist:
            return None

    def fields_list(self):
        return self.fields.all().values_list(flat=True)


class Processor(HasFields, models.Model):
    name = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    fields = models.ManyToManyField('core.BaseField')


class Emitter(HasFields, models.Model):
    name = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    fields = models.ManyToManyField('core.BaseField')


class BaseField(models.Model):
    name = models.CharField(max_length=100)


class HookProcessorAssoc(HasFields, models.Model):
    hook = models.ForeignKey('core.Hook')
    processor = models.ForeignKey('core.Processor')
    relies_on = models.ForeignKey('self', null=True)
    fields = models.ManyToManyField('core.HookField')

    def process(self, data, step):
        load_source(self.processor.task_name,
                    'tasks/processors/' + self.processor.task_name + '.py'
                    ).process(self.id, data.id, step)


class HookEmitterAssoc(HasFields, models.Model):
    hook = models.ForeignKey('core.Hook')
    emitter = models.ForeignKey('core.Emitter')
    relies_on = models.ForeignKey('core.HookProcessorAssoc', null=True)
    fields = models.ManyToManyField('core.HookField')

    def emit(self, data):
        load_source(self.emitter.task_name,
                    'tasks/emitters/' + self.emitter.task_name + '.py'
                    ).emit.delay(self.id, data.id)


class HookField(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField()
