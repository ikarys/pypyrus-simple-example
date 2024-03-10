import re

class PypyrusFilters:
    @staticmethod
    def slug(input_string):
        slug = input_string.replace(' ', '-').replace('_', '-').lower()
        slug = re.sub(r'[^a-zA-Z0-9_-]', '', slug)
        slug = slug.lower()
        return slug