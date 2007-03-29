<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]"/>
    <style type="text/css">
        #pageLogin
        {
            font-size: 10px;
            font-family: verdana;
            text-align: right;
        }
    </style>
	<style type="text/css" media="screen">
		@import "/static/css/style.css";
	</style>
	<script src="/static/date_chooser/date-functions.js" type="text/javascript"></script>
	<script src="/static/date_chooser/datechooser.js" type="text/javascript"></script>
	<link rel="stylesheet" type="text/css" href="/static/date_chooser/datechooser.css" />
	<script type="text/javascript">

		function sort_page(field, prev_field) {
			reversed = document.list_form.reversed.value
			if (field == prev_field) {
				if (reversed == 'False') {
					document.list_form.reversed.value = 'True';
				} else if (reversed == 'True') {
					document.list_form.reversed.value = 'False';
				}
			} else {
				document.list_form.reversed.value = 'False';
			}//if (field == prev_field)
			document.list_form.sort_page_by.value = field;
			document.list_form.submit();
		}//function sort_page(field)

		function goto_page(page) {
			document.list_form.page.value = page;
			document.list_form.submit();
		}//function goto_page(page)

	</script>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

<!-- START List -->
<div py:def="show_list_page()" id="page_list">
	<form id="list_form" name="list_form" method="get">
	<div py:replace="show_quick_search()" />
	<table py:replace="show_list_table()" />
	</form>
</div><!--page_list-->
<!-- END List -->

<!-- START List Table -->
<table py:def="show_list_table()" class="list_table">
	<?python
	col_cnt = len(column_fields)
	if 0 < len(actions):
		col_cnt += 1
	row_keys = rows.keys()
	row_keys.sort()
	if reversed:
		row_keys.reverse()
	row_odd = False
	row_class = 'odd_row'
	?>

	<thead>
		<tr>
		<td colspan="${col_cnt}">
			<span py:replace="get_list_sort()" />
			<span py:replace="get_list_items()" />
			<span py:replace="get_list_nav()" />
		</td>
		</tr>
		<tr>
		<th py:if="len(actions) > 0">
			Actions
		</th>
		<th py:for="field in column_fields">
			<a href="javascript: sort_page('${field}', '${sort_page_by}')">
				${fields[field]['description']}
				<img py:if="sort_page_by==field and reversed==False" src="/static/images/list/down.gif" />
				<img py:if="sort_page_by==field and reversed==True" src="/static/images/list/up.gif" />
			</a>
		</th>
		</tr>
	</thead>

	<tfoot>
		<tr>
		<td colspan="${col_cnt}">
			<span py:replace="get_list_items()" />
			<span py:replace="get_list_nav()" />
			<span py:replace="get_new_link()" />
			<input type="hidden" id="sort_page_by" name="sort_page_by" value="${sort_page_by}" />
			<input type="hidden" id="reversed" name="reversed" value="${reversed}" />
			<input type="hidden" id="page" name="page" value="${page}" />
		</td>
		</tr>
	</tfoot>

	<tbody>
		<tr class="${row_class}" py:for="k in row_keys">
		<?python
		if row_odd:
			row_odd = False
			row_class = 'odd_row'
		else:
			row_odd = True
			row_class = 'even_row'
		row = rows[k]
		?>
		<td>
			<span py:for="action in ('details', 'edit', 'delete')" py:if="action in actions">
				<a href="${action}?id=${row['id']}">${beautify(action)}</a>
			</span>
		</td>
		<td py:for="field in column_fields">
			${row[field]}
		</td>
		</tr>
	</tbody>
</table>
<!-- START List Table -->


<!-- START New Item Link -->
<span py:def="get_new_link()" class="new_item_link">
	<a href="new">New Item</a>
</span>
<!-- END New Item Link -->

<!-- START List Items -->
<span py:def="get_list_items()" class="page_list_items">
	<?python
	first_row = first_row+1
	if max_row < last_row:
		last_row = max_row
	item_desc = 'item'
	if 1 < max_row:
		item_desc += 's'
	?>
	$first_row to $last_row of $max_row $item_desc
</span>
<!-- END START List Items -->

<!-- START List Nav -->
<span py:def="get_list_nav()" class="page_list_nav">
	<?python
	tmp = float(max_row)/float(show)
	last_page = int(tmp)
	if last_page < tmp:
		last_page += 1
	first_prev = 1<page
	last_next = page<last_page
	?>
	<a py:if="first_prev" href="javascript: goto_page(1)">&lt;&lt;First</a>
	<a py:if="first_prev" href="javascript: goto_page(${page-1})">&lt;Prev</a>
	Page ${page}
	<a py:if="last_next" href="javascript: goto_page(${page+1})">Next&gt;</a>
	<a py:if="last_next" href="javascript: goto_page(${last_page})">Last&gt;&gt;</a>
