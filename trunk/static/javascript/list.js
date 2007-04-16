/*
From Jonas Raoni Soares Silva
http://www.joninhas.ath.cx
*/
String.prototype.capitalize = function(){ //v1.0
    return this.replace(/\w+/g, function(a){
        return a.charAt(0).toUpperCase() + a.substr(1).toLowerCase();
    });
};


function set_vars(result) {
	document.list_form.page.value = result['page'];
	document.list_form.sort_page_by.value = result['sort_page_by'];
}//function sort_vars(result)

function getListTable(result) {
	//createLoggingPane(true);
	set_vars(result);
	var actions = result['actions'];
	var columns = result['column_fields'];
	var fields = result['fields'];
	var first_row = result['first_row'];
	var last_row = result['last_row'];
	var max_row = result['max_row'];
	var page = result['page'];
	var reversed_result = result['reversed_result'];
	var rows = result['rows'];
	var show = result['show'];
	var sort_result_by = result['sort_result_by'];

	var col_cnt = columns.length + 1;
	var item_desc = 'item';

	var tmp_page_last = parseFloat(max_row)/parseFloat(show);
	var page_last = parseInt(tmp_page_last);
	if (page_last < tmp_page_last) {
		page_last++;
	}
	var tbl_head = getListTableHead(fields, columns, col_cnt, page, page_last, first_row, last_row, max_row, item_desc);
	var tbl_foot = getListTableFoot(col_cnt, page, page_last, first_row, last_row, max_row, item_desc);
	var tbl_body = getListTableBody(rows, fields, columns, col_cnt, page, actions);
	//var tbl_body = TBODY(null, map(getListTableRow, result['rows']));
	var lnx_pages = getPageLinks(page, last_page);
	//list_nav_load_event(page);
	replaceChildNodes('page_links', lnx_pages);
	replaceChildNodes('list_table', [tbl_head, tbl_foot, tbl_body]);
	//replaceChildNodes('list_table_body', '');
	//replaceChildNodes('list_table', tbody);
	list_nav_load_event(page);
}//function getListTable(result)

function getSortResult(sort_by, reversed, columns, fields) {
	var options = Array();
	for (i in columns) {
		var column = columns[i];
		var field = fields[column]['description'];
		options = options.concat(OPTION({'value': column}, field));
	}
	var select = SELECT({'id': 'sort_result_by', 'name': 'sort_result_by'}, options);
	var input = INPUT({'type': 'checkbox', 'id': 'reversed_result', 'name': 'reversed_result'}, '');
	var span = SPAN({'class': 'page_list_sort'}, ['Sort Results By: ', select, ' Reverse: ', input]);
	return span;
}//function getSortResult(sort_by, reversed)

function getPageLinks(page, last_page) {
	var span = Array();
	var i;
	var p_pre = '';
	var p_post = '';
	if (page < 6) {
		if (last_page < 10) {
			i_end = last_page
		} else {
			i_end = 10
		}
		for (i=1; i<=i_end; i++) {
			var a = A({'href': 'javascript: json_goto(' + i + ')'}, i);
			span = span.concat(SPAN(null, [a, ' ']));
		}
	} else if (page > last_page-5) {
		for (i=last_page-9; i<=last_page; i++) {
			var a = A({'href': 'javascript: json_goto(' + i + ')'}, i);
			span = span.concat(SPAN(null, [a, ' ']));
		}
	} else {
		for (i=page-4; i<=page+5; i++) {
			var a = A({'href': 'javascript: json_goto(' + i + ')'}, i);
			span = span.concat(SPAN(null, [a, ' ']));
		}
	}
	if (page > 5) {
		p_pre = '... ';
	}
	if (page < last_page-5) {
		p_post = ' ...';
	}
	var p = P(null, ['Pages: ', p_pre, span, p_post]);	
	return p;
}//function getPageLinks(page, last_page)

function getListTableItems(first_row, last_row, max_row, item_desc) {
	if ( max_row < last_row ) {
		last_row = max_row;
	}
	if ( 1 < max_row ) {
		item_desc += 's';
	}
	var item = (first_row+1) + ' to ' + last_row + ' of ' + max_row + ' ' + item_desc;
	return SPAN({'class': 'page_list_items'}, item);
}//function getListTableItems(first_row, last_row, max_row, item_desc)

