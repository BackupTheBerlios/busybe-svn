'''The Base Controller for BusyBe - this can be used for Turbogears projects

Copyright (C) 2006 8Layer Technologies (http://www.8layertech.com/)
 
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.
 
This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
02110-1301, USA.
 
Author's contact info:
 Website: http://www.8layertech.com/
 E-mail Address: ecalso@8layertech.com
 Office Address: 218 AIC-Burgundy Empire Tower, ADB Avenue
                 Cor. Sapphire and Garnet Roads, Ortigas
				 Center, Pasig City, Philippines, 1605
 Office Phone: +63(2)7060501 or +63(2)7060502 local 803
 Mobile Phone: +63(919)8468862
'''

import cherrypy
import crypt, string, random
import datetime
import re
import turbogears
from turbogears import controllers, identity, redirect
from sqlobject import SQLObject, SQLObjectNotFound, BoolCol
from sqlobject.sqlbuilder import AND, OR, NOT, LEFTJOINOn
from MySQLdb.connections import OperationalError
from formencode import validators

BaseUrl = '/'
Now = datetime.datetime.now


def beautify(text):
	'''Capitalize the first letter of each word.
	'''
	text = ' '.join(text.split('_'))
	text = ' '.join(text.split('.'))
	words = (word.capitalize() for word in text.split(' '))
	text = ' '.join(words)
	return text


def expose(*args, **kw):
	'''BusyBe's version of Turbogear's version of Cherrypy's expose.
	
	This is for the authentication of the user.
	'''
	decorator = turbogears.expose(*args, **kw)
	return decorator


def get_count(code):
	'''Return an integer for an auto-generated code.
	'''
	if re.search('-', code):
		pre,count = code.split('-')
	else:
		count = code
	#TODO Return an exception if count cannot be an integer
	return int(count)


def get_salt(chars = string.letters + string.digits):
	'''Get two random letter/number to be used for the crypt.
	'''
	return random.choice(chars) + random.choice(chars)


def sort_page_rows(rows, sort_page_by=None):
	'''Sort a list of entries retrieved from a database query.
	'''
	if sort_page_by:
		if cherrypy.session.has_key('sort_page_by'):
			cherrypy.session['prev_sort_page_by'] = cherrypy.session['sort_page_by']
		cherrypy.session['sort_page_by'] = sort_page_by
		tmp = {}
		for row in rows:
			key = '%s%s' % (getattr(row, sort_page_by), row.id)
			tmp[key] = row
		rows = []
		keys = tmp.keys()
		keys.sort()
		if cherrypy.session.has_key('prev_sort_page_by') and cherrypy.session['sort_page_by'] == cherrypy.session['prev_sort_page_by']:
			keys.reverse()
			del(cherrypy.session['sort_page_by'])
			del(cherrypy.session['prev_sort_page_by'])
		for key in keys:
			rows.append(tmp[key])
	return rows


def select_all(model_table):
	'''Get all entries from a DB table that's not deleted.
	'''
	if hasattr(model_table.q, 'deleted'):
		return model_table.select(model_table.q.deleted==False)
	else:
		return model_table.select()


class AuthController(controllers.Root):
	@turbogears.expose(template="templates.login")
	def login(self, forward_url=None, previous_url=None, *args, **kw):

		if not identity.current.anonymous \
			and identity.was_login_attempted() \
			and not identity.get_identity_errors():
			raise redirect(forward_url)

		forward_url=None
		previous_url= cherrypy.request.path

		if identity.was_login_attempted():
			msg=_("The credentials you supplied were not correct or "
				   "did not grant access to this resource.")
		elif identity.get_identity_errors():
			msg=_("You must provide your credentials before accessing "
				   "this resource.")
		else:
			msg=_("Please log in.")
			forward_url= cherrypy.request.headers.get("Referer", "/")
		cherrypy.response.status=403
		return dict(message=msg, previous_url=previous_url, logging_in=True,
					original_parameters=cherrypy.request.params,
					forward_url=forward_url)

	@turbogears.expose()
	def logout(self):
		identity.current.logout()
		raise redirect("/")


