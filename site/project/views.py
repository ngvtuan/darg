from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required

def index(request):
    template = loader.get_template('index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

@login_required
def start(request):
    template = loader.get_template('start.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
