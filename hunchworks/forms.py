#!/usr/bin/env python

import models
import custom_fields

from django import forms
from django.forms import ModelForm
from django.forms.widgets import PasswordInput


class AuthUserForm(ModelForm):
  class Meta:
    model= models.User
    exclude = (
    'groups', 'user_permissions',
    )
    widgets = {
      'password': PasswordInput()
      }

class UserForm(ModelForm):
  skills = forms.CharField( max_length=100 )
  languages = forms.CharField( max_length=100 )

  class Meta:
    model = models.User
    exclude = (
    'show_profile_reminder', 'bio_text', 'phone', 'skills', 'user_id',
	'skype_name', 'website', 'profile_picture', 'education', 'classes', 
	'location_interests', 'roles', 'hunches', 'invited_users', 'groups',
	'collaborators', 'user',
	)

class HunchForm(ModelForm):
  skills_required = forms.CharField()
  languages_required = forms.CharField()
  tags = forms.CharField()
  hunch_collaborators = forms.CharField()

  class Meta:
    model = models.Hunch
    exclude = (
    'hunch_id', 'skills', 'groups', 'users', 'invited_users', 'hunch_tags',
    'time_created', 'time_modified', 'hunch_strength',
    )
    
class EvidenceForm(ModelForm):
    
  class Meta:
    model = models.Evidence
    exclude = (
    'hunch_id', 'creator_id', 'evidence_strength', 'time_created',
    'time_modified', 'attachments', 'albums', 'hunch', 'evidence_tags'
    )


class GroupForm(ModelForm):
  group_collaborators = forms.CharField()
  
  class Meta:
    model= models.Group


class HomepageForm(ModelForm):
  class Meta:
    model = models.User


class InvitePeople(forms.Form):
  invited_emails = custom_fields.MultiEmailField(widget=forms.Textarea(
    attrs={'cols': 30, 'rows': 10}))
  
  def save(self, *args, **kwargs):
    created_user = models.User.objects.get(pk=1)
    print self.cleaned_data
    #TODO( Chris: 8-15-2011): figure out how ot introspect invited_emails object instead
    # of using email_input
    for email_input in self.cleaned_data['invited_emails']:
      invited_email = models.InvitedUser( email=email_input )
      invited_user = models.UserInvites( invited_email=invited_email, user=created_user, status=0)
      invited_user.save()
    
