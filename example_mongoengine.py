from mongoengine import connect, Document, StringField
import os


uri = "mongodb://{}:{}@{}/?authSource=admin".format(
    os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME"),
    os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD"),
    os.getenv("MONGODB_URL"))

print(uri)
connect(db="test", host=uri)



class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


user = User(email="test@test.com")
user.first_name = "Maksym"
user.last_name = "Sladkov"
user.save()
