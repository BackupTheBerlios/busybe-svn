import logging

import cherrypy

import turbogears
from turbogears import controllers, expose, validate, redirect

from busybe import json

import model
import re
from conf import pkg
from base_controller import *
from base_controller import _dbg
from sqlobject.sqlbuilder import AND,OR,NOT,LEFTJOINOn


log = logging.getLogger("busybe.controllers")


class Person(Base):
	show = 3
	tbl = model.Person
	default_fields = (
			'name',
			'full_name',
			'active',
			'address',
			'home_phone',
			'office_phone',
			'mobile_phone',
			'birth_date',
			'money',
			'no_of_peanuts',
			'weight',
		)
	column_fields = (
			'name',
			'full_name',
			'active',
			'money',
			'no_of_peanuts',
			'weight',
		)


class Community(Base):
	tbl = model.Community
	title = 'Group'
	default_fields = (
			'name',
			'leader',
		)

	def _init_(self):
		self.mtm_tbl = model.PersonCommunity
		self.mtm_col = 'community'
		self.rel_tbl = model.Person
		self.rel_col = 'leader'
		self.mtm_rel_col = 'person'

	@expose(template='%s.templates.edit' % pkg)
	def edit(self, id, **kw):
		page_dict = self._edit(id, **kw)
		page_dict['fields']['leader']['options'] = self.get_persons(id)
		return page_dict

	def get_persons(self, id):
		'''Make sure we only show persons that aren't members of any community or is a member of the community
		'''
		id = int(id)
		rels = self.mtm_tbl.selectBy(community=id, deleted=False)
		where_ors = []
		for rel in rels:
			where_ors.append(self.rel_tbl.q.id==rel.personID)
		options = self._get_rows(
				self.rel_tbl,
				('name', ),
				where_or=where_ors,
			)
		return options

	@expose()
	def save0(self, id=None, **kw):
		row = self._save(id, **kw)
		turbogears.redirect('index')


class PersonCommunity(Base):
	tbl = model.PersonCommunity
	title = 'Membership'
	default_fields = (
			'active',
			'community',
			'person',
		)


class Event(Base):
	tbl = model.Event


class Participant(Base):
	tbl = model.Participant
	fields = dict(
			event = dict(
					column = ('name', 'start'),
					format = '%s on %s',
				),
		)


class Root(Menu):
	title = 'Menu'
	person = Person()
	community = Community()
	membership = PersonCommunity()
	event = Event()
	participant = Participant()


