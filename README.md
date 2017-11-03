Django admin links
-------------------

### Installation
This package can be installed via pip using `pip install django_admin_links`

### Use
Django admin links is a tools using which you can 
represent foreign keys as read-only links in django
admin in order to facilitate navigability.

In order to use this tool, you should let your django 
admin classes inherit from `ModelAdminWithLinks` instead
of inheriting directly from `admin.ModelAdmin`. Similar
approach can be taken for `TabularInlineWithLinks` and
`StackedInlineWithLinks`. After doing that, you can define
a field on your admin class called `link_fields` and specify
names of the fields, you want to be represented as links in there.
It should be some iterable like a list or a tuple.
It is worth noting that fields included in `link_fields` should 
also be included in `fields`.
