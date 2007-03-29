<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<?python
import re
import datetime
title = re.sub(r'([A-Z][a-z0-9]*)', r' \1', title)
?>

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
	<title> ${title} List [8layer Technologies] </title>
	<script language="JavaScript">
	<!-- Begin
	var checkflag = "false";
	function check(field) {
		if (checkflag == "false") {
			for (i = 0; i < field.length; i++) {
				field[i].checked = true;}
			field.checked = true;
			checkflag = "true";
			return 0; }
		else {
			for (i = 0; i < field.length; i++) {
				field[i].checked = false; }
			field.checked = false;
			checkflag = "false";
			return 0; }
	}
	//  End --></script>
	<script src="/static/date_chooser/date-functions.js" type="text/javascript"></script>
	<script src="/static/date_chooser/datechooser.js" type="text/javascript"></script>
	<link rel="stylesheet" type="text/css" href="/static/date_chooser/datechooser.css" />

	<style>
	<!--

	table.edit {
	}
	table.edit th, table.edit td {
		margin: 0px 0px 0px 0px;
		padding: 4px 6px 4px 6px;
	}
	table.edit tbody th {
		background-color: #030;
		color: #f0fff0;
		font-size: smaller;
		text-align: right;
	}
	table.edit tfoot th {
		background-color: #9a9;
		color: #efe;
	}
	table.edit tfoot th span#newlink {
		float: left;
	}
	table.edit tfoot th span#rowcount {
		float: right;
	}
	table.edit tbody {
	}
	table.edit tbody td {
		background-color: #d9e0d9;
		color: #000;
	}
	table.edit tbody {
	}

	table.list {
	}
	table.list th, table.list td {
		margin: 0px 0px 0px 0px;
		padding: 4px 6px 4px 6px;
	}
	table.list th a {
		color: #efe;
	}
	table.list thead th {
		background-color: #030;
		color: #efe;
	}
	table.list tfoot th {
		background-color: #9a9;
		color: #efe;
	}
	table.list tfoot th span#newlink {
		float: left;
		margin-right: 8px;
	}
	table.list tfoot th span#rowcount {
		float: right;
		margin-left: 8px;
	}
	table.list tbody {
	}
	table.list tbody td {
		background-color: #d9e0d9;
		color: #000;
	}
	table.list tbody {
	}

	-->
	</style>
</head>

<body>
<?python
Now = datetime.datetime.now()
def beautify(text=''):
	'''Capitalize the first letter of each word.
	'''
	words = (word.capitalize() for word in text.split('_'))
	text = ' '.join(words)
	return text
?>

<div>
<h2>${title}</h2>

