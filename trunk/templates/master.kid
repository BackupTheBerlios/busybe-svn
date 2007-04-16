<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
import sitetemplate
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master_base.kid'">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta py:replace="item[:]"/>
	<link rel="stylesheet" type="text/css" href="/static/css/busybe.css" />
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

<!-- PAGE START -->
<div id="pageLogin">
	<span py:if="session.has_key('user')">
		Welcome ${session['user']}. ||
		<a href="/" title="Home">Home</a> ||
		<a href="logout" title="Logout">Logout</a> ||
		<a href="login" title="Login">Change User</a>
	</span>
	<span py:if="not session.has_key('user')">
		<a href="/" title="Home">Home</a> ||
		<a href="login" title="Login">Login</a>
	</span>
</div>

<h1>${head}</h1>

<div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

<div py:replace="[item.text]+item[:]"/>

<div id="footer"></div>
</body>

</html>
