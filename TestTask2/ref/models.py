from django.db import models
from django.contrib.auth.models import User


class ReferalUser(models.Model):
    user_stat = models.OneToOneField(User, unique=True)
    point = models.PositiveSmallIntegerField(default=0)
    referal = models.EmailField(max_length=225, null=True, blank=True, default=None)

    class Meta:
        ordering = ["-point"]


class ReferalNumber(models.Model):
    link = models.PositiveSmallIntegerField(unique=True)
    cost_link = models.PositiveSmallIntegerField(default=1)
    ref_user = models.OneToOneField(ReferalUser)

    def activate_link(self, joiner):
        self.cost_link += 1
        print(self.cost_link)
        temp = 0
        joiner = ReferalUser.objects.get(user_stat__email=joiner.referal)
        while not joiner == self.ref_user:
            print(joiner.user_stat.email)
            print(self.ref_user.user_stat.email)
            print('in while')
            joiner.point += 1
            joiner.save()
            temp +=1
            joiner = ReferalUser.objects.get(user_stat__email=joiner.referal)
        self.ref_user.point += (self.cost_link - temp)
        self.ref_user.save()
        self.save()