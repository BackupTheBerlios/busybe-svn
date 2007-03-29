# This module provides helper functions for the JSON part of your
# view, if you are providing a JSON-based API for your app.

# Here's what most rules would look like:
# @jsonify.when("isinstance(obj, YourClass)")
# def jsonify_yourclass(obj):
#     return [obj.val1, obj.val2]
#
# The goal is to break your objects down into simple values:
# lists, dicts, numbers and strings

from turbojson.jsonify import jsonify
import sqlobject

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

@jsonify.when('isinstance(obj, type)')
def jsonify_type(obj):
	return str(obj)

@jsonify.when('isinstance(obj, sqlobject.SOBoolCol)')
def jsonify_bool_col(obj):
	return str(obj)

@jsonify.when('isinstance(obj, sqlobject.SODecimalCol)')
def jsonify_decimal_col(obj):
	return str(obj)

@jsonify.when('isinstance(obj, sqlobject.SODateCol)')
def jsonify_date_col(obj):
	return str(obj)

@jsonify.when('isinstance(obj, sqlobject.SODateTimeCol)')
def jsonify_datetime_col(obj):
	return str(obj)

@jsonify.when('isinstance(obj, sqlobject.SOFloatCol)')
def jsonify_float_col(obj):
	return str(obj)

@jsonify.when('isinstance(obj, sqlobject.SOIntCol)')
def jsonify_int_col(obj):
	return str(obj)

@jsonify.when('isinstance(obj, sqlobject.SOUnicodeCol)')
def jsonify_unicode_col(obj):
	return str(obj)

