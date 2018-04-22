from django.db import models

class PostQuerySet(models.QuerySet):
    def published_posts(self):
        return self.filter(published_at__isnull=False)

    def unpublished_posts(self):
        return self.filter(published_at__isnull=True)