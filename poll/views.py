from django.shortcuts import render
from .models import *
from django.http import Http404,HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView
from django.db.models import Q
from ems.decorators import *
from poll.forms import *
# Create your views here.
def index(request):
    context = {}
    context['title']='polls'
    context['x']=Question.objects.all()
    return render(request,'poll/index.html',context)
def details(request,id=None):
    context={}
    context['y']=Question.objects.get(id=id)
    context['c']=Question.objects.get(id=id).choice_set.all()
    return render(request,'poll/details.html',context)
def poll(request,id=None):
    if request.method=='GET':
        try:
            question=Question.objects.get(id=id)
        except:
            raise Http404
        context={}
        context['y']=Question.objects.get(id=id)
        return render(request,'poll/poll.html',context)
    if request.method=='POST':
        user_id=1
        data=request.POST
        ret=Answer.objects.create(user_id=user_id,choice_id=data['choice'])
        if ret:
            return HttpResponse('your work is done successfully')
        else:
            return HttpResponse('sorry!')







class PollView(View):
    decorators = [login_required, admin_hr_required]

    #@method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Question, id=id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choices]
            template = 'poll/edit_poll.html'
        else:
            poll_form = PollForm(instance=Question())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            template = 'poll/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)

   # @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Question())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/poll/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/new_poll.html', context)

   # @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Question, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('/poll/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/edit_poll.html', context)

   # @method_decorator(decorators)
    def delete(self, request, id=None):
        question = get_object_or_404(Question,id=id)
        question.delete()
        return redirect('polls_list')