</span>
<!-- END List Nav -->


<!-- START List Sort -->
<span py:def="get_list_sort()" class="page_list_sort">
	Sort Results By:
	<select id="sort_result_by" name="sort_result_by"
		onchange="
			this.form.page.value=1;
			this.form.sort_page_by.value=this.value;
			this.form.reversed_result.checked='True';
			this.form.reversed.value='True';
			submit()">
		<option value="id"></option>
		<option py:for="field in column_fields" value="$field" py:if="sort_result_by != field and fields[field]['type'] != list">${fields[field]['description']}</option>
		<option py:for="field in column_fields" value="$field" selected="selected"  py:if="sort_result_by == field and fields[field]['type'] != list">${fields[field]['description']}</option>
	</select>
	Reverse:
	<input type="checkbox" id="reversed_result" name="reversed_result"
		value="True" onclick="this.form.reversed.value='True'; submit()" py:if="reversed_result==False" />
	<input type="checkbox" id="reversed_result" name="reversed_result"
		value="True" checked="checked" onclick="this.form.reversed.value=''; submit()" py:if="reversed_result==True" />
</span>
<!-- END List Sort -->


<!-- START List Quick Search -->
<div py:def="show_quick_search()" id="quick_search_form">
<?python
search_details = list(search_fields)
?>
<table class="quick_search">
<thead>
	<tr>
		<th>Search</th>
	</tr>
</thead>
<tbody>
	<tr><td>
		<select id="search_field" name="search_field"
			onclick="show(this.value)"
			onchange="show(this.value)">
		<option py:if="not search_field" value=""
		>-- select field --</option>
		<option py:for="detail in search_details" value="${detail}"
		py:if="search_field==detail" selected="selected"
		>${fields[detail].get('description', beautify(detail))}</option>
		<option py:for="detail in search_details" value="${detail}"
		py:if="search_field!=detail"
		>${fields[detail].get('description', beautify(detail))}</option>
	</select>

	<div id="search_div_" style="display: inline;"></div>

	<div py:for="detail in search_details"
		id="search_div_${detail}" style="display: none;">
		${search_input_field(detail)}
	</div>

	<?python
	js_search_fields = ','.join('"%s"'%a for a in search_details)
	?>

	<script type="text/javascript">
		var fields = new Array(${js_search_fields});

		function hideall() {
			if(document.layers){ for (i in fields) {
					document['search_div_'+fields[i]].display="none";
				} }
			if(document.all){ for (i in fields) {
					document.all['search_div_'+fields[i]].style.display="none";
				} }
			if(document.getElementById) { for (i in fields) {
					document.getElementById('search_div_'+fields[i]).style.display="none";
				} }
		}

		function show(z) {
			hideall();
			if(document.layers) {
				document['search_div_'+z].display="inline";
				//document['sort_result_by'].value = z;
				//document['sort_page_by'].value = z;
			}
			if(document.all) {
				document.all['search_div_'+z].style.display="inline";
				//document.all['sort_result_by'].value = z;
				//document.all['sort_page_by'].value = z;
			}
			if(document.getElementById) {
				document.getElementById('search_div_'+z).style.display="inline";
				//document.getElementById['sort_result_by'].value = z;
				//document.getElementById['sort_page_by'].value = z;
			}
			document.list_form.sort_result_by.value = z;
			document.list_form.sort_page_by.value = z;
		}

		show("${search_field}");
	</script>

	<input id="quick_search" name="quick_search" value="Search" type="submit" onclick="this.form.page.value=1;" />
	<a href="?" title="View All">View All</a> |
	<a href="search" title="Advanced Search">Detailed Search</a>
	</td></tr>
</tbody>
</table>
</div>
<!-- END List Quick Search -->