class MenuController(controllers.Root):
	exclude = ['exclude', 'index', 'module', 'modules', 'accesslog', 'is_app_root', 'msglog', 'msglogfunc', ]
	def _get_modules(self):
		modules = (attr for attr in dir(self.__class__) if attr not in self.exclude and attr != 'get_modules' and not re.match('^_', attr))
		return modules

	@turbogears.expose(template="templates.menu")
	def index(self):
		import time
		now = time.ctime()
		modules = self._get_modules()
		return dict(
				now=now,
				modules = modules,
				title = beautify(re.sub('.*\.', '', self.__class__.__module__)),
			)


class BaseController(controllers.Root):
	'''This is the base class for creating database-driven
	web-based aps.
	
	The attributes and methods here are the ones that can be
	commonly used to List, Edit, and Delete items in a DB
	Table. The methods rely on the templates
	'template/edit.kid' for editing and 'template/list.kid'
	to list the rows.
	
	TODO:
	- Modify the list method to and template to view only a
	  maximum number of rows per page; and show 'previous'
	  and 'next' links accordingly.
	- Modify the lists to be viewed based on a particular
	  order (the user should be able to arrange the list
	  based on the column_fields).
	- On deleting, check with the user first to be sure that
	  the item is what's intended to be deleted.
	- Modify the delete method (and prolly add another
	  template) to enable deleting of individual items
	  (hint: this can be used for the previous TODO)
	- Begin the details method -- this is intended to show
	  the details of a specific item on an immutable page.
	  "Delete" and "Edit" buttons should be shown in this
	  page.
	- The sidebar is currently on the master template. This
	  should be transfered to a method here.
	- Modify the index method to do what it says -- it doesn't
	  authenticate right now for ease of testing the other
	  methods.
	'''
	#now = now
	actions = []
	column_fields = ()
	detail_fields = ()
	entry_details = []
	fields = {}
	hidden_fields = ()
	item_details = {}
	parent_fields = ()
	search_fields = ()

	def _details(self, id, **kw):
		return dict(
			)
	_details.__doc__ = ''

	def _delete_item(self, id):
		item = self.tbl_obj.get(id)
		# mark item as deleted if the table has a column name deleted
		# otherwise, just delete the item
		if hasattr(item, 'deleted'):
			item.deleted = True
			for field in self.detail_fields:
				try:
					exec('value = item.%s' % field)
					setattr(item, field, 'deleted%s\b%s' % (item.id, value))
				except:
					pass
		else:
			item.delete(id)

	def _edit(self, id):
		row = self.tbl_obj.get(id)
		for name in self.search_fields:
			exec('self.fix_field(name, value=row.%s)' % name)
			if self.fields[name].has_key('type'):
				if self.fields[name]['type'] == dict:
					exec('self.fix_field(name, value=row.%s.id)' % name)
		for name in self.detail_fields:
			exec('self.fix_field(name, value=row.%s)' % name)
			if self.fields[name].has_key('type'):
				if self.fields[name]['type'] == dict:
					exec('self.fix_field(name, value=row.%s.id)' % name)
		return dict(
				title = 'Edit %s' % self.__class__.__name__,
				details = self.detail_fields,
				entry_details = self.entry_details,
				fields = self.fields,
				id = id,
				item_details = self.item_details,
				new = False,
			)
	_edit.__doc__ = ''

	def _fix_field(self, name, description=None, value=None, **kw):
		if self.fields.has_key(name):
			pass
		else:
			self.fields[name] = {}
		if description:
			self.fields[name]['description'] = description
		elif self.fields[name].has_key('description'):
			pass
		else:
			self.fields[name]['description'] = beautify(name)
		if value:
			self.fields[name]['value'] = value
		else:
			self.fields[name]['value'] = ''
		if not self.fields[name].has_key('type'):
			if name in self.tbl_obj._columnDict.keys():
				col_type = str(self.tbl_obj._columnDict[name])
				if re.search('Bool', col_type):
					self.fields[name]['type'] = 'bool'
				elif re.search('Int', col_type):
					self.fields[name]['type'] = 'int'
				elif re.search('Float', col_type):
					self.fields[name]['type'] = 'float'
				elif re.search('Time', col_type):
					self.fields[name]['type'] = 'time'
				elif re.search('DateTime', col_type):
					self.fields[name]['type'] = 'datetime'
				elif re.search('Date', col_type):
					self.fields[name]['type'] = 'date'
			if name+'ID' in self.tbl_obj._columns:
				self.fields[name]['type'] = 'select'
		for k,v in kw.items():
			self.fields[name][k] = v
		# These lines remove the fields that are not in the database -- disabled for recursive searches
		#if name not in self.tbl_obj._columnDict.keys() and name+'ID' not in self.tbl_obj._columnDict.keys():
		#	del self.fields[name]
	_fix_field.__doc__ = ''

	def _get_query_results(self, *clauses, **kw):
		if hasattr(self.tbl_obj.q, 'deleted'):
			return self.tbl_obj.select(AND(
					self.tbl_obj.q.deleted==False,
					*clauses
				))
		elif (kw.has_key('show_del') and kw['show_del']):
			return self.tbl_obj.select(AND(*clauses))
		elif len(clauses) > 1:
			return self.tbl_obj.select(AND(*clauses))
		else:
			return self.tbl_obj.select()

	def _get_rows_single_search_regular(self, **kw):
		self.s_field = s_field = kw['search_field']
		self.s_value = s_value = kw[s_field]
		s_table = self.tbl_obj
		if self.fields.has_key(s_field) and self.fields[s_field].has_key('type'):
			if s_field in s_table._columnDict.keys():
				rows = self._get_query_results(
						getattr(s_table.q, s_field)==s_value,
					)
			elif s_field+'ID' in s_table._columnDict.keys():
				if self.fields[s_field]['type'] == 'select':
					for entry in self.fields[s_field]['options']:
						if s_value and int(s_value) == entry.id:
							self.s_value = entry
				elif self.fields[s_field]['type'] == 'foreign_text':
					exec("results = self.fields[s_field]['table'].selectBy(%s=kw[s_field])" % self.fields[s_field]['column'])
					s_value = None
					for result in results:
						s_value = result.id
						break
				else:
					self.s_value = int(self.s_value)
				rows = self._get_query_results(
						getattr(s_table.q, s_field+'ID')==s_value,
					)
		elif '.' in s_field:
		# for foreign keys or foreign keys on foreign keys, go over each one and add each table to the queries (where clause)
			k = s_field
			queries = []
			k_cols = k.split('.')
			k_tabs = self.fields[k]['tables']
			exec('queries.append(self.tbl_obj.q.%sID==k_tabs[0].q.id)' % (k_cols[0]))
			for cnt in range(0, len(k_tabs)):
				if cnt < len(k_tabs)-1:
					exec('queries.append(k_tabs[cnt].q.%sID==k_tabs[cnt+1].q.id)' % (k_cols[cnt+1]))
				else:
					exec('queries.append(k_tabs[cnt].q.%s=="%s")' % (k_cols[cnt+1], kw[k]))
			rows = self._get_query_results(*queries)
		else:
			rows = self._get_query_results(
					getattr(s_table.q, s_field)==s_value,
				)
		return rows

	def _get_rows_single_search_range(self, **kw):
		self.s_field = s_field = kw['search_field']
		s_value_first = kw[kw['search_field']+'_first']
		s_value_last = kw[kw['search_field']+'_last']
		self.s_value = (s_value_first, s_value_last)
		s_table = self.tbl_obj
		rows = self._get_query_results(
				getattr(s_table.q, s_field)>=s_value_first,
				getattr(s_table.q, s_field)<=s_value_last,
			)
		return rows

	def _get_rows_detailed_search(self, **kw):
		self.s_field = s_field = ''
		self.s_value = s_value = ''
		queries = []
		for k in self.search_fields:
			if k in kw.keys() and kw[k]:
				try:
					exec('queries.append(self.tbl_obj.q.%s=="%s")' % (k, kw[k]))
				except KeyError:
					if self.fields[k].get('type', '') == 'foreign_text':
						exec("results = self.fields[k]['table'].selectBy(%s=kw[k])" % self.fields[k]['column'])
						s_value = None
						for result in results:
							s_value = result.id
							break
						exec('queries.append(self.tbl_obj.q.%sID==%s)' % (k, s_value))
					elif '.' in k:
						# for foreign keys or foreign keys on foreign keys, go over each one and add each table to the queries (where clause)
						k_cols = k.split('.')
						k_tabs = self.fields[k]['tables']
						exec('queries.append(self.tbl_obj.q.%sID==k_tabs[0].q.id)' % (k_cols[0]))
						for cnt in range(0, len(k_tabs)):
							if cnt < len(k_tabs)-1:
								exec('queries.append(k_tabs[cnt].q.%sID==k_tabs[cnt+1].q.id)' % (k_cols[cnt+1]))
							else:
								exec('queries.append(k_tabs[cnt].q.%s=="%s")' % (k_cols[cnt+1], kw[k]))
					else:
						exec('queries.append(self.tbl_obj.q.%sID==%s)' % (k, kw[k]))
				if not self.fields.has_key(k):
					self.fields[k] = {}
				self.fields[k]['value'] = kw[k]
			elif '%s_first' % k in kw.keys() and kw['%s_first' % k]:
				print '-'*64
				print 'k', kw['%s_first' % k], ': k', kw['%s_last' % k]
				print '-'*64
				exec('queries.append(self.tbl_obj.q.%s>="%s")' % (k, kw[k+'_first']))
				exec('queries.append(self.tbl_obj.q.%s<="%s")' % (k, kw[k+'_last']))
				if not self.fields.has_key(k):
					self.fields[k] = {}
				self.fields[k]['value'] = kw[k+'_first']
		print queries
		rows = self._get_query_results(
				*queries
			)
		return rows

	def _get_rows(self, **kw):
		if 'search_field' in kw and kw['search_field'] in kw:
			rows = self._get_rows_single_search_regular(**kw)
		elif 'search_field' in kw and kw['search_field']+'_last' in kw:
			rows = self._get_rows_single_search_range(**kw)
		elif kw.has_key('search'):
			rows = self._get_rows_detailed_search(**kw)
		else:
			self.s_field = s_field = ''
			self.s_value = s_value = ''
			rows = self._get_query_results()
		return rows

	def _item(self, id, **kw):
		page_dict = {}
		if id:
			item_dict = self._edit(id)
		else:
			item_dict = self._new(**kw)
		list_dict = self._list(**kw)
		for k,v in list_dict.items():
			page_dict[k] = v
		for k,v in item_dict.items():
			page_dict[k] = v
		return dict(
				actions = self.actions,
				columns = self.column_fields,
				details = self.detail_fields,
				entry_details = self.entry_details,
				fields = self.fields,
				hidden_fields = self.hidden_fields,
				id = item_dict['id'],
				item_details = self.item_details,
				max_row = page_dict['max_row'],
				new = item_dict['new'],
				page = page_dict['page'],
				rows = page_dict['rows'],
				row_cnt = page_dict['row_cnt'],
				search_field = page_dict['search_field'],
				search_value = page_dict['search_value'],
				searches = self.search_fields,
				show = page_dict['show'],
				title = self.__class__.__name__,
			)
	_item.__doc__ = ''

	def _list(self, page=1, show=10, sort_page_by=None, **kw):
		show = int(show)
		page = int(page)
		cherrypy.session['page'] = page
		row_start = (page-1)*show
		row_end = (page)*show
		try: self.tbl_obj.createTable()
		except: pass
		#for field in self.detail_fields:
		#	self.fix_field(field)
		#for field in self.column_fields:
		#	self.fix_field(field)
		rows = self._get_rows(**kw)
		try:
			max_row = len(list(rows))
		except validators.Invalid:
			max_row = 0
		rows = rows[row_start:row_end]
		if sort_page_by:
			rows = sort_page_rows(rows, sort_page_by)
		try:
			row_cnt = len([row for row in rows])
		except TypeError:
			row_cnt = 0
		except validators.Invalid:
			row_cnt = 0
		return dict(
				columns = self.column_fields,
				details = self.detail_fields,
				entry_details = self.entry_details,
				fields = self.fields,
				item_details = self.item_details,
				max_row = max_row,
				page = page,
				rows = rows,
				row_cnt = row_cnt,
				search_field = self.s_field,
				search_value = self.s_value,
				show = show,
				title = self.__class__.__name__,
				#title = str(cherrypy.session)
			)
	_list.__doc__ = ''

	def _mass_delete(self, select):
		#from basemodel import hub
		#hub.begin()
		for id in select:
			if int(id) > 0:
				self._delete_item(id)
		#hub.commit()
		#hub.end()
		turbogears.flash("Successfully deleted entry") 
		raise cherrypy.HTTPRedirect(turbogears.url(
				'index?page=%s' % cherrypy.session['page']
			))
	_mass_delete.__doc__ = ''

	def _mass_update(self, action, **kw):
		url = 'mass_%s?' % (action.lower())
		for k,values in kw.items():
			if type(values) is str:
				url += '%s=%s&' % (k, values)
			else:
				for v in values:
					url += '%s=%s&' % (k, v)
		raise cherrypy.HTTPRedirect(turbogears.url(url))
	_mass_update.__doc__ = ''

	def _new(self, **kw):
		for field in self.hidden_fields:
			if field in kw:
				if field not in self.fields:
					self.fields[field] = {}
				self.fields[field]['value'] = kw[field]
		for name in self.search_fields:
			self.fix_field(name, value='')
			field = self.fields[name]
			if not field.has_key('value') and field['type'] != 'hidden':
				self.fields[name]['value'] = ''
			if field.has_key('code'):
				self.fields[name]['value'] = self.generate_code(name, field['code']['prefix'], field['code']['reset'])
			if field.has_key('default'):
				self.fields[name]['value'] = field['default']
		for name in self.detail_fields:
			self.fix_field(name, value='')
			field = self.fields[name]
			if not field.has_key('value') and field['type'] != 'hidden':
				self.fields[name]['value'] = ''
			if field.has_key('code'):
				self.fields[name]['value'] = self.generate_code(name, field['code']['prefix'], field['code']['reset'])
			if field.has_key('default'):
				self.fields[name]['value'] = field['default']
		return dict(
				title = 'New %s' % self.__class__.__name__,
				details = self.detail_fields,
				fields = self.fields,
				id = '',
				new = True,
				db = self.tbl_obj,
			)
	_new.__doc__ = ''

	def _save(self, id=None, new=False, submit=None, **kw):
		#self.model.hub.begin()
		kw = self.validate(**kw)
		if new == 'True':
			if hasattr(self.tbl_obj, 'deleted'):
				entry = self.tbl_obj(deleted=False, **kw)
			else:
				entry = self.tbl_obj(**kw)
		else:
			entry = self.tbl_obj.get(id)
			for k,v in kw.items():
				setattr(entry, k, v)
		return entry.id
		#self.model.hub.commit()
		#self.model.hub.end()
 		turbogears.flash("Changes saved!") 
	_save.__doc__ = ''

	def _search(self, **kw):
		page_dict = {}
		item_dict = self._new(**kw)
		list_dict = self._list(**kw)
		for k,v in list_dict.items():
			page_dict[k] = v
		for k,v in item_dict.items():
			page_dict[k] = v
		return dict(
				actions = self.actions,
				columns = self.column_fields,
				details = self.detail_fields,
				entry_details = self.entry_details,
				fields = self.fields,
				id = item_dict['id'],
				item_details = self.item_details,
				max_row = page_dict['max_row'],
				new = item_dict['new'],
				page = page_dict['page'],
				rows = page_dict['rows'],
				row_cnt = page_dict['row_cnt'],
				searches = self.search_fields,
				search_field = page_dict['search_field'],
				search_value = page_dict['search_value'],
				show = page_dict['show'],
				title = self.__class__.__name__,
				#title = str(cherrypy.session)
			)
	_search.__doc__ = ''

	def _validate(self, **kw):
		for k,v in kw.items():
			if self.fields.has_key(k):
				if self.fields[k].has_key('type'):
					col_type = self.fields[k]['type']
					if col_type == 'bool' or col_type == bool:
						if kw.has_key(k) and v == 'True':
							kw[k] = True
						else:
							kw[k] = False
					elif col_type == 'int' or col_type == int:
						try:
							kw[k] = int(v)
						except ValueError:
							kw[k] = None
					elif col_type == 'float' or col_type == float:
						try:
							kw[k] = float(v)
						except ValueError:
							kw[k] = None
					elif col_type == 'password':
						if v == kw['verify_%s'%k] and len(v) > 1:
							kw[k] = crypt.crypt(v, get_salt())
						else:
							del kw[k]
						del kw['verify_%s' % k]
					elif col_type == 'datetime':
						if kw[k] == '':
							kw[k] = None
						else:
							c_date,c_time = v.split(' ')
							year,mon,day = c_date.split('-')
							hour,min,sec = c_time.split(':')
							kw[k] = datetime.datetime(
									int(year),
									int(mon),
									int(day), 
									int(hour),
									int(min),
									int(sec),
								)
					elif col_type == 'date':
						if kw[k] == '':
							kw[k] = None
					elif col_type == 'time':
						if kw[k] == '':
							kw[k] = None
						else:
							hour,min,sec = v.split(':')
							kw[k] = datetime.datetime(
									Now().year,
									Now().month,
									Now().day, 
									int(hour),
									int(min),
									int(sec),
								)
					elif col_type == 'select':
						if kw[k] == '':
							kw[k] = None
					elif col_type == 'foreign_text':
						if kw[k]:
							kw[k] = kw[k].replace(' ', '')
							exec("results = self.fields[k]['table'].selectBy(%s=kw[k])" % self.fields[k]['column'])
							kw[k] = None
							kw[k+'ID'] = None
							for result in results:
								kw[k] = result.id
								kw[k+'ID'] = result.id
								break
						else:
							kw[k] = None
					else:
						kw[k] = v
				else:
					try:
						col_type = str(self.tbl_obj._columnDict[k])
					except KeyError:
						col_type = 'select'
					if re.search('Bool', col_type):
						kw[k] = bool(v)
					elif re.search('Int', col_type):
						kw[k] = int(v)
					elif re.search('Float', col_type):
						kw[k] = float(v)
			else:
				try:
					col_type = str(self.tbl_obj._columnDict[k])
					if re.search('Bool', col_type):
						kw[k] = bool(v)
					elif re.search('Int', col_type):
						kw[k] = int(v)
					elif re.search('Float', col_type):
						kw[k] = float(v)
				except KeyError:
					pass
				except ValueError:
					pass
					#kw[k] = 0
		return kw
	_validate.__doc__ = ''

	def _validation_error(self, funcname, kw, errors):
		return dict(
				tg_template='templates.error',
				error='Invalid Argument',
			)
	_validation_error.__doc__ = ''

	def auth(self, function, **kw):
		class_name = self.__class__.__name__
		pass
	auth.__doc__ = '''Check if the user is authorized to access the current page.'''

	@turbogears.expose(template='templates.blank')
	def delete(self, **kw):
		self.auth('delete')
		return self._delete(**kw)
	delete.__doc__ = '''Delete an item with a specific id.'''

	@turbogears.expose(template='templates.blank')
	def details(self, id, **kw):
		self.auth('details')
		return self._details(id, **kw)
	details.__doc__ = '''
		TODO: Show the details of an entry with a given id.'''

	@turbogears.expose(template='templates.edit')
	def edit(self, id):
		self.auth('edit')
		return self._item(id)
	edit.__doc__ = '''
		Show a page to edit an item with a specific id.'''

	@turbogears.expose(template='templates.error')
	def error(self,msg):
		return dict(msg=msg)

	def fix_field(self, name, description=None, value=None, **kw):
		return self._fix_field(name, description, value, **kw)
	fix_field.__doc__ = '''
		Make sure all the necessary values in the fields[name]
		dictionary is defined.'''

	def generate_code(self, field, pre, reset=None):
		if reset == 'yearly':
			period = Now().strftime('%Y')
		elif reset == 'monthly':
			period = Now().strftime('%Y%m')
		else:
			period = ''
		prefix = '%s%s' % (pre, period)
		tbl = self.tbl_obj
		if hasattr(self.tbl_obj.q, 'deleted'):
			code = tbl.select(tbl.q.deleted==False).max(field)
		else:
			code = tbl.select().max(field)
		if code and re.search(prefix, code):
			count = get_count(code)+1
		else:
			count = 1
		code = '%s-%04i' % (prefix, count)
		code = re.sub('^-', '', code)
		self.fields[field]['value'] = code
		return code

