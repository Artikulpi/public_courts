from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import inlineformset_factory
from account.decorators import admin_required
from corruption.models import Case, Article, Imprisonment, CriminalFines
from corruption.forms import CaseForm, ArticleForm

def home(request):
    cases_list = Case.objects.all()
    paginator = Paginator(cases_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)
    
    return render_to_response("corruption/home.html",
                              {"cases": cases,},
                              context_instance=RequestContext(request))

def view_case(request, case_id):
    try:
        case = Case.objects.get(pk=case_id)
    except ObjectDoesNotExist:
        raise Http404
    
    return render_to_response("corruption/view_case.html",
                              {"case": case,},
                              context_instance=RequestContext(request))

@admin_required
def admin(request):
    ImprisonmentFormSet = inlineformset_factory(Case, Imprisonment,
                                                    can_delete=False)
    CriminalFinesFormSet = inlineformset_factory(Case, CriminalFines,
                                                     can_delete=False)
    if request.method == "POST":
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            case_instance = form.save()
            formset = ImprisonmentFormSet(request.POST, instance=case_instance)
            if formset.is_valid():
                formset.save()
            
            cfformset = CriminalFinesFormSet(request.POST,
                                             instance=case_instance)
            if cfformset.is_valid():
                cfformset.save()
            
            return HttpResponseRedirect('./')
    else:
        form = CaseForm()
        formset = ImprisonmentFormSet()
        cfformset = CriminalFinesFormSet()
            
    cases_list = Case.objects.all().order_by("-id")
    paginator = Paginator(cases_list, 10)
    page = request.GET.get('page')
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)
        
    return render_to_response("corruption/admin/home.html",
                              {"cases": cases, "form": form,
                               "formset": formset, "cfformset": cfformset, },
                              context_instance=RequestContext(request))

@admin_required
def admin_view_case(request, case_id):
    try:
        case = Case.objects.get(pk=case_id)
        imprisonments = Imprisonment.objects.filter(case=case)
        criminal_fineses = CriminalFines.objects.filter(case=case)
    except ObjectDoesNotExist:
        raise Http404
    
    ImprisonmentFormSet = inlineformset_factory(Case, Imprisonment)
    CriminalFinesFormSet = inlineformset_factory(Case, CriminalFines)
    
    if request.method == "POST":
        form = CaseForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            
            formset = ImprisonmentFormSet(request.POST, instance=case)
            cfformset = CriminalFinesFormSet(request.POST, instance=case)
            if formset.is_valid() and cfformset.is_valid():
                formset.save()
                cfformset.save()
            
            return HttpResponseRedirect('./')
    else:
        form = CaseForm(instance=case)
        formset = ImprisonmentFormSet(instance=case)
        cfformset = CriminalFinesFormSet(instance=case)
    
    return render_to_response("corruption/admin/view_case.html",
                              {"case": case, "form": form,
                               "imprisonments": imprisonments,
                               "criminal_fineses": criminal_fineses,
                               "formset": formset, "cfformset": cfformset, },
                              context_instance=RequestContext(request))

@admin_required
def admin_del_case(request, case_id):
    if request.method == "POST":
        try:
            case = Case.objects.get(pk=request.POST.get("case-id"))
            case.delete()
        except ObjectDoesNotExist:
            raise Http404
    
    return HttpResponseRedirect("../../")

@admin_required
def admin_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('./')
    else:
        form = ArticleForm()
        
    articles = Article.objects.all()
    return render_to_response("corruption/admin/article.html",
                              {"articles": articles, "form": form, },
                              context_instance=RequestContext(request))
    
@admin_required
def admin_view_article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('./')
    else:
        form = ArticleForm(instance=article)
    
    return render_to_response("corruption/admin/view_article.html",
                              {"article": article, "form": form, },
                              context_instance=RequestContext(request))

@admin_required
def admin_del_article(request, article_id):
    if request.method == "POST":
        try:
            article = Article.objects.get(pk=request.POST.get("article-id"))
            article.delete()
        except ObjectDoesNotExist:
            raise Http404
    
    return HttpResponseRedirect("../../")
    
