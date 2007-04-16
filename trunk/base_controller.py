import logging

import cherrypy
from cherrypy import request, response

import turbogears
from turbogears import controllers, expose, validate, redirect, flash

import model
import re
from conf import pkg, template_dir, theme
import datetime
from MySQLdb.connections import OperationalError, IntegrityError
import sqlobject
from sqlobject import SQLObjectNotFound 
from sqlobject.sqlbuilder import AND,OR,NOT,LEFTJOINOn
exec('from %s import json' % pkg)
import crypt, random


Now = datetime.datetime.now

log = logging.getLogger("%s.controllers" % pkg)


def _dbg(*msg):
	print '----'
	import os
	a = os.system('/bin/date')
	try:
		print msg
	except:
		print str(msg)
	print '----'

def _get_temp(tmp):
	return '%s.%s.%s' % (pkg, template_dir, tmp)

def beautify(text):
	'''Capitalize the first letter of each word.
	'''
	old_text = text
	text = ''
	for char in old_text:
		if re.match('[A-Z]', char):
			text += ' '
		text += char
	text = re.sub('  ', ' ', text)
	text = re.sub('^ ', '', text)
	text = ' '.join(text.split('_'))
	text = ' '.join(text.split('.'))
	words = (word.capitalize() for word in text.split(' '))
	text = ' '.join(words)
	return text

def get_dict(orig, dest={}):
	'''Copy the contents of the orig dict to the dest dict.
	Create a new dest dict if it doesn't exist.
	'''
	for k, v in orig.iteritems():
		dest[k] = v
	return dest

def get_salt(chars=None):
	'''Get two random letter/number to be used for the crypt.
	'''
	if not chars:
		import string
		chars = string.letters + string.digits
	return random.choice(chars) + random.choice(chars)

def hard_restart():
	'''Kill all python processes to spawn a new one.
	'''
	from subprocess import Popen, PIPE
	p = Popen('/usr/bin/killall python', shell=True, stdout=PIPE, stderr=PIPE)

def soft_restart():
	'''Reload the project by touch'ing the controllers.
	'''
	from subprocess import Popen, PIPE
	p = Popen('touch megarc/controllers.py', shell=True, stdout=PIPE, stderr=PIPE)


class AuthTables(object):
	pass


class Auth(controllers.Root):
	auth_dict = {}

	def _get_template(self, tmp):
		return '%s.%s.%s' % (pkg, template_dir, tmp)

	def _set_auth_tables(self):
		pass

	def _auth(self, function):
		return True # remove comment to disable authentication
		self.set_auth_attr()
		class_name = self.__class__.__name__
		if cherrypy.session.has_key('user'):
			username = cherrypy.session['user']
		else:
			return 0
		user = self.auth_dict['user'].byUser(username)
		access_level = user.access_level
		user_group = user.user_group
		permissions = self.auth_dict['permission'].selectBy(
				access_level = access_level,
				#user_group = user_group,
				class_name = class_name,
				function = function,
			)
		if access_level.access_level == 'admin':
			return True
		authorized = False
		for permission in permissions:
			if permission.access_level == access_level:
				authorized = True
				break
		if authorized:
			return True
		else:
			return 'Access not allowed for class %s action %s.' % (
					class_name,
					function,
				)

	def set_auth_attr(self):
		self._set_auth_tables()
		for tbl in ('user', 'access_level', 'user_group', 'permission'):
			if not self.auth_dict.has_key(tbl):
				class_name = beautify(tbl).replace(' ', '')
				model_class = getattr(model, class_name)
				self.auth_dict[tbl] = model_class

	def auth(self, function='menu'):
		'''Find out if the user is authorized to do the given action.'''
		#return True # Comment out to disable authentication
		authorized = self._auth(function)
		if authorized == True:
			return True
		elif authorized == False:
			raise cherrypy.HTTPRedirect(turbogears.url('/login'))
		else:
			redirect('error?msg=%s' % authorized)
		redirect('error?msg=%s' % 'An Error occurred while logging in.')

	@turbogears.expose(_get_temp('login'))
	def login(self, **kw):
		title = 'Login'
		head = 'Login'
		return dict(
				head = head,
				session = dict(cherrypy.session),
				title = title,
				template_dir = template_dir,
				theme = theme,
				#tg_template = str(self._get_template('login')),
			)
	login.__doc__ = '''Display a login page.'''

	@turbogears.expose()
	def logout(self, **kw):
		if cherrypy.session.has_key('user'):
			del cherrypy.session['user']
		raise cherrypy.HTTPRedirect(turbogears.url('/'))

	@turbogears.expose()
	def signin(self, user, password):
		username = user
		try:
			user = model.User.byUser(user)
		except SQLObjectNotFound:
			flash('Invalid username/password.')
			redirect('/login')
		good = False
		salt = user.password[0] + user.password[1]
		passwd = crypt.crypt(password, salt)
		if user.password == passwd:
			cherrypy.session['user'] = username
			redirect(turbogears.url('.'))
		else:
			flash('Invalid username/password.')
			redirect('/login')