<!-- START Search Fields -->
<span py:def="search_input_field(detail)" class="search_input_field">
	<?python
	col_type = False
	if fields[detail].has_key('type'):
		col_type = fields[detail]['type']
	value = None
	if search_values.has_key(detail):
		value = search_values[detail]
	column = False
	if fields[detail].has_key('column'):
		column = fields[detail]['column']
	options = False
	if fields[detail].has_key('options'):
		options = fields[detail]['options']
	add = False
	if fields[detail].has_key('add'):
		add = fields[detail]['add']
	description = fields[detail].get('description', beautify(detail))
	?>

	<span py:if="col_type in (str, unicode, 'text')">
		<input id="${detail}" name="${detail}"
		value="${value}" />
	</span>

	<span py:if="col_type == bool">
		<select id="${detail}" name="${detail}">
			<?python
			if value in ('True', 'False'):
				value = value
			else:
				value = None
			?>
			<option value="${value}" selected="selected"
			py:if="value in ('True', 'False')"
			>${value}</option>
			<option value=""></option>
			<!-->${fields[detail][value]}</option>-->
			<option value="${option}"
			py:for="option in ('True', 'False')"
			py:if="option != value"
			>${option}</option>
			<!-->${fields[detail][option]}</option>-->
		</select>
	</span>

	<span py:if="col_type == int">
		<?python
		if not value:
			value = ('', '')
		elif type(value) is not list:
			value = ('', '')
		?>
		<input id="${detail}_first" name="${detail}_first"
		value="${value[0]}" size="8" /> -
		<input id="${detail}_last" name="${detail}_last"
		value="${value[1]}" size="8" />
		<small>Integer (1, 2, 3, ...)</small>
	</span>

	<span py:if="col_type == float">
		<?python
		if not value:
			value = ('', '')
		elif type(value) is not list:
			value = ('', '')
		?>
		<input id="${detail}_first" name="${detail}_first"
		value="${value[0]}" size="8" /> -
		<input id="${detail}_last" name="${detail}_last"
		value="${value[1]}" size="8" />
		<small>Float (1.0, 0.5, -3.9, 6, ...)</small>
	</span>

	<span py:if="col_type == 'datetime'">
		<?python
		current_date = ''
		if not value:
			value = (current_date, current_date)
		elif type(value) is not list:
			value = (current_date, current_date)
		?>
		<input name="${detail}_first" id="${detail}_first"
		value="${value[0]}" size="18" />
		<img src="/static/date_chooser/calendar.gif"
		onclick="showChooser(this, '${detail}_first', '${detail}_first_chooser', 1950, 2010, Date.patterns.ISO8601LongPattern, true);" />
		<div id="${detail}_first_chooser" class="dateChooser select-free"
		   	style="display: none; visibility: hidden; width: 160px;">
		</div>
		-
		<input name="${detail}_last" id="${detail}_last"
		value="${value[1]}" size="18" />
		<img src="/static/date_chooser/calendar.gif"
		onclick="showChooser(this, '${detail}_last', '${detail}_last_chooser', 1950, 2010, Date.patterns.ISO8601LongPattern, true);" />
		<div id="${detail}_last_chooser" class="dateChooser select-free"
		   	style="display: none; visibility: hidden; width: 160px;">
		</div>
		<!--small>Date: ${Now.strftime('%Y-%m-%d')}</small-->
	</span>

	<span py:if="col_type == 'date'">
		<?python
		#current_date = Now.strftime('%Y-%m-%d')
		current_date = ''
		if not value:
			value = (current_date, current_date)
		elif type(value) is not list:
			value = (current_date, current_date)
		?>
		<input name="${detail}_first" id="${detail}_first"
		value="${value[0]}" size="10" />
		<img src="/static/date_chooser/calendar.gif"
		onclick="showChooser(this, '${detail}_first', '${detail}_first_chooser', 1950, 2010, 'Y-m-d', false);" />
		<div id="${detail}_first_chooser" class="dateChooser select-free"
		   	style="display: none; visibility: hidden; width: 160px;">
		</div>
		-
		<input name="${detail}_last" id="${detail}_last"
		value="${value[1]}" size="10" />
		<img src="/static/date_chooser/calendar.gif"
		onclick="showChooser(this, '${detail}_last', '${detail}_last_chooser', 1950, 2010, 'Y-m-d', false);" />
		<div id="${detail}_last_chooser" class="dateChooser select-free"
		   	style="display: none; visibility: hidden; width: 160px;">
		</div>
		<!--small>Date: ${Now.strftime('%Y-%m-%d')}</small-->
	</span>

	<span py:if="col_type == 'time'">
		<?python
		#current_time = Now.strftime('%H:%M:%S')
		current_time = ''
		if not value:
			value = (current_time, current_time)
		elif type(value) is not list:
			value = (current_time, current_time)
		?>
		<input name="${detail}_first" id="${detail}_first"
			value="${value[0]}" size="10" /> -
		<input name="${detail}_last" id="${detail}_last"
			value="${value[1]}" size="10" />
		<!--small>Time: ${Now.strftime('%H:%M:%S')}</small-->
	</span>

	<span py:if="col_type == list">
		<?python
		if value:
			value = int(value)
		?>
		<select name="${detail}" id="${detail}">
			<option py:if="value"
			value="${value}" selected="selected"
			>${options[value][column]}</option>
			<option value=""></option>
			<option py:for="option in options"
			py:if="option != value" value="${option}"
			>${options[option][column]}</option>
		</select>
	</span>

	<span py:if="col_type == dict">
		<select name="${detail}" id="${detail}">
			<option py:if="not value"
			value=""></option>
			<option py:if="value"
			value="${value}" selected="selected"
			>${options[value]}</option>
			<option py:for="option in options.keys()"
			py:if="option != value" value="${option}"
			>${options[option]}</option>
		</select>
	</span>
