from django.utils.text import slugify

from apps.organizations.models import Organization


def generate_unique_slug(name: str) -> str:
    """
    Generate a unique slug
    """

    base_slug = slugify(name)
    slug = base_slug
    counter = 2

    while Organization.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
        
    return slug