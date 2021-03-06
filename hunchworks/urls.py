#!/usr/bin/env python

from django.conf.urls.defaults import *
from hunchworks.views import dashboard, auth, users, groups, hunches, evidences, explore, feeds, bookmark, static
from hunchworks import forms


urlpatterns = patterns(
  "hunchworks.views",

  # embed
  url(r"^embed/", include("djembedly.urls")),

  # tokeninputs
  # https://github.com/adammck/djtokeninput
  url(r"^djtokeninput/", include("djtokeninput.urls")),

  # dashboard/home/index
  url(r"^$", dashboard.dashboard, name="dashboard"),

  # auth
  url(r"^login$",        auth.login,        name="login"),
  url(r"^login/error/$", auth.error,        name="login_error"),
  url(r"^logout$",       auth.logout,       name="logout"),
  url(r"^signup$",       auth.signup,       name="signup"),
  url(r"^invitePeople",  auth.invitePeople, name="invitePeople"),
  url(r"", include("social_auth.urls")),

  # users
  url(r"^profile/(?P<user_id>\d+)$",         users.profile,     name="profile"),
  url(r"^profile/(?P<user_id>\d+)/edit$",    users.edit,        name="edit_profile"),
  url(r"^connections$",                      users.connections, name="connections"),
  url(r"^profile/(?P<user_id>\d+)/connect$", users.connect,     name="connect"),
  url(r"^profile/(?P<user_id>\d+)/remove$",  users.remove,      name="remove"),

  # groups
  url(r"^groups$",                           groups.index,    name="groups"),
  url(r"^groups/my$",                        groups.my,       name="my_groups"),
  url(r"^groups/all$",                       groups.all,      name="all_groups"),
  url(r"^groups/(?P<group_id>\d+)$",         groups.show,     name="group"),
  url(r"^groups/(?P<group_id>\d+)/edit$",    groups.edit,     name="edit_group"),
  url(r"^groups/create",                     groups.create,   name="create_group"),
  url(r"^groups/(?P<group_id>\d+)/join$",    groups.join,     name="join_group"),
  url(r"^groups/(?P<group_id>\d+)/leave$",   groups.leave,    name="leave_group"),
  url(r"^groups/(?P<group_id>\d+)/hunches$", groups.hunches,  name="group_hunches"),

  # hunches
  url(r"^hunches$",                                hunches.index,        name="hunches"),
  url(r"^hunches/my$",                             hunches.my,           name="my_hunches"),
  url(r"^hunches/all$",                            hunches.all,          name="all_hunches"),
  url(r"^hunches/finished$",                       hunches.finished,     name="finished_hunches"),
  url(r"^hunches/open$",                           hunches.open,         name="open_hunches"),
  url(r"^hunches/(?P<hunch_id>\d+)$",              hunches.show,         name="hunch"),
  url(r"^hunches/(?P<hunch_id>\d+)/activity$",     hunches.activity,     name="hunch_activity"),
  url(r"^hunches/(?P<hunch_id>\d+)/comments$",     hunches.comments,     name="hunch_comments"),
  url(r"^hunches/(?P<hunch_id>\d+)/contributors$", hunches.contributors, name="hunch_contributors"),
  url(r"^hunches/(?P<hunch_id>\d+)/permissions$",  hunches.permissions,  name="hunch_permissions"),

  url(r"^hunches/(?P<hunch_id>\d+)/edit$",         hunches.edit,         name="edit_hunch"),
  url(r"^hunches/(?P<hunch_id>\d+)/follow$",       hunches.follow,       name="follow_hunch"),
  url(r"^hunches/(?P<hunch_id>\d+)/unfollow$",     hunches.unfollow,     name="unfollow_hunch"),

  url(r"^hunches/(?P<hunch_id>\d+)/evidence$",                      hunches.hunch_evidences, name="hunch_evidences"),
  url(r"^hunches/(?P<hunch_id>\d+)/evidence/(?P<evidence_id>\d+)$", hunches.hunch_evidence,  name="hunch_evidence"),

  # create hunch wizard
  url(r'^hunches/create$', hunches.HunchWizard.as_view([
    forms.hunch.HunchFormOne,
    forms.hunch.HunchFormTwo,
    forms.hunch.HunchFormThree,
    forms.hunch.HunchFormFour
  ]), name="create_hunch"),

  # hunch evidence
  url(r"^hunches/(?P<hunch_id>\d+)/evidence/add$", hunches.add_evidence, name="add_hunch_evidence"),

  # hunch feeds
  url(r"^hunches/feed/$",                    feeds.RecentHunchFeed()),
  url(r"^hunches/(?P<hunch_id>\d+)/feed$",   feeds.EvidencesFeed()),

  # evidences
  url(r"^evidence$",                           evidences.index,  name="evidences"),
  url(r"^evidence/(?P<evidence_id>\d+)$",      evidences.show,   name="evidence"),
  url(r"^evidence/(?P<evidence_id>\d+)/edit$", evidences.edit,   name="edit_evidence"),
  url(r"^evidence/create$",                    evidences.create, name="create_evidence"),

  url(r"^evidences/search.json$", evidences.search, name="search_evidence"),

  # explore external evidences
  url(r"^explore$", explore.explore, name="explore"),

  url(r'^evidences/search.json$', evidences.search, name="search_evidence"),

  # bookmarks
  url(r'^bookmark/(?P<object_type>[a-zA-Z]+)/(?P<object_id>\d+)$',   bookmark.add,      name="bookmark"),
  url(r'^unbookmark/(?P<object_type>[a-zA-Z]+)/(?P<object_id>\d+)$', bookmark.delete,   name="unbookmark"),
  url(r'^bookmarks/groups$',                                         bookmark.groups,   name="bookmarked_groups"),
  url(r'^bookmarks/hunches$',                                        bookmark.hunches,  name="bookmarked_hunches"),
  url(r'^bookmarks/evidence$',                                       bookmark.evidence, name="bookmarked_evidence"),
  url(r'^bookmarks/all$',                                            bookmark.all,      name="bookmarked_all"),

  # static pages
  url(r"^about/privacy$", static.page, kwargs={ "template": "privacy" }, name="about_privacy"),
  url(r"^about/scoring$", static.page, kwargs={ "template": "scoring" }, name="about_scoring"),
)