class Menu(Auth):
	exclude = [
			'accesslog',
			'error',
			'exclude',
			'index',
			'is_app_root',
			'login',
			'logout',
			'msglog',
			'msglogfunc',
			'module',
			'modules',
			'signin',
			'title',
		]

	def _get_labels(self, modules):
		labels = []
		for module in modules:
			try:
				mod = getattr(self, module)
				mod._common()
				labels.append(mod.title)
			except AttributeError:
				labels.append(beautify(module))
		return labels

	def _get_modules(self):
		mod_list = dir(self.__class__)
		modules = [attr for attr in mod_list if attr not in self.exclude and attr != 'get_modules' and not re.match('^_', attr)]
		tmp = list(modules)
		for mod in tmp:
			if getattr(self, mod)._auth('list') != True:
				modules.remove(mod)
		return list(modules)

	def _set_excludes(self):
		excludes = (
				'auth', 
				'auth_dict',
				'set_auth_attr',
			)
		for exclude in excludes:
			if exclude not in self.exclude:
				self.exclude.append(exclude)

	@expose(_get_temp('error'))
	def error(self, msg):
		return dict(
				head='Error',
				msg=msg,
				session = dict(cherrypy.session),
				title = 'Error',
				#tg_template = str(self._get_template('error')),
			)

	@expose('json')
	@expose(_get_temp('menu'))
	def index(self):
		self.auth('menu')
		import time
		now = time.ctime()
		self._set_excludes()
		try:
			head = self.head
		except AttributeError:
			head = beautify(re.sub('.*\.', '', self.__class__.__module__))
		try:
			title = self.title
		except AttributeError:
			self.head
		modules = self._get_modules()
		labels = self._get_labels(modules)
		return dict(
				head = head,
				labels = labels,
				modules = modules,
				session = dict(cherrypy.session),
				title = title,
				template_dir = template_dir,
				theme = theme,
				#tg_template = str(self._get_template('menu')),
			)


