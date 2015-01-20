from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
import datetime

# Create your views here.
def index(request):
    return render_to_response('index.html', {'name':'ming'})


def home(request):
    html = "<html><body>now is %s</body></html>" % (datetime.datetime.now())
    request.session.set_test_cookie()
    return HttpResponse(html)

def stock(request, stock_code):
    name = 'testing'
    if 'q' in request.GET and request.GET['q']:
        stock_name = request.GET['q']
        
    if int(stock_code) < 100:
        response = render_to_response('stock.html', locals())
        if request.session.test_cookie_worked():
            response.set_cookie('color', 'blue')
        return response
    else:
        raise Http404()
