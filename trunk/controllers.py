import logging

import cherrypy

import turbogears
from turbogears import controllers, expose, validate, redirect

import model
import re
from conf import pkg
from base_controller import *
from base_controller import _dbg
from sqlobject.sqlbuilder import AND,OR,NOT,LEFTJOINOn

import hud_cti


log = logging.getLogger("busybe.controllers")


class AuthTables(object):
	user_group = model.Community


class BusyBeBase(Base):
	def _set_auth_tables(self):
		self.auth_dict['user_group'] = model.Community


class BusyBeMenu(Menu):
	def _set_auth_tables(self):
		self.auth_dict['user_group'] = model.Community


class User(BusyBeBase):
	tbl = model.User
	fields = dict(
			password = dict(
					type = 'passwd',
				),
		)


class AccessLevel(BusyBeBase):
	show = 10
	tbl = model.AccessLevel


class Permission(BusyBeBase):
	tbl = model.Permission


class Person(BusyBeBase):
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


class Community(BusyBeBase):
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
		self.auth('edit')
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


class PersonCommunity(BusyBeBase):
	tbl = model.PersonCommunity
	title = 'Membership'
	default_fields = (
			'active',
			'community',
			'person',
		)


class Event(BusyBeBase):
	tbl = model.Event


class Participant(BusyBeBase):
	tbl = model.Participant
	fields = dict(
			event = dict(
					column = ('name', 'start'),
					format = '%s on %s',
				),
		)


class CallType(BusyBeBase):
	show = 5
	tbl = model.Calltypecat


class Root(BusyBeMenu):
	title = 'BusyBeMenu'
	person = Person()
	community = Community()
	membership = PersonCommunity()
	event = Event()
	participant = Participant()
	inbound = hud_cti.Inbound()
	outbound = hud_cti.Outbound()
	user = User()
	access_level = AccessLevel()
	permission = Permission()
	call_type = CallType()


