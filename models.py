from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from contact_manager.models import Contact, ContactRole

READ = 'r'
WRITE = 'w'
BOTH = 'rw'
ACCESS_DIRECTION = (
    (READ, 'Read'),
    (WRITE, 'Write'),
    (BOTH, 'Read/Write'),
)

DEV = 'd'
LIVE = 'l'
DEPRICATED = 'X'
STATE = (
    (DEV, 'In development'),
    (LIVE, 'Live'),
    (DEPRICATED, 'Deprecated'),
)

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True, )
    image = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE, default=LIVE, blank=False)

    class Meta:
        ordering = ['name']
        permissions = (
            ("is_owner", "Is Owner"),
        )

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(PaymentMethod, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.name)

class ModuleWritesToModule(models.Model):
    from_module = models.ForeignKey('Module', related_name='module_from_relation')
    to_module = models.ForeignKey('Module', related_name='module_to_relation')
    access_direction = models.CharField(choices=ACCESS_DIRECTION, default=BOTH, max_length=2)
    payment_methods = models.ManyToManyField('PaymentMethod', blank=True, default=None)
    state = models.CharField(max_length=1, choices=STATE, default=LIVE, blank=False)
    comment = models.CharField(max_length=150, default=None, null=True, blank=True)
    is_online = models.NullBooleanField(default=None, null=True, blank=True)

    class Meta:
        unique_together = ('from_module', 'to_module', 'access_direction', 'is_online')

    def __unicode__(self):
        return str("%s %s %s" % (self.from_module, self.access_direction, self.to_module))


class Module(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    documentation = models.URLField(blank=True, null=True)
    tickets = models.URLField(blank=True, null=True)
    customer_facing = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=STATE, default=LIVE, blank=False)
    connected_to_module = models.ManyToManyField('self', through='ModuleWritesToModule', through_fields=('from_module', 'to_module'), related_name='module_write_module', symmetrical=False, default=None, blank=True)
    css_class = models.CharField(max_length=50, blank=True, null=True)
    is_service = models.BooleanField(default=False, blank=False, null=False)
    is_external = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        ordering = ['name']
        permissions = (
            ("is_owner", "Is Owner"),
        )

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(Module, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.name)


class ModuleContact(models.Model):
    parent = models.ForeignKey(Module)
    contact = models.ForeignKey(Contact)
    role = models.ForeignKey(ContactRole)

    class Meta:
        unique_together = ('parent', 'contact', 'role', )

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return str(self.name)