class Base(Auth):
	show = 3
	page = 1

	def _init_(self):
		pass

	def _action(self, action, **kw):
		self._common()
		try:
			function = getattr(self, action.lower())
			if function.exposed == True:
				return function(**kw)
			else:
				redirect('error?msg=The action "%s" is not allowed. Please report this to the programmer.' % action)
		except KeyError:
			redirect('error?msg=Action "%s" not recognize. Please report this to the programmer.' % action)

	def _common(self):
		self._init_()
		page_dict = get_dict(self._get_page_dict())
		try:
			title = self.title
		except AttributeError:
			title = re.sub('.*\.', '', self.__class__.__name__)
		page_dict['title'] = beautify(title)
		page_dict['head'] = page_dict['title']
		#page_dict['beautify'] = beautify
		page_dict['session'] = dict(cherrypy.session)
		page_dict['template_dir'] = template_dir
		page_dict['theme'] = theme
		return page_dict

	def _delete(self, id, tbl=None, **kw):
		page_dict = self._common()
		id = int(id)
		if not tbl:
			tbl = self.tbl
		row = tbl.get(id)
		if hasattr(self, 'mtm_tbl') and hasattr(self, 'mtm_col') and self.mtm_tbl != tbl:
			mtm_rows = self.mtm_tbl.select(
					getattr(self.mtm_tbl.q, '%sID' % self.mtm_col) == id
				)
			for mtm_row in mtm_rows:
				self._delete(mtm_row.id, self.mtm_tbl)
		if hasattr(row, 'deleted'):
			row.deleted = True
			#col_dict = tbl._columnDict
			col_dict = tbl.sqlmeta.columns
			for field, col in col_dict.iteritems():
				if col.unique:
					setattr(row, field, '%s\b%s' % (id, getattr(row, field)))
		else:
			tbl.delete(id)

	def _details(self, id, **kw):
		page_dict = self._common()
		page_dict['values'] = self._get_details_values(id, **kw)
		page_dict['entry_id'] = id
		return page_dict

	def _edit(self, id=None, **kw):
		page_dict = self._common()
		page_dict['values'] = self._get_edit_values(id, **kw)
		page_dict['entry_id'] = id
		return page_dict

	def _get_field_details(self, field):
		detail = self.fields[field]
		if not detail.has_key('description'):
			detail['description'] = beautify(field)
		if not detail.has_key('type'):
			detail['type'] = self._get_field_type(field)
			detail['col_type'] = self._get_db_col_type(field) #debug
		if not detail.has_key('required'):
			detail['required'] = self._get_field_required(field)
		if not detail.has_key('length'):
			try:
				detail['length'] = self.col_dict[field].length
			except AttributeError:
				detail['length'] = 0
		detail = self._get_field_details_typed(detail)
		self.fields[field] = detail

	def _get_field_details_typed(self, detail):
		col_type = detail['type']
		if col_type == list:
			detail = self._get_field_details_type_list(detail)
		return detail

	def _get_field_details_type_list(self, detail):
		if not detail.has_key('table'):
			detail['table'] = detail['col_type'].foreignKey
		tbl = getattr(model, detail['table'])
		if not detail.has_key('column'):
			# If no column is defined, get the fist unique column we can find
			#col_dict = tbl._columnDict
			col_dict = tbl.sqlmeta.columns
			for k, v in col_dict.iteritems():
				if v.unique:
					detail['column'] = k
					break
			# Make sure we have a value
			if not detail.has_key('column'):
				for k, v in col_dict.iteritems():
					detail['column'] = k
					break
		if detail.has_key('options'):
			# Let go of the previous options
			del detail['options']
		if detail.has_key('default_options'):
			detail['options'] = detail['default_options']
		else:
			# Get the options from a column of all the contents of the given table
			detail['options'] = self._get_rows(
					tbl,
					[detail['column']],
				)
			if detail.has_key('format'):
				for key, opt in detail['options'].iteritems():
					i = j = k = key
					try:
						detail['options'][i][j][k][detail['column']] = detail['format'] % opt[j][k][detail['column']]
					except KeyError:
						try:
							detail['options'][i][j][k] = {}
							detail['options'][i][j][k][detail['column']] = detail['format'] % opt[j][k][detail['column']]
						except KeyError:
							try:
								detail['options'][i][j] = {}
								detail['options'][i][j][k] = {}
								detail['options'][i][j][k][detail['column']] = detail['format'] % opt[j][k][detail['column']]
							except KeyError:
								detail['options'][i] = {}
								detail['options'][i][j] = {}
								detail['options'][i][j][k] = {}
								detail['options'][i][j][k][detail['column']] = detail['format'] % opt[j][k][detail['column']]
		return detail

	def _get_field_required(self, field):
		return self.col_dict[field].notNone

	def _get_field_type(self, field):
		col_type = None
		try:
			db_type = str(self.col_dict[field])
		except KeyError:
			col_type = list
		if re.search('Bool', db_type):
			col_type = bool
		elif re.search('Int', db_type):
			col_type = int
		elif re.search('Float', db_type) or re.search('Currency', db_type) or re.search('Decimal', db_type):
			col_type = float
		elif re.search('Str', db_type):
			col_type = str
			if not self.col_dict[field].length:
				col_type = 'text'
		elif re.search('Unicode', db_type):
			col_type = unicode
			if not self.col_dict[field].length:
				col_type = 'text'
		elif re.search('DateTime', db_type):
			col_type = 'datetime'
		elif re.search('Time', db_type):
			col_type = 'time'
		elif re.search('Date', db_type):
			col_type = 'date'
		elif re.search('ForeignKey', db_type):
			col_type = list
		else:
			col_type = db_type
		return col_type

	def _get_db_col_type(self, field): #debug
		db_type = self.col_dict[field]
		#print field
		#_dbg(dir(db_type))
		#_dbg(db_type.default)
		#if self.fields[field]['type'] == 'datetime':
		#	_dbg(type(db_type.default))
		#if field == 'community':
		#	_dbg(dir(db_type))
		#	_dbg(type(db_type.foreignKey))
		#	_dbg(db_type.foreignName)
		#_dbg(db_type.notNone)
		return db_type

	def _get_page_details(self):
		'''Make sure the required details needed in the page are given
		'''
		page_dict = self._get_page_details_fields()
		page_dict['actions'] = self._get_page_details_actions()
		#page_dict['col_cnt'] = self._get_page_details_col_cnt()
		return page_dict

	def _get_page_details_actions(self):
		default_actions = (
				'add',
				'delete',
				'details',
				'edit',
				'list',
				'cancel',
				'new',
			)
		if hasattr(self, 'actions'):
			if type(self.actions) != list:
				self.actions = list(self.actions)
			for action in default_actions:
				if action not in self.actions:
					self.actions.append(action)
		else:
			self.actions = list(default_actions)
		tmp = list(self.actions)
		for action in tmp:
			if self._auth(action) != True:
				self.actions.remove(action)
		return self.actions

	def _get_page_details_fields(self):
		'''Make sure the required field details needed in the page are given.
		'''
		page_dict = {}
		self._set_col_dict()
		if not hasattr(self, 'default_fields'):
			self.default_fields = list(self.all_fields)
			try:
				self.default_fields.remove('deleted')
				self.default_fields.remove('date_entered')
			except ValueError:
				pass
		if not hasattr(self, 'fields'):
			self.fields = {}
			for k in self.all_fields:
				self.fields[k] = {}
		else:
			for k in self.all_fields:
				if not self.fields.has_key(k):
					self.fields[k] = {}
		page_dict['fields'] = self.fields
		page_attrs = (
				'column_fields',
				'detail_fields',
				'edit_fields',
				'search_fields',
				#'quick_search_fields',
				#'_fields',
			)
		for page_attr in page_attrs:
			if not hasattr(self, page_attr):
				setattr(self, page_attr, list(self.default_fields))
		for k in self.default_fields:
			if self.fields[k].has_key('type'):
				col_type = self.fields[k]['type']
				if col_type == 'passwd':
					if type(self.detail_fields) != list:
						self.detail_fields = list(self.detail_fields)
					try:
						self.detail_fields.remove(k)
					except ValueError:
						pass
				if col_type in ('passwd', 'text'):
					if type(self.column_fields) != list:
						self.column_fields = list(self.column_fields)
					try:
						self.column_fields.remove(k)
					except ValueError:
						pass
		for page_attr in page_attrs:
			page_dict[page_attr] = getattr(self, page_attr)
		if hasattr(self, 'hidden_fields'):
			# Make sure the fields in hidden_fields are not in edit_fields and vice-versa
			for field in self.hidden_fields:
				if field in self.edit_fields:
					self.edit_fields.remove(field)
		else:
			# Make sure there's a hidden_fields attribute
			self.hidden_fields = []
		page_dict['hidden_fields'] = self.hidden_fields
		return page_dict

	def _get_page_dict(self):
		page_dict = {}
		page_dict = self._get_page_details()
		for field in self.fields:
			self._get_field_details(field)
		page_dict = self._get_page_details()
		return page_dict

	def _get_details_value(self, field, row, **kw):
		value = getattr(row, field)
		detail = self.fields[field]
		if detail['type'] == list or detail['type'] == 'foreign_text':
			value = detail['options'][value.id][value.id][value.id][detail['column']]
			#try:
			#	column = detail['column']
			#	if type(column) == tuple:
			#		values = []
			#	else:
			#		value = getattr(value, column)
			#except AttributeError:
			#	value = None
		if type(value) == str or type(value) == unicode:
			(value, sub_cnt) = re.subn('[0-9]*\b', '', value)
			if sub_cnt:
				value = value + ' (deleted)'
		return value

	def _get_details_values(self, id, **kw):
		values = {}
		row = self.tbl.get(id)
		for field in self.all_fields:
			values[field] = self._get_details_value(field, row, **kw)
		return values

	def _get_edit_value(self, field, row, **kw):
		if kw.has_key(field):
			value = self._get_edit_value_given(field, kw[field])
		elif row:
			value = self._get_edit_value_db(field, row)
		else:
			value = self._get_edit_value_default(field)
		return value

	def _get_edit_value_db(self, field, row):
		try:
			value = getattr(row, field)
		except SQLObjectNotFound:
			value = None
		# Change the value according to col_type
		detail = self.fields[field]
		value = self._get_edit_value_typed(value, detail)
		return value

	def _get_edit_value_default(self, field):
		detail = self.fields[field]
		try:
			value = detail['default']
		except KeyError:
			try:
				default = self.col_dict[field].default
				if not default == sqlobject.sqlbuilder.NoDefault:
					value = default
				else:
					value = None
			except AttributeError:
				value = None
		if detail['type'] == bool and (type(value) == unicode or type(value) == str):
			if value == 'False':
				value = False
			else:
				value = True
		elif detail['type'] == 'datetime':
			pass
		return value

	def _get_edit_value_given(self, field, value):
		#TODO: Check if the given value is valid
		detail = self.fields[field]
		value = self._get_edit_value_typed(value, detail)
		return value

	def _get_edit_value_typed(self, value, detail):
		col_type = detail['type']
		if col_type == list:
			try:
				value = value.id
			except AttributeError:
				try:
					value = int(value)
				except ValueError:
					value = None
				except TypeError:
					value = None
		elif col_type == 'foreign_text':
			try:
				value = getattr(value, detail['column'])
			except AttributeError:
				value = None
		elif col_type == 'passwd':
			value = None
		elif col_type == bool:
			if not value:
				value = False
			elif value == 'False':
				value = False
			else:
				value = True
		return value

	def _get_edit_values(self, id, **kw):
		values = {}
		if id:
			row = self.tbl.get(id)
		else:
			row = None
		for field in self.all_fields:
			values[field] = self._get_edit_value(field, row, **kw)
		return values

	def _get_row_value(self, row, field):
		#TODO: Change the value according to the col_type
		try:
			field_detail = self.fields[field]
		except KeyError:
			field_detail = {}
		try:
			if type(field) == tuple:
				values = []
				for f in field:
					values.append(getattr(row, f))
				#value = ', '.join(str(v) for v in values)
				value = tuple(values)
			else:
				value = getattr(row, field)
		except AttributeError:
			value = getattr(row, field+'ID')
		except SQLObjectNotFound:
			value = None
		if field_detail.has_key('type') and field_detail['type'] == list:
			column = field_detail['column']
			if type(column) == tuple:
				values = []
				for f in column:
					values.append(getattr(value, f))
				if field_detail.has_key('format'):
					value = field_detail['format'] % tuple(values)
				else:
					value = ', '.join(str(v) for v in values)
			else:
				value = getattr(value, column, value)
		if type(value) == str or type(value) == unicode:
			(value, sub_cnt) = re.subn('[0-9]*\b', '', value)
			if sub_cnt:
				value = value + ' (deleted)'
		return value

	def _get_rows(self, tbl, fields, where_and=[], where_or=[], **kw):
		if not tbl:
			tbl = self.tbl
		if not fields:
			fields = self.default_fields
		rows_obj = self._get_rows_query(tbl, where_and, where_or, **kw)
		rows = self._get_rows_to_dict(rows_obj, tbl, fields, **kw)
		return rows

	def _get_rows_to_dict(self, rows_obj, tbl, fields, **kw):
		if kw.has_key('page') and kw.has_key('show'):
			first_row = (kw['page']-1) * kw['show']
			last_row = ( (kw['page']) * kw['show'] )
			self.page_dict['max_row'] = rows_obj.count()
			self.page_dict['first_row'] = first_row
			self.page_dict['last_row'] = last_row
			rows_obj = rows_obj[first_row:last_row]
		# Get Rows from the DB and put it in a dictionary
		tmp_rows_dict = {}
		rows_dict = {}
		for row in rows_obj:
			key = row.id
			tmp_rows_dict[key] = {}
			tmp_rows_dict[key]['id'] = row.id
			for field in fields:
				tmp_rows_dict[key][field] = self._get_row_value(row, field)
		# Sort the page by the field given
		if not kw.has_key('sort_page_by') or kw['sort_page_by'] == 'id':
			for id, row in tmp_rows_dict.iteritems():
				try:
					rows_dict[id][id][id] = row
				except KeyError:
					try:
						rows_dict[id][id] = {}
						rows_dict[id][id][id] = row
					except KeyError:
						rows_dict[id] = {}
						rows_dict[id][id] = {}
						rows_dict[id][id][id] = row
		else:
			for id, row in tmp_rows_dict.iteritems():
				sort_page = row[kw['sort_page_by']]
				try: sort_page = sort_page.lower()
				except AttributeError: pass
				sort_rows = row[kw['sort_result_by']]
				try: sort_rows = sort_rows.lower()
				except AttributeError: pass
				key = (sort_page, sort_rows, id)
				#rows_dict[key] = row
				try:
					rows_dict[sort_page][sort_rows][id] = row
				except KeyError:
					try:
						rows_dict[sort_page][sort_rows] = {}
						rows_dict[sort_page][sort_rows][id] = row
					except KeyError:
						rows_dict[sort_page] = {}
						rows_dict[sort_page][sort_rows] = {}
						rows_dict[sort_page][sort_rows][id] = row
		return rows_dict

	def _get_rows_query(self, tbl, where_and=[], where_or=[], **kw):
		select_args = {}
		select_args['orderBy'] = self._get_rows_query_sort_by(tbl, **kw)
		if kw.has_key('search_field') and kw['search_field'] != '':
			# Quick search
			[where_and, where_or] = self._get_rows_query_quick_search(tbl, where_and, where_or, kw['search_field'], kw['search_value'])
		elif kw.has_key('search') and kw['search'] == 'Search':
			# Detailed search
			[where_and, where_or] = self._get_rows_query_detailed_search(tbl, where_and, where_or, **kw)
		select_args['clause'] = self._get_rows_query_clause(tbl, where_and, where_or)
		try:
			rows = tbl.select(**select_args)
		except AttributeError:
			rows = tbl.select()
		rows = self._get_rows_query_reversed(rows, **kw)
		return rows

	def _get_rows_query_clause(self, tbl, where_and, where_or):
		if hasattr(tbl.q, 'deleted'):
			where_and.append(
					tbl.q.deleted == False,
				)
		if len(where_or) > 0:
			clause = AND(
					OR(*where_or),
					*where_and
				)
		elif len(where_and) > 0:
			clause = AND(
					*where_and
				)
		else:
			clause = None
		return clause

	def _get_rows_query_detailed_search(self, tbl, where_and, where_or, **kw):
		for field in self.search_fields:
			if kw.has_key(field) and kw[field] != '':
				value = kw[field]
				[where_and, where_or] = self._get_rows_query_search_single(tbl, where_and, where_or, field, value)
		return [where_and, where_or]

	def _get_rows_query_quick_search(self, tbl, where_and, where_or, search_field, search_value):
		if search_value != '':
			return self._get_rows_query_search_single(tbl, where_and, where_or, search_field, search_value)
		else:
			return [where_and, where_or]

	def _get_rows_query_search_single(self, tbl, where_and, where_or, field, value):
		col_type = self.fields[field]['type']
		if col_type in (unicode, str, 'text'):
			value = str(value)
			where_and.append(getattr(tbl.q, field).contains(value))
		elif col_type in (int, float, 'date', 'datetime'):
			if col_type in (int, float):
				try:
					value[0] = col_type(value[0])
				except ValueError:
					value[0] = None
				try:
					value[1] = col_type(value[1])
				except ValueError:
					value[1] = None
			elif col_type in ('date', 'datetime'):
				value = [str(v) for v in value]
			if value[0]:
				where_and.append(getattr(tbl.q, field) >= value[0])
			if value[1]:
				where_and.append(getattr(tbl.q, field) <= value[1])
		elif col_type == bool:
			if value == True or re.search('True', value):
				value = True
			else:
				value = False
			where_and.append(getattr(tbl.q, field) == value)
		elif col_type in (list, ):
			try:
				value = int(value)
			except ValueError:
				value = None
			where_and.append(getattr(tbl.q, field+'ID') == value)
		elif col_type == 'passwd':
			self.search_fields.remove(field)
			self.column_fields.remove(field)
		else:
			value = str(value)
			where_and.append(getattr(tbl.q, field) == value)
		return [where_and, where_or]

	def _get_rows_query_reversed(self, rows, **kw):
		if kw.has_key('reversed_result') or not kw.has_key('sort_result_by'):
			try:
				self.page_dict['reversed_result'] = True
			except AttributeError:
				pass
			rows = rows.reversed()
		else:
			try:
				self.page_dict['reversed_result'] = False
			except AttributeError:
				pass
		return rows

	def _get_rows_query_sort_by(self, tbl, **kw):
		if not kw.has_key('sort_result_by'):
			sort_by = tbl.q.id
			try: self.page_dict['sort_result_by'] = 'id'
			except AttributeError: pass
		else:
			try:
				sort_by = getattr(tbl.q, kw['sort_result_by'])
			except AttributeError:
				sort_by = getattr(tbl.q, kw['sort_result_by']+'ID')
				# The plan is to sort by id at first, then sort by the value of the column -- this would be a db-intensive query tho.
				#sort_by = 'id'
				#kw['sort_result_by'] = kw['sort_result_by']+'ID'
			try: self.page_dict['sort_result_by'] = kw['sort_result_by']
			except AttributeError: pass
		return sort_by

	def _item(self, **kw):
		page_dict = get_dict(self._common())
		page_dict = get_dict(self._edit(), page_dict)
		page_dict = get_dict(self._list(), page_dict)
		return page_dict

	def _list(self, **kw):
		flash('')
		self.page_dict = self._common()
		kw = self._list_details(**kw)
		self.page_dict['rows'] = self._get_rows(tbl=self.tbl, fields=self.column_fields, where_and=[], where_or=[], **kw)
		return self.page_dict

	def _list_details(self, **kw):
		for key in ('show', 'page'):
			if kw.has_key(key):
				kw[key] = int(kw[key])
			elif hasattr(self, key):
				kw[key] = getattr(self, key)
			self.page_dict[key] = kw[key]
		if not kw.has_key('sort_page_by') or kw['sort_page_by'] == 'id':
			try:
				kw['sort_page_by'] = kw['sort_result_by']
			except KeyError:
				kw['sort_page_by'] = 'id'
				kw['reversed'] = True
			if not kw.has_key('reversed'):
				kw['sort_page_by'] = kw['sort_result_by']
				if kw.has_key('reversed_result'):
					kw['reversed'] = True
				else:
					kw['reversed'] = False
		self.page_dict['sort_page_by'] = kw['sort_page_by']
		if kw.has_key('reversed'):
			if kw['reversed'] == 'True' or kw['reversed'] == True:
				kw['reversed'] = True
			else:
				kw['reversed'] = False
		else:
			kw['reversed'] = False
		self.page_dict['reversed'] = kw['reversed']
		self.page_dict['search_values'] = {}
		if kw.has_key('search_field') and kw['search_field'] != '':
			# Quick Search
			field = str(kw['search_field'])
			try:
				kw['search_value'] = kw[field]
			except KeyError:
				kw['search_value'] = kw[field] = [kw[field+'_first'], kw[field+'_last']]
			self.page_dict['search_field'] = field
			self.page_dict['search_values'][field] = kw[field]
		elif kw.has_key('search') and kw['search'] == 'Search':
			# Detailed Search
			for field in self.search_fields:
				try:
					search_value = kw[field]
				except KeyError:
					try:
						search_value = kw[str(field)] = [kw[field+'_first'], kw[field+'_last']]
					except KeyError:
						search_value = kw[str(field)] = ''
				self.page_dict['search_values'][field] = search_value
		else:
			self.page_dict['search_field'] = ''
		return kw

	def _save(self, id, **kw):
		self._common()
		#TODO: Check the input
		kw = self._save_fix_values(**kw)
		try:
			if id:
				row = self._save_old(id, **kw)
			else:
				row = self._save_new(**kw)
			mtm = True
			for attr in ('mtm_rel_col', 'mtm_col', 'rel_col', 'mtm_tbl', 'rel_tbl',):
				if not hasattr(self, attr):
					mtm = False
					break
			if mtm==True:
				mtm_dict = {
						self.mtm_rel_col: getattr(row, '%sID' % self.rel_col),
						self.mtm_col: row.id,
					}
				rel = self.mtm_tbl.selectBy(**mtm_dict)
				if len(list(rel)) <= 0:
					self.mtm_tbl(deleted=False, **mtm_dict)
			return row
		except ValueError:
			redirect('error?msg=Invalid input.')

	def _save_fix_value(self, field, value):
		col_type = self.fields[field]['type']
		if col_type == list:
			value = int(value)
		elif col_type == bool:
			value = self._save_get_value_bool(value)
		elif col_type == 'datetime':
			value = self._save_get_value_datetime(value)
		elif col_type == 'passwd':
			value = self._save_get_value_passwd(value)
		elif col_type == 'time':
			value = self._save_get_value_time(value)
		elif type(col_type) == type:
			value = col_type(value)
		else:
			value = value
		return value

	def _save_fix_value_default(self, field, default):
		value = default
		return value

	def _save_fix_values(self, **kw):
		if kw.has_key('id'):
			url = 'edit?'
		else:
			url = 'new?'
		for k, v in kw.iteritems():
			if self.fields.has_key(k) and self.fields[k]['type'] != 'passwd':
				url += '%s=%s&' % (k, v)
		tmp_kw = dict(kw)
		for k, v in tmp_kw.iteritems():
			if self.fields.has_key(k):
				if v:
					kw[k] = self._save_fix_value(k, v)
				elif self.fields[k].has_key('default'):
					kw[k] = self._save_fix_value_default(k, self.fields[field]['default'])
				else: #debug
					kw[k] = None
				v = kw[k]
				if self.fields[k]['required'] and v == '' and self.fields[k]['type'] != 'passwd':
					flash(
							'%s is required. Please fill it up before submitting.' % (self.fields[k]['description'])
						)
					redirect(url)
				elif self.fields[k]['type'] == 'passwd':
					if v == False:
						flash('%s entered do not match.' % (self.fields[k]['description']))
						redirect(url)
					elif v == None:
						del kw[k]
						del v
						continue
		return kw

	def _save_get_value_bool(self, value):
		if type(value) == list:
			if 'True' in value:
				value = True
			else:
				value = False
		elif value == 'False':
			value = False
		elif value == 'True':
			value = True
		return value

	def _save_get_value_datetime(self, value):
		c_date,c_time = value.split(' ')
		year,mon,day = c_date.split('-')
		hour,min,sec = c_time.split(':')
		value = datetime.datetime(
				int(year),
				int(mon),
				int(day), 
				int(hour),
				int(min),
				int(float(sec)),
			)
		return value

	def _save_get_value_passwd(self, value):
		value = self._verify_passwd(value)
		return value

	def _save_get_value_time(self, value):
		# Still can't save
		date = Now().strftime('%Y-%m-%d')
		value = '%s %s' % (date, value)
		value = self._save_get_value_datetime(value)
		return value

	def _save_new(self, **kw):
		'''Save new entry to the DB and return the row object of the new entry
		'''
		# Make sure everything passed to the DB is in the field list
		inputs = {}
		for k, v in kw.iteritems():
			if k in self.all_fields:
				inputs[k] = v
		# Save new entry to the DB and return the row object
		row = self.tbl(**inputs)
		return row

	def _save_old(self, id, **kw):
		'''Modify entries of a row with the given id and return the row object of the modified row
		'''
		row = self.tbl.get(id)
		for k, v in kw.iteritems():
			setattr(row, k, v)
		return row

	def _set_col_dict(self):
		#col_dict = self.tbl._columnDict
		col_dict = self.tbl.sqlmeta.columns
		self.col_dict = {}
		for k, v in col_dict.iteritems():
			self.col_dict[k.replace('ID', '')] = v
		self.all_fields = self.col_dict.keys()

	def _verify_passwd(self, value):
		(value, verify) = value
		if value == verify:
			if value == '':
				value = None
			else:
				return crypt.crypt(value, get_salt())
		else:
			return False

	@expose()
	def action(self, action, **kw):
		'''This runs an action given by the keyword: action
		'''
		return self._action(action, **kw)

	@expose()
	@expose('json')
	def cancel(self, **kw):
		flash('')
		try: del self.actions
		except AttributeError: pass
		self._common()
		try:
			url = self.cancel_url
		except AttributeError:
			url = 'index'
		redirect(url)

	@expose(_get_temp('details'))
	@expose('json')
	def details(self, id, **kw):
		self.auth('details')
		page_dict = self._details(id, **kw)
		#page_dict['tg_template'] = str(self._get_template('details'))
		return page_dict

	@expose()
	def delete(self, id, **kw):
		self.auth('delete')
		##TODO: Verify before deleting
		#page_dict = self._delete(id, **kw)
		#redirect('details?')
		self.actions = ('verify_delete', 'cancel', )
		return self.details(id, **kw)

	@expose(_get_temp('edit'))
	@expose('json')
	def edit(self, id, **kw):
		self.auth('edit')
		page_dict = self._edit(id, **kw)
		#page_dict['tg_template'] = str(self._get_template('edit'))
		return page_dict

	@expose(_get_temp('error'))
	def error(self, msg):
		page_dict = self._common()
		page_dict['head'] = msg
		page_dict['msg'] = msg
		page_dict['title'] = msg
		#page_dict['tg_template'] = str(self._get_template('error'))
		return page_dict

	@expose(_get_temp('item'))
	@expose('json')
	def item(self):
		self.auth('item')
		page_dict = get_dict(self._item())
		#page_dict['tg_template'] = str(self._get_template('item'))
		return page_dict

	@expose(_get_temp('list'))
	@expose('json')
	def search(self, **kw):
		self.auth('list')
		kw['search'] = 'Search'
		page_dict = self._list(**kw)
		#page_dict['tg_template'] = str(self._get_template('search'))
		return page_dict

	@expose(_get_temp('list'))
	@expose('json')
	def list(self, **kw):
		self.auth('list')
		page_dict = self._list(**kw)
		#page_dict['tg_template'] = str(self._get_template('list'))
		return page_dict

	@expose(_get_temp('edit'))
	@expose('json')
	def new(self, **kw):
		self.auth('new')
		page_dict = get_dict(self._edit(**kw))
		#page_dict['tg_template'] = str(self._get_template('edit'))
		return page_dict

	@expose()
	@expose('json')
	def save(self, id=None, **kw):
		self.auth('save')
		self._save(id, **kw)
		flash('Successfully saved entry')
		redirect('index')

	@expose()
	@expose('json')
	def verify_delete(self, id, **kw):
		self.auth('delete')
		try: del self.actions
		except AttributeError: pass
		self._delete(id, **kw)
		redirect('index')

	index = list


