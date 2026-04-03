from catalog.models import Category
for c in Category.objects.all(): print(c.id, repr(c.name))