#	@turbogears.expose(template='templates.blank')
#	def index(self):
#		return self._index()
#	index.__doc__ = '''
#		This method authenticates the user. If it's a valid
#		user, it redirects to the list.'''

	@turbogears.expose(template='templates.item')
	def item(self, id=None, **kw):
		self.auth('item')
		return self._item(id, **kw)
	item.__doc__ = ''''''

	@turbogears.expose()
	def login(self, **kw):
		return '''<form>
		Username: <input name="user" />
		Password: <input name="password" type="password" />
		</form>'''
	login.__doc__ = '''Display a login page.'''

	@turbogears.expose(template='templates.list')
	def list(self, **kw):
		self.auth('list')
		return self._item(id=None, **kw)
	list.__doc__ = '''
		List items on the table.'''

	@turbogears.expose(template='templates.list_noed_nodel')
	def list_noed_nodel(self, id=None, **kw):
		self.auth('list')
		return self._item(id, **kw)
	list_noed_nodel.__doc__ = '''
		List items on the table without allowing users to edit and delete the entries.'''

	@turbogears.expose()
	def mass_delete(self, select):
		self.auth('delete')
		return self._mass_delete(select)
	mass_delete.__doc__ = '''
		Delete several items selected from a list.'''

	@turbogears.expose()
	def mass_update(self, action, **kw):
		return self._mass_update(action, **kw)
	mass_update.__doc__ = '''
		Update several items selected from a list.'''

	@turbogears.expose(template='templates.edit')
	def new(self, id=None, **kw):
		self.auth('new')
		return self._item(id, **kw)
	new.__doc__ = '''
		Show a form asking for details on a new item.'''

	@turbogears.expose()
	def save(self, id=None, new=False, submit=None, **kw):
		self.auth('save')
		result = self._save(id, new, submit, **kw)
		if not cherrypy.session.has_key('page'):
			cherrypy.session['page'] = 1
		raise cherrypy.HTTPRedirect(turbogears.url(
				'index?page=%s' % cherrypy.session['page']
			))
		return result
	save.__doc__ = '''
		Save an item with a specific id.'''

	@turbogears.expose(template='templates.search_noed_nodel')
	def search(self, **kw):
		self.auth('list')
		return self._search(**kw)
	search.__doc__ = '''
		Show a form asking for details on a new item.'''

	def validate(self, **kw):
		return self._validate(**kw)
	validate.__doc__ = '''
		Validate the inputs given before saving an entry.'''

	@turbogears.expose(template='templates.blank')
	def validation_error(self, funcname, kw, errors):
		return self._validation_error(funcname, kw, errors)
	validation_error.__doc__ = '''
		Show a validation error page when an invalid value is
		given.'''

	def _delete(self, **kw):
		return dict(
			)
	delete.__doc__ = '''
		Delete an item with a specific id.'''

	index = item


class BusyBeObject(SQLObject):
	'''This class stands as the default DB table for BusyBe.
	'''
	deleted = BoolCol(default=False)

