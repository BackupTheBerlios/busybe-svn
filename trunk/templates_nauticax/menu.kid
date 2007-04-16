<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
	<title> ${title} [8layer Technologies] </title>

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

	-->
	</style>

	<script type="text/javascript">
		/*
		addLoadEvent(function(){
				connect('show_mod_list','onclick', function (e) {
					e.preventDefault();
					var d = loadJSONDoc("${std.url('/index', tg_format='json')}");
					d.addCallback(showModuleList);
				});
		});

		addLoadEvent(function(){
				connect('hide_mod_list','onclick', function (e) {
					e.preventDefault();
					var d = loadJSONDoc("${std.url('/index', tg_format='json')}");
					d.addCallback(hideModuleList);
				});
		});
		*/

		function showModuleList(result) {
			var mod_list = UL(null, map(mod_display, result['modules'], result['labels']));
			replaceChildNodes('module_list', mod_list);
		}//function showModuleList(result)
		function mod_display(module, label) {
			return LI(null, A({'href': "${std.url('/')}" + module}, label));
		}//function mod_display(module)

		function hideModuleList(result) {
			replaceChildNodes('module_list', '');
		}//function hideModuleList(result)

		function hideModList() {
			replaceChildNodes('module_list', '');
		}//function hideModList()

	</script>
</head>

<body>

<div id="main_menu">

<li py:def="display_mod(module, label)">
	<a href="${module}">${label}</a>
</li>

<ul>
	${map(display_mod, modules, labels)}
</ul>

</div>

</body>
</html>
