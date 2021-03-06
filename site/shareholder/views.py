from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext as _

from sendfile import sendfile

from shareholder.models import Shareholder, OptionPlan
from utils.formatters import human_readable_segments


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
    securities = shareholder.company.security_set.all()

    # hack security props for shareholder spec data
    for sec in securities:
        if sec.track_numbers:
            if shareholder.current_segments(sec):
                sec.segments = human_readable_segments(
                    shareholder.current_segments(sec))
        sec.count = shareholder.share_count(security=sec) or 0
    context = RequestContext(request, {
                             'shareholder': shareholder,
                             'securities': securities})
    return HttpResponse(template.render(context))


@login_required
def optionsplan(request, optionsplan_id):
    template = loader.get_template('optionsplan.html')
    optionsplan = get_object_or_404(OptionPlan, id=int(optionsplan_id))
    context = RequestContext(request, {"optionplan": optionsplan})
    return HttpResponse(template.render(context))


@login_required
def optionsplan_download_pdf(request, optionsplan_id):
    optionplan = OptionPlan.objects.get(id=optionsplan_id)
    if optionplan.company.operator_set.filter(user=request.user).exists():
        return sendfile(request, optionplan.pdf_file.path)
    else:
        return HttpResponseForbidden(_("Permission denied"))


@login_required
def optionsplan_download_img(request, optionsplan_id):
    optionplan = OptionPlan.objects.get(id=optionsplan_id)
    if optionplan.company.operator_set.filter(user=request.user).exists():
        return sendfile(request, optionplan.pdf_file_preview_path())
    else:
        return HttpResponseForbidden(_("Permission denied"))
