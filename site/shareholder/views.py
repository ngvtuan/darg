from django.http import HttpResponse
from django.template import RequestContext, loader

def positions(request):
    template = loader.get_template('positions.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def log(request):
    template = loader.get_template('log.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def shareholder(request, shareholder_id):
    template = loader.get_template('shareholder.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