function getListTableNewItemLink() {
	return SPAN(
		{'class': 'new_item_link'},
		A({'href': 'new'}, 'New Item')
	)
}//function getListTableNewItemLink()

function getListTableNav(id, page, page_last) {
	var nav = Array();
	var lnx = Array();
	var pages = Array();
	pages = pages.concat(1, page-1, page+1, page_last);
	for (i in pages) {
		lnx = lnx.concat({'href': 'javascript: json_goto(' + pages[i] + ')'});
	}//for (i in pages)
	if ( page > 1 ) {
		nav = nav.concat(A(lnx[0], '<<First'), ' ');
		nav = nav.concat(A(lnx[1], '<Prev'), ' ');
	}
	nav = nav.concat(' Page ' + page + ' ');
	if ( page < page_last ) {
		nav = nav.concat(A(lnx[2], 'Next>'), ' ');
		nav = nav.concat(A(lnx[3], 'Last>>'), ' ');
	}
	return SPAN({'class': 'page_list_nav'}, [nav, '\n']);
}//function getListTableNav(id, page) {

function getListTableHead(fields, columns, col_cnt, page, page_last, first_row, last_row, max_row, item_desc) {
	var thead = Array();
	var details = Array();
	var nav = getListTableNav('head', page, page_last);
	var items = getListTableItems(first_row, last_row, max_row, item_desc);
	details = details.concat(nav, items);
	var td = Array(TD({'colspan':col_cnt}, [details, '\n']));
	var th = Array(TH(null, 'Actions'));
	for (var i in columns) {
		var field = columns[i];
		field = fields[field]['description'];
		th = th.concat(TH(null, field));
	}
	var sort = TD({'colspan':col_cnt}, getSortResult('id', 'True', columns, fields));
	thead = thead.concat(TR(null, [sort, '\n']), TR(null, [td, '\n']), TR(null, [th, '\n']));
	return THEAD(null, thead);
}//function getListTableHead(fields, columns, col_cnt, page)

function getListTableFoot(col_cnt, page, page_last, first_row, last_row, max_row, item_desc) {
	var tfoot = Array();
	var details = Array();
	var nav = getListTableNav('foot', page, page_last);
	var items = getListTableItems(first_row, last_row, max_row, item_desc);
	var new_item_link = getListTableNewItemLink();
	details = details.concat(nav, items, new_item_link);
	var td = Array(TD({'colspan':col_cnt}, details));
	tfoot = tfoot.concat(TR(null, [td, '\n']));
	return TFOOT(null, tfoot);
}//function getListTableHead(fields, columns, col_cnt, page)

function getListTableBody(rows, fields, columns, col_cnt, page, actions) {
	var tbody = Array();
	var row_cnt = 0;
	for (var i in rows) {
	var row0 = rows[i];
	for (var j in row0) {
	var row1 = rows[j];
	for (var k in row1) {
	var row2 = row1[k]
	for (var l in row2) {
		var row = row2[l]
		row_cnt++;
		if (row_cnt%2) {
			var row_class = 'odd_row';
		} else {
			var row_class = 'even_row';
		}
		var row_attr = Array();
		var d_attr = Array();
		var trow = Array(TD(d_attr, _getListTableActions(actions, row['id'])));
		row_attr['class'] = row_class;
		for (var col in columns) {
			field = columns[col];
			trow = trow.concat(TD(d_attr, row[field]));
		}
		tbody = tbody.concat(TR(row_attr, [trow, '\n']));
	}
	}
	}
	}
	return TBODY(null, tbody);
}//function getListTableBody(rows, fields, columns, col_cnt, page)

function _getListTableActions(actions, id) {
	var lnx = Array();
	var default_actions = ['details', 'edit', 'delete'];
	for (i in default_actions) {
		action = default_actions[i];
		if (action in oc(actions)) {
			link = A({'href': action+'id='+id}, action.capitalize())
			lnx = lnx.concat(SPAN(null, [link, '\n']));
		}
	}
	return [lnx, '\n'];
}//function _getListTableActions(actions, id)

/*
Function from
http://snook.ca/archives/javascript/testing_for_a_v/
for finding out if a string is in the values of array a by replacing the keys as values and values as keys;
*/
function oc(a) {
  var o = {};
  for(var i=0;i<a.length;i++)
  {
    o[a[i]]='';
  }
  return o;
}//function oc(a)

