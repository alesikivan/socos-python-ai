# views.py
from django.http import HttpResponse
import datetime

from pkg import parser

def parse(request, url):
    text = parser.parse(url)

    return HttpResponse(text)

def main(request):
    return HttpResponse("Hello world!")

# def test(request):
#     import time
#
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#
#     return HttpResponse(html)
