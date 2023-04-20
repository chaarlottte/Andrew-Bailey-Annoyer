from faker.providers import user_agent, address
from faker import Faker
import random, string

class TotallyRealPerson():
    def __init__(self) -> None:
        self._fake = Faker()
        self._fake.add_provider(user_agent)

        self.first_name = self._fake.name().split(" ")[0]
        self.last_name = self._fake.name().split(" ")[1]

        self._gen_address()

        self.phone_num = self._gen_phone_number()
        self.email = self._gen_email()

        self.user_agent = self._fake.chrome(version_from=110, version_to=112)
        try:
            self.browser_ver = self.user_agent.split("Chrome/")[1].split(".")[0]
        except:
            pass
        pass

    def _gen_address(self) -> str:
        try:
            self.full_address = self._fake.address()
            self.street_address = self.full_address.split("\n")[0]
            self.city = self.full_address.split("\n")[1].split(",")[0]
            self.state = self.full_address.split("\n")[1].split(", ")[1].split(" ")[0]
            self.zip = self.full_address.split("\n")[1].split(", ")[1].split(" ")[1]
        except:
            # Gonna be fun when this library breaks and this recurses to the moon.
            self._gen_address()

    def _gen_phone_number(self) -> str:
        # Simply generate a 10-digit string, which SHOULD count as a valid phone number in the US.
        return ''.join(random.choice(string.digits) for i in range(10))
    
    def _gen_email(self) -> str:
        providers = [
            "gmail.com",
            "outlook.com",
            "hotmail.com",
            "yahoo.com"
        ]

        # This just takes our already-generated first name and last name, then puts an underscore in between them,
        # adds a random year, and adds an email provider.
        email = f"{self.first_name.lower()}_{self.last_name.lower()}{random.randint(1970, 2010)}@{random.choice(providers)}"
        return email

if __name__ == "__main__":
    TotallyRealPerson()