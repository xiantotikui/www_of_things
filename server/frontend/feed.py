import json
from datetime import datetime, timezone
                              
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Server, Device, Alert

class AlertsFeed(View):
    def __init__(self):
        self.feed = {}
        self.feed['version'] = 'https://jsonfeed.org/version/1'
        
        self.feed['title'] = 'Alarmy WoT'
        self.feed['description'] = 'Powiadomienia o sytuacjach nadzwyczajnych.'
        self.feed['home_page_url'] = 'https://server.fuszara.pl/'
        self.feed['feed_url'] = 'https://server.fuszara.pl/alerts/feed.json'
        self.feed['author'] = {}
        self.feed['author']['name'] = 'Łukasz Fuszara'
        self.feed['author']['url'] = 'https://www.fuszara.pl/'
        self.feed['items'] = []
    def get(self, request):
        elements = Alert.objects.all().order_by("-id")[:10]
        server = Server.objects.get(id=1).server_address
        counter = 0
        for e in elements:
            item_address = e.address
            url = item_address.split('/')
            address = 'https://' + url[2] + '/'
            value = url[3]
            name = url[4]
            device = Device.objects.get(device_address=address).id
            link = '{}device/{}/{}/{}'.format(server, device, value, name)
            self.feed['items'].append({
                'title': e.address,
                'date_published': e.created_date.astimezone().isoformat(),
                'id': link,
                'url': link,
                'content_html': e.value
            })
            counter += 1
        return JsonResponse(self.feed)

@csrf_exempt
def get(request):
    if request.method == 'POST':
        response = json.loads(request.body.decode('utf8'))['alert']
        Alert.objects.create(address=response['address'], value=response['value'])
        return HttpResponse()