</span>
<!-- END Search Fields -->


<!-- START Details -->
<div py:def="show_details_page(values={})" id="page_details">
	<form action="action">

	<input py:if="entry_id"
	type="hidden" id="id" name="id"
	value="${entry_id}"
	/>

	<table>

	<tbody py:for="field in detail_fields">
		<?python
		?>
		<tr>
			<th>${fields[field]['description']}:</th>
			<td>${values[field]}</td>
		</tr>
	</tbody>

	</table>

	<span py:for="action in ('edit', 'delete', 'verify_delete', 'cancel')" py:if="action in actions">
		<a href="${action}?id=${entry_id}">${beautify(action)}</a>
	</span>

	<!--input type="submit" id="action" name="action" value="Edit"/-->
	<!--input type="submit" id="action" name="action" value="Delete"/-->

	</form>
</div>
<!-- END Details -->


<!-- START Edit -->
<div py:def="show_edit_page(values={})" id="page_edit">
	<form action="action" id="edit_form" name="edit_form">

	<input py:if="entry_id"
	type="hidden" id="id" name="id"
	value="${entry_id}" />

	<input py:for="field in hidden_fields"
	type="hidden" id="${field}" name="${field}"
	value="${values[field]}" />

	<table>

	<tbody py:for="field in edit_fields">
		<?python
		detail = fields[field]
		?>
		<tr py:if="detail['type'] not in (list, bool, int, float, 'text', 'passwd', 'date', 'time', 'datetime')"
			py:replace="show_edit_common(field, detail)" />
		<tr py:if="detail['type'] == 'date'" py:replace="show_edit_date(field, detail)" />
		<tr py:if="detail['type'] == 'datetime'" py:replace="show_edit_datetime(field, detail)" />
		<tr py:if="detail['type'] == 'passwd'" py:replace="show_edit_passwd(field, detail)" />
		<tr py:if="detail['type'] == 'text'" py:replace="show_edit_text(field, detail)" />
		<tr py:if="detail['type'] == 'time'" py:replace="show_edit_time(field, detail)" />
		<tr py:if="detail['type'] == int" py:replace="show_edit_int(field, detail)" />
		<tr py:if="detail['type'] == float" py:replace="show_edit_float(field, detail)" />
		<tr py:if="detail['type'] == bool" py:replace="show_edit_bool(field, detail)" />
		<tr py:if="detail['type'] == list" py:replace="show_edit_list(field, detail)" />

	</tbody>

	</table>

	<input onclick="this.form.target=''; this.form.action='save' this.form.id.value=${entry_id};" type="submit" id="action" name="action" value="Save"/>
	<input type="reset" value="Clear" />
	<input onclick="this.form.target=''; this.form.action='cancel';" type="submit" id="action" name="action" value="Cancel"/>

	</form>
</div>
<!-- END Edit -->

<!-- START Edit Input Functions -->

<tr py:def="show_edit_common(field, detail)">
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<input id="${field}" name="${field}"
		value="${values[field]}"
		maxlength="${detail['length']}"
		/>
	</td>
</tr>

<tr py:def="show_edit_time(field, detail)">
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<input id="${field}" name="${field}"
		value="${values[field]}" size="7" />
		<small>(Time: 08:15, 13:06, ...)</small>
	</td>
</tr>

