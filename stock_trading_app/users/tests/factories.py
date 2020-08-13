import factory
from django.contrib.auth import get_user_model
from stock_trading_app.users.models import Profile

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)
        else:
            password = factory.Faker(
                "password",
                length=10,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate()

            self.set_password(password)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        django_get_or_create = ("user",)

    type = Profile.TRADER
    user = factory.SubFactory(UserFactory, profile=None)
