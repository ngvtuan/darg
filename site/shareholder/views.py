from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from shareholder.models import Shareholder

@login_required
def positions(request):
    template = loader.get_template('positions.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

@login_required
def log(request):
    template = loader.get_template('log.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

@login_required
def shareholder(request, shareholder_id):
    template = loader.get_template('shareholder.html')
    shareholder = get_object_or_404(Shareholder, id=int(shareholder_id))
    context = RequestContext(request, {'shareholder': shareholder})
    return HttpResponse(template.render(context))
