from django.http import HttpResponse
from combosearcher.models import Combos
import time


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def upload_combos(request):
    start_time = time.time()
    with open('toupload.csv', 'r',encoding="utf8") as csvfile:
        lines = csvfile.readlines()

    chunks = [lines[x:x + 100] for x in range(0, len(lines), 1000)]
    running_chunk = 0
    for chunk in chunks:
        running_chunk += 1
        print(f"Running Chunks: {running_chunk}/{len(chunks)}")
        to_bulk_create = []
        for line in chunk:
            try:
                line_split = line.split(',')
                url = line_split[0]
                username = line_split[1]
                password = line_split[2]
            except IndexError:
                continue
            to_bulk_create.append(Combos(url=url, username=username, password=password))
        objs = Combos.objects.bulk_create(to_bulk_create)
        print("--- %s seconds Lapsed---" % (time.time() - start_time))
    return HttpResponse("All data uploaded successfully")
