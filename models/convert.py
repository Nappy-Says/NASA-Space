from models.models import *

last_id = 0

f = open("txt.txt", "r")

for content in f:
    if content[0] == '0':
        print(content)
        satellite = Satellite(name=content)
        satellite.save()

        last_id = satellite.id

    if content[0] == '1' or content[0] == '2':
        Lines(line=str(content), satellite=last_id).save()
