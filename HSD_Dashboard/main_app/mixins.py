from django.contrib.auth.mixins import UserPassesTestMixin

class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.role =='A'