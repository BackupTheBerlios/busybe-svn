<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
import sitetemplate
BaseUrl = '/'
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="sitetemplate">

<!--head-->
<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'">
	<meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''" />
	<title py:replace="''">Your title goes here</title>
	<script src="/tg_js/MochiKit.js"></script>
	<script type="text/javascript">
		function requestPageList() {
			var d = loadJSONDoc("${std.url('pagelist', tg_format='json')}");
			d.addCallback(showPageList);
		}

		function showPageList(result) {
			var currentpagelist = UL(null, map(row_display, result["pages"]));
			replaceChildNodes("pagelist", currentpagelist); replaceChildNodes("pagelist", currentpagelist); 
		}

		function row_display(pagename) {
			return LI(null, A({"href" : "${std.url('./')}" + pagename}, pagename))
		}
	</script>

	<style>
	<!--
	td#page_content {
		font-family: verdana, arial, fantasy;
		font-size: 12.5pt;
	}

	a {
		color: #030;
		font-weight: bold;
		text-decoration: none;
	}
	a:hover {
		text-decoration: underline;
	}
	div#sidebar {
		float:right;
		width: 10em
	}
	div#sidebar ul {
		list-style: none;
	}
	div#sidebar ul li {
	}
	div.top_links a {
		color: #fff;
	}

	td div a {
		font-weight: bold;
		font-family: Arial;
	}
	td a {
		font-weight: bold;
		font-family: Verdana, Arial;
	}
	-->
	</style>
	<meta py:replace="item[:]" />

</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'">

    
<div py:if="tg_flash" class="flash" py:content="tg_flash"></div>
<div py:replace="item[:]" />

<!--p>View a <a href="#" onclick="requestPageList()">complete list of pages.</a></p-->
<div id="pagelist">
</div>

<!-- Shame is an improper emotion invented by pietists to oppress the human race.  -->
</body>
</html>
