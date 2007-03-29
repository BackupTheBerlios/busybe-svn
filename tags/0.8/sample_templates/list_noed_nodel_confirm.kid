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




<!-- List -->
<?python
col_cnt = len(columns)
page_last = int(max_row/show)
if page_last != max_row*1.0/show:
	page_last += 1
?>

<span>
<a py:if="page != 1" title="First page"
	href="?page=1">&lt;&lt;First</a>
<a py:if="page != 1" title="Previous page"
	href="?page=${page-1}">&lt;Previous</a>
<a py:if="max_row > page*show" title="Next page"
	href="?page=${page+1}">Next&gt;</a>
<a py:if="max_row > page*show" title="Last page"
	href="?page=${page_last}">Last&gt;&gt;</a>
</span>

<?python
cgi_args = []
for field in hidden_fields:
	cgi_args.append('%s=%s' % (field, fields[field]['value']))
str_cgi_args = '&'.join(cgi_args)
?>

<form action="mass_update">
<table class="list">
	<thead><tr>
		<th py:for="column in columns">
		<a href="?sort_page_by=${column}&amp;page=${page}"
			>${fields[column].get('description', beautify(column))}</a>
		</th>
	</tr></thead>

	<tfoot><tr>
		<th colspan="${col_cnt}" style="text-align: right;">
			<!--span id="newlink">
				<a href="new?${str_cgi_args}">add item</a>
<a py:if="page != 1" title="First page"
	href="?page=1">&lt;&lt;First</a>
<a py:if="page != 1" title="Previous page"
	href="?page=${page-1}">&lt;Previous</a>
<a py:if="max_row > page*show" title="Next page"
	href="?page=${page+1}">Next&gt;</a>
<a py:if="max_row > page*show" title="Last page"
	href="?page=${page_last}">Last&gt;&gt;</a>
			</span-->
			<span id="rowcount">${row_cnt} item(s)</span>
		</th>
	</tr></tfoot>

	<tbody py:for="row in rows">
		<tr>
			<!--td>
				<span
				py:for="action in actions">&nbsp;|&nbsp;<a
					href="${action['link'].replace('$id', str(row.id))}"
					>${action['description']}</a></span>
			</td-->
			<!--td>
				${row.finished_fabric}
			</td-->
			<td py:for="field in columns">
				<?python
				if not fields[field].has_key('type'):
					value = getattr(row, field)
				elif fields[field]['type'] == 'select':
					option = getattr(row, field)
					column = fields[field]['column']
					if hasattr(option, column):
						option_value = getattr(option, column)
					else:
						#option_value = 'ERROR! attribute "%s" not found in %s' % (column, option)
						option_value = ''
					value = option_value
				elif fields[field]['type'] == 'foreign_text':
					option = getattr(row, field)
					column = fields[field]['column']
					if hasattr(option, column):
						option_value = getattr(option, column)
					else:
						#option_value = 'ERROR! attribute "%s" not found in %s' % (column, option)
						option_value = ''
					value = option_value
				elif fields[field]['type'] == dict:
					if fields[field].has_key('options_short'):
						value = fields[field]['options_short'][getattr(row, field).id]
					elif fields[field].has_key('options'):
						value = fields[field]['options'][getattr(row, field).id]
					else:
						value = getattr(row, field).id
				elif fields[field]['type'] == 'bool':
					value = fields[field][getattr(row, field)]
				elif fields[field]['type'] == 'time':
					value = str(getattr(row, field))
					value = re.sub('.* ', '', value)
				else:
					value = getattr(row, field)
				?>
				${value}
			</td>
		</tr>
		<tr py:if="not details == columns">
		<td colspan="${col_cnt}" class="details">
			<span py:for="field in details" py:if="hasattr(row, field) and getattr(row, field) and not field in columns">
				<?python
				col_type = False
				if fields[field].has_key('type'):
					col_type = fields[field]['type']
				?>
				<span py:if="col_type == 'select'">
					<?python
					column = fields[field]['column']
					option = getattr(row, field)
					if hasattr(option, column):
						option_value = getattr(option, column)
					else:
						option_value = 'ERROR! attribute "%s" not found in %s' % (column, option)
					?>
					<strong>${fields[field].get('description', beautify(field))}:</strong>
					${option_value}
				</span>
				<span py:if="col_type == 'foreign_text'">
					<strong>${fields[field].get('description', beautify(field))}:</strong> ${getattr(getattr(row, field), fields[field]['column'])} 
				</span>
				<div py:if="col_type == dict">
					<strong>${fields[field].get('description', beautify(field))}:</strong>
					${fields[field]['options'][getattr(row, field).id]}
				</div>
				<span py:if="col_type == 'bool'">
					<strong>${fields[field].get('description', beautify(field))}:</strong>
					${fields[field][getattr(row, field)]}
				</span>
				<span py:if="col_type == 'time'">
					<strong>${fields[field].get('description', beautify(field))}:</strong>
					${re.sub('.* ', '', str(getattr(row, field)))}
				</span>
				<span py:if="not col_type or col_type not in ('time', dict, 'select', 'text', 'password', 'foreign_text')">
					<strong>${fields[field].get('description', beautify(field))}:</strong>
					${getattr(row, field)} 
				</span>
				<div py:if="col_type == 'text'">
					<strong>${fields[field].get('description', beautify(field))}:</strong>
					${getattr(row, field)} 
				</div>
			</span>
		</td>
		</tr>

		<tr py:for="entry in entry_details">
		<td colspan="2" class="details">
			<strong>${entry['column']}</strong>
		</td>
		<td colspan="${col_cnt-2}" class="details">
			<?python
			id = row
			for column in entry['id']:
				id = getattr(id, column, id)
			?>
			${entry['details'].get(id)}
		</td>
		</tr>

		<tr py:for="item_detail in item_details">
			<?python
			results = getattr(row, item_detail['join_on'], [])
			item_dict = {}
			for result in results:
				item_tuple = []
				item_code = (getattr(result, item_detail['id_col'], ''))
				for column_detail in item_detail['tuple']:
					cols = column_detail.split('.')
					value = result
					for col in cols:
						value = getattr(value, col, '')
					item_tuple.append(value)
				item_dict[item_code] = item_detail['fstring'] % tuple(item_tuple)
			?>
			<td>
				${item_detail['label']} Details:
			</td>
			<td colspan="${col_cnt-1}">
				<div py:for="k,v in item_dict.items()">
					<b>${k}</b>: ${v}
				</div>
			</td>
		</tr>

	</tbody>

</table>
</form>

<form action="confirm">
<input type="hidden" name="new" value="${new}" />
<input type="hidden" name="id" value="${id}" />
<input py:for="field in hidden_fields"
py:if="fields.has_key(field)"
type="hidden" name="${field}"
value="${fields[field]['value']}" />
<input type="submit" name="submit" value="Add Another Item" />
<input type="submit" name="submit" value="Confirm" />
<input type="submit" name="submit" value="Cancel" />
</form>


</div>

</body>
</html>
