from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import NoReverseMatch, reverse
from django.forms.widgets import HiddenInput
from django.utils.safestring import mark_safe


class ModelAdminWithLinks(admin.ModelAdmin):
    link_fields = []

    def __init__(self, *args, **kwargs):
        super(ModelAdminWithLinks, self).__init__(*args, **kwargs)
        self.object = None

    def get_form(self, request, obj=None, **kwargs):
        self.object = obj
        return super(ModelAdminWithLinks, self).get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if self.link_fields and self.object is not None and db_field.name in self.link_fields:
            kwargs['widget'] = ForeignKeyLinkWidget(db_field.remote_field,
                                                    self.admin_site, using=kwargs.get('using'))
        return super(ModelAdminWithLinks, self) \
            .formfield_for_foreignkey(db_field, request, **kwargs)


class TabularInlineWithLinks(admin.TabularInline):
    link_fields = []

    def __init__(self, *args, **kwargs):
        super(TabularInlineWithLinks, self).__init__(*args, **kwargs)
        self.object = None

    def get_formset(self, request, obj=None, **kwargs):
        self.object = obj
        return super(TabularInlineWithLinks, self).get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if self.link_fields and self.object is not None and db_field.name in self.link_fields:
            kwargs['widget'] = ForeignKeyLinkWidget(db_field.remote_field,
                                                    self.admin_site, using=kwargs.get('using'))
        return super(TabularInlineWithLinks, self). \
            formfield_for_foreignkey(db_field, request, **kwargs)


class StackedInlineWithLinks(admin.StackedInline):
    link_fields = []

    def __init__(self, *args, **kwargs):
        super(StackedInlineWithLinks, self).__init__(*args, **kwargs)
        self.object = None

    def get_formset(self, request, obj=None, **kwargs):
        self.object = obj
        return super(StackedInlineWithLinks, self).get_formset(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if self.link_fields and self.object is not None and db_field.name in self.link_fields:
            kwargs['widget'] = ForeignKeyLinkWidget(db_field.remote_field,
                                                    self.admin_site,
                                                    using=kwargs.get('using'))
        return super(StackedInlineWithLinks, self) \
            .formfield_for_foreignkey(db_field, request, **kwargs)


class ForeignKeyLinkWidget(ForeignKeyRawIdWidget):
    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['readonly'] = 'readonly'
        output = super(ForeignKeyLinkWidget, self).render(name, value, attrs)
        try:
            related_url = reverse(
                'admin:{}_{}_change'.format(
                    self.rel.model._meta.app_label,
                    self.rel.model._meta.model_name,
                ),
                args=[value],
            )
        except NoReverseMatch:
            return output

        return self.render_hidden_input(name, value, attrs) + mark_safe(
            u'<a class="fk-link" href="{url}">{label}</a>'.format(
                url=related_url, label=self.label_for_value(value)))

    def render_hidden_input(self, name, value, attrs=None):
        text_in = HiddenInput().render(name, value, attrs)
        return mark_safe(u'<div>{input}</div>'.format(input=text_in))
