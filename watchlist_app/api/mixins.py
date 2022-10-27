

class UserQuerysetMixin():
    allow_staff_view = False
    user_field = "user"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        queryset = super(UserQuerysetMixin, self).get_queryset(*args, **kwargs)
        if self.allow_staff_view and user.is_staff:
            return queryset
        return queryset.filter(**lookup_data)
