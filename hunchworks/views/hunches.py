#!/usr/bin/env python

from hunchworks import models, forms
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required


def showHunch(request, hunch_id):
  """Show a Hunch."""
  hunch = get_object_or_404(models.HwHunch, pk=hunch_id)

  if not hunch.is_viewable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  context.update({ "hunch": hunch })
  return render_to_response('showHunch.html', context)


@login_required
def createHunch(request):
  """Create a Hunch.  Assumes HwHunch.user = request.user! """
  context = RequestContext(request)
  if request.method == 'POST':

    data = request.POST.copy()
    data.update({'creator':request.user.pk, 'status':2})
    hw_hunch_form = forms.HwHunchForm(data, instance=models.HwHunch())
    hw_evidence_form = forms.HwEvidenceForm(data, instance=models.HwEvidence())

    if hw_hunch_form.is_valid() and hw_evidence_form.is_valid():
      hw_hunch = hw_hunch_form.save()

      languages_required = request.POST['languages_required']
      languages_required = languages_required.split(',')
      for skill_id in languages_required:
        skill_connection = models.HwSkillConnections.objects.create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

      skills_required = request.POST['skills_required']
      skills_required = skills_required.split(',')
      for skill_id in skills_required:
        skill_connection = models.HwSkillConnections.objects.create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

      tags = request.POST['tags']
      tags = tags.split(',')
      for tag_id in tags:
        tag_connection = models.HwTagConnections.objects.create(
          tag=models.HwTag.objects.get(pk=tag_id),
          hunch=hw_hunch)

      hunch_collaborators = request.POST['hunch_collaborators']
      hunch_collaborators = hunch_collaborators.split(',')
      hunch_collaborators.append( request.user.pk )
      for user_id in hunch_collaborators:
        hunch_connection = models.HwHunchConnections.objects.create(
          user=models.HwUser.objects.get(pk=user_id),
          hunch=hw_hunch,
          status=0)

      hw_evidence = hw_evidence_form.save(commit=False)
      hw_evidence.hunch_id = hw_hunch.pk
      hw_evidence.save()
      return HttpResponseRedirect('/hunchworks/profile')
    else:
      hunch_form = forms.HwHunchForm(request.POST)
      evidence_form = forms.HwEvidenceForm(request.POST)
  else:
    hunch_form = forms.HwHunchForm()
    evidence_form = forms.HwEvidenceForm()

  context.update({ 'hunch_form':hunch_form, 'evidence_form':evidence_form,
    'user_id': request.user.pk })
  return render_to_response('createHunch.html', context)


@login_required
def editHunch(request, hunch_id):
  """Edit a Hunch."""
  hunch = get_object_or_404(models.HwHunch, pk=hunch_id)
  if not hunch.is_editable_by(request.user):
    raise PermissionDenied

  context = RequestContext(request)
  if request.method == 'POST':
    data = request.POST.copy()
    data.update({'creator':request.user.pk, 'status':2})
    hw_hunch_form = forms.HwHunchForm(data, instance = hunch)

    if hw_hunch_form.is_valid():
      hw_hunch = hw_hunch_form.save()

      #create new language skills for this hunch
      languages_required = request.POST['languages_required']
      languages_required = languages_required.split(',')
      for skill_id in languages_required:
        skill_connection = models.HwSkillConnections.objects.get_or_create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

    #create new non language skills for this hunch
      skills_required = request.POST['skills_required']
      skills_required = skills_required.split(',')
      for skill_id in skills_required:
        skill_connection = models.HwSkillConnections.objects.get_or_create(
          skill=models.HwSkill.objects.get(pk=skill_id),
          hunch=hw_hunch,
          level=1)

      #remove unneeded language and skills from this hunch
      skill_connections = models.HwSkillConnections.objects.filter(hunch=hw_hunch.pk)
      skills = languages_required + skills_required

      for skill_connection in skill_connections:
        if str(skill_connection.skill_id) not in skills:
          models.HwSkillConnections.objects.get(pk=skill_connection.pk).delete()

      #create new tags for this hunch
      tags = request.POST['tags']
      tags = tags.split(',')
      for tag_id in tags:
        tag_connection = models.HwTagConnections.objects.get_or_create(
          tag=models.HwTag.objects.get(pk=tag_id),
          hunch=hw_hunch)

      #remove unneeded tags from this hunch
      tag_connections = models.HwTagConnections.objects.filter(hunch=hw_hunch.pk)

      for tag_connection in tag_connections:
        if str(tag_connection.tag_id) not in tags:
          models.HwTagConnections.objects.get(pk=tag_connection.pk).delete()

      #create new collaborators for this hunch
      hunch_collaborators = request.POST['hunch_collaborators']
      hunch_collaborators = hunch_collaborators.split(',')
      hunch_collaborators.append( request.user.pk )
      for user_id in hunch_collaborators:
        hunch_connection = models.HwHunchConnections.objects.get_or_create(
          user=models.HwUser.objects.get(pk=user_id),
          hunch=hw_hunch,
          status=0)

      #remove unneeded collaborators from this hunch
      hunch_connections = models.HwHunchConnections.objects.filter(hunch=hw_hunch.pk)

      for hunch_connection in hunch_connections:
        if str(hunch_connection.user_id) not in hunch_collaborators:
          models.HwHunchConnections.objects.get(pk=hunch_connection.pk).delete()

      return HttpResponseRedirect('/hunchworks/profile')
    else:
      hunch_form = forms.HwHunchForm(request.POST)
  else:
    hunch_form = forms.HwHunchForm(instance = hunch)

  context.update({ 'hunch_id': hunch_id, 'user_id': request.user.pk,
    'hunch_form': hunch_form })
  return render_to_response('editHunch.html', context)