<tr py:def="show_edit_date(field, detail)">
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<input id="${field}" name="${field}"
		value="${values[field]}" size="10" />
		<img src="/static/date_chooser/calendar.gif"
		onclick="showChooser(this, '${field}', '${field}_chooser', 1950, 2010, 'Y-m-d', false);" />
			<div id="${field}_chooser" class="dateChooser select-free"
			   	style="display: none; visibility: hidden; width: 160px;">
			</div>
	</td>
</tr>

<tr py:def="show_edit_datetime(field, detail)">
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<input id="${field}" name="${field}"
		value="${values[field]}" size="18" />
		<img src="/static/date_chooser/calendar.gif"
		onclick="showChooser(this, '${field}', '${field}_chooser', 1950, 2010, Date.patterns.ISO8601LongPattern, true);" />
			<div id="${field}_chooser" class="dateChooser select-free"
			   	style="display: none; visibility: hidden; width: 160px;">
			</div>
	</td>
</tr>

<tr py:def="show_edit_passwd(field, detail)">
	<th>
		${detail['description']}<sup py:if="detail['required']">*</sup><br />
		Verify ${detail['description']}<sup py:if="detail['required']">*</sup>
	</th>
	<td>
		<input id="${field}" name="${field}" type="password"
		maxlength="${detail['length']}" /><br />
		<input id="${field}" name="${field}" type="password"
		maxlength="${detail['length']}" />
	</td>
</tr>

<tr py:def="show_edit_text(field, detail)">
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<textarea id="${field}" name="${field}"
			rows="6" cols="32"
			>${values[field]}</textarea>
	</td>
</tr>

<tr py:def="show_edit_int(field, detail)">
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<input id="${field}" name="${field}"
		value="${values[field]}" size="8"
		/>
		<small>(1, 2, 3, ...)
		</small>
	</td>
</tr>

<tr py:def="show_edit_float(field, detail)">
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<input id="${field}" name="${field}"
		value="${values[field]}" size="8"
		/>
		<small>(0.3, 2, 6.4, ...)
		</small>
	</td>
</tr>

<tr py:def="show_edit_bool(field, detail)">
	<th>${detail['description']}</th>
	<td>
		<input type="hidden" id="${field}" name="${field}"
		value="False" />
		<input type="checkbox" id="${field}" name="${field}"
		py:if="values[field]" checked="checked" value="True" />
		<input type="checkbox" id="${field}" name="${field}"
		py:if="not values[field]" value="True" />
	</td>
</tr>

<tr py:def="show_edit_list(field, detail)">
	<?python
	options = detail['options']
	chosen_id = values[field]
	if chosen_id:
		chosen_option = options.pop(values[field])
	?>
	<th>${detail['description']}<sup py:if="detail['required']">*</sup></th>
	<td>
		<select id="${field}" name="${field}">
			<option py:if="chosen_id" value="${chosen_id}">${chosen_option[detail['column']]}</option>
			<option value=""></option>
			<option py:for="key, option in options.iteritems()" value="${key}">${option[detail['column']]}</option>
		</select>
		<!--
		<script type="text/javascript">
		function ${field}_show_details(link, value) {
			//document.${field}_detail_form.submit()
			document.edit_form.id.value = document.edit_form.${field}.value;
			document.edit_form.action = link;
			document.edit_form.target = '_blank';
			document.edit_form.submit();
		}//function ${field}_show_details(link, id)
		</script>
		<a href="javascript: ${field}_show_details('/person/details', ${chosen_id})">details</a>
		-->
	</td>
</tr>

<!-- END Edit Input Functions -->


<!-- START Detailed Search Form -->
<div py:def="show_search_page" id="page_search">
	<form action="search" method="get" id="list_form" name="list_form">
	<table id="search_form_table">
	<tbody>
	<tr py:for="field in search_fields">
		<th>${fields[field]['description']}</th>
		<td>${search_input_field(field)}</td>
	</tr>
	</tbody>
	</table>
	<input type="submit" value="Search" />
	<div id="page_list">
	<table py:replace="show_list_table()" />
	</div>
	</form>
</div>
<!-- END Detailed Search Form -->



<!-- PAGE START -->
<div py:if="tg.config('identity.on',False) and not 'logging_in' in locals()"
        id="pageLogin">
        <span py:if="tg.identity.anonymous">
            <a href="/login">Login</a>
        </span>
        <span py:if="not tg.identity.anonymous">
            Welcome ${tg.identity.user.display_name}.
            <a href="/logout">Logout</a>
        </span>
</div>

<h1>${head}</h1>

<div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

<div py:replace="[item.text]+item[:]"/>

<!-- End of main_content -->

<div id="footer0"></div>
</body>

</html>