<!-- Edit -->
<form action="save" method="post">
<input type="hidden" name="new" value="${new}" />
<input type="hidden" name="id" value="${id}" />
<input py:for="field in hidden_fields"
py:if="fields.has_key(field)"
type="hidden" name="${field}"
value="${fields[field]['value']}" />
<table class="edit">
	<tbody py:for="detail in details">
	<?python
	col_type = False
	if fields[detail].has_key('type'):
		col_type = fields[detail]['type']
	value = False
	if fields[detail].has_key('value'):
		value = fields[detail]['value']
	column = False
	if fields[detail].has_key('column'):
		column = fields[detail]['column']
	options = False
	if fields[detail].has_key('options'):
		options = fields[detail]['options']
	add = False
	if fields[detail].has_key('add'):
		add = fields[detail]['add']
	if fields[detail].has_key('search'):
		search = fields[detail]['search']
	description = fields[detail]['description']
	label = description
	if fields[detail].has_key('label'):
		label = fields[detail]['label']
	?>

	<tr py:if="not col_type">
		<th>
			${description}
		</th>
		<td>
			<input name="${detail}" id="${detail}"
			value="${value}" />
		</td>
	</tr>

	<tr py:if="col_type == 'password'">
		<th>
			${description}<br />
			Verify ${description}
		</th>
		<td>
			<input name="${detail}" id="${detail}"
			type="password" /><br />
			<input name="verify_${detail}" id="verify_${detail}"
			type="password" />
		</td>
	</tr>

	<tr py:if="col_type == 'select'">
		<th>
			${description}
		</th>
		<td>
			<select name="${detail}" id="${detail}">
				<option py:if="new==True or not value or value.id==0"
				value=""></option>
				<option py:if="new==False and value and value.id!=0"
				value="${value.id}" selected="selected">
				<?python
				if hasattr(value, column):
					option_value = getattr(value, column)
				else:
					option_value = 'ERROR! attribute "%s" not found' % column
				?>${option_value}</option>
				<option py:for="option in options"
				py:if="option != value or new==True"
				value="${option.id}">
				<?python
				if hasattr(option, column):
					option_value = getattr(option, column)
				else:
					option_value = 'ERROR! attribute "%s" not found' % column
				?>${option_value}</option>
			</select>
			<?python
			#if column == 'name':
			#	what = type(option.__class__.name.fget(1))
			#else:
			#	what = ''
			#${str(dir(option.__class__))}
			#${option}
			#${str(dir(what))}
			#${str(what.__doc__)}
			#${what}
			?>
			<small py:if="add">
				<a href="${add}" target="_blank">
					Add ${description}
				</a>
			</small>
		</td>
	</tr>

	<tr py:if="col_type == 'foreign_text'">
		<th>
			${description}
		</th>
		<td>
			<?python
			if value:
				text_value = getattr(value, fields[detail]['column'], '')
			else:
				text_value = ''
			?>
			<input id="${detail}" name="${detail}" value="${text_value}" />
			<small py:if="search">
				<a href="${search}" target="_blank">
					Search ${label}
				</a>
			</small>
		</td>
	</tr>

	<tr py:if="col_type == 'bool'">
		<th>
			${description}
		</th>
		<td>
			<select name="${detail}" id="${detail}">
				<?python
				if new==False and value:
					value = value
				else:
					value = False
				?>
				<option value="${value}" selected="selected"
				>${fields[detail][value]}</option>
				<option value="${option}"
				py:for="option in (True, False)"
				py:if="option != value"
				>${fields[detail][option]}</option>
			</select>
		</td>
	</tr>

	<tr py:if="col_type == 'int'">
		<th>
			${description}
		</th>
		<td>
			<input name="${detail}" id="${detail}"
			value="${value}" size="8" />
			<small>Integer (1, 2, 3, ...)</small>
		</td>
	</tr>

	<tr py:if="col_type == 'float'">
		<th>
			${description}
		</th>
		<td>
			<input name="${detail}" id="${detail}"
			value="${value}" size="8" />
			<small>Float (1.0, 0.5, -3.9, 6, ...)</small>
		</td>
	</tr>

	<tr py:if="col_type == 'text'">
		<th>
			${description}
		</th>
		<td>
			<?python
			text_rows = 6
			text_cols = 32
			if fields[detail].has_key('cols'):
				text_cols = fields[detail]['cols']
			if fields[detail].has_key('rows'):
				text_rows = fields[detail]['rows']
			?>
			<textarea name="${detail}" id="${detail}"
				rows="${text_rows}" cols="${text_cols}">${value}</textarea>
		</td>
	</tr>

	<tr py:if="col_type == 'hidden'">
		<th>
			${description}
		</th>
		<td>
			${value}
			<input name="${detail}" id="${detail}"
			value="${value}" type="hidden" />
		</td>
	</tr>

	<tr py:if="col_type == dict">
		<th>
			${description}
		</th>
		<td>
			<select name="${detail}" id="${detail}">
				<option py:if="new==True or not value"
				value=""></option>
				<option py:if="new==False and value"
				value="${value}" selected="selected"
				>${options[value]}</option>
				<option py:for="option in options.keys()"
				py:if="option != value"
				value="${option}"
				>${options[option]}</option>
			</select>
			<small py:if="add">
				<a href="${add}" target="_blank">
					Add ${description}
				</a>
			</small>
		</td>
	</tr>

	<tr py:if="col_type == list">
		<th>
			${description}
		</th>
		<td>
			<select name="${detail}" id="${detail}">
				<option py:if="new==True or not value"
				value=""></option>
				<option py:if="new==False and value"
				value="${value}" selected="selected"
				>${value}</option>
				<option py:for="option in options"
				py:if="option != value"
				value="${option}"
				>${option}</option>
			</select>
			<small py:if="add">
				<a href="${add}" target="_blank">
					Add ${description}
				</a>
			</small>
		</td>
	</tr>

	<tr py:if="col_type == 'datetime'">
		<?python
		current_date = Now.strftime('%Y-%m-%d %H:%M:%S')
		if not value:
			value = current_date
		?>
		<th>
			${description}
		</th>
		<td>
			<input name="${detail}" id="${detail}"
			value="${value}" size="18" />
			<img src="/static/date_chooser/calendar.gif"
			onclick="showChooser(this, '${detail}', '${detail}_chooser', 1950, 2010, Date.patterns.ISO8601LongPattern, true);" />
			<div id="${detail}_chooser" class="dateChooser select-free"
			   	style="display: none; visibility: hidden; width: 160px;">
			</div>
			<small>Date: ${current_date}</small>
		</td>
	</tr>

	<tr py:if="col_type == 'date'">
		<?python
		current_date = Now.strftime('%Y-%m-%d')
		if not value:
			value = current_date
		?>
		<th>
			${description}
		</th>
		<td>
			<input name="${detail}" id="${detail}"
			value="${value}" size="10" />
			<img src="/static/date_chooser/calendar.gif"
			onclick="showChooser(this, '${detail}', '${detail}_chooser', 1950, 2010, 'Y-m-d', false);" />
			<div id="${detail}_chooser" class="dateChooser select-free"
			   	style="display: none; visibility: hidden; width: 160px;">
			</div>
			<small>Date: ${current_date}</small>
		</td>
	</tr>

	<tr py:if="col_type == 'time'">
		<?python
		current_time = Now.strftime('%H:%M:%S')
		if not value:
			value = current_time
		?>
		<th>
			${description}
		</th>
		<td>
			<input name="${detail}" id="${detail}"
			value="${value}" size="10" />
			<small>Time: ${current_time}</small>
		</td>
	</tr>

	</tbody>
</table>
<input type="submit" id="submit" name="submit" value="Save"/>
<input type="reset" id="reset" name="reset" value="Clear"/>
</form>

</div>

</body>
</html>

