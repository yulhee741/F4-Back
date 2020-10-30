from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, F


REVIEW_RATING_CHOICES = (
    (1, _('Terrible')),
    (2, _('Poor')),
    (3, _('Average')),
    (4, _('Very Good')),
    (5, _('Excellent')),
)


class Review(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, blank=False, null=True)
    place = models.ForeignKey("place.Place", on_delete=models.CASCADE, blank=False, null=True)
    content = models.TextField(blank=False, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    rating = models.FloatField(choices=REVIEW_RATING_CHOICES, blank=False, null=True)
    # review_likes = models.ManyToManyField(User, related_name='review_likes', default=None, blank=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        from place.models import Place
        if not self.pk:
            Place.objects.filter(pk=self.place_id).update(counts=F('counts') + 1)
        super().save(*args, **kwargs)

    # def count_likes(self):
    #     # total likes_user
    #     return self.likes.count()
