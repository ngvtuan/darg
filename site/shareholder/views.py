from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from shareholder.models import Shareholder, OptionPlan


@login_required
def positions(request):
    template = loader.get_template('positions.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


@login_required
def options(request):
    template = loader.get_template('options.html')
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


@login_required
def optionsplan(request, optionsplan_id):
    template = loader.get_template('optionsplan.html')
    optionsplan = get_object_or_404(OptionPlan, id=int(optionsplan_id))
    context = RequestContext(request, {"optionplan": optionsplan})
    return HttpResponse(template.render(context))
