<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<?python print template_dir ?>

<head>
    <meta content="text/html; charset=UTF-8"
        http-equiv="content-type" py:replace="''"/>
	<title>${title}</title>
    <style type="text/css">
    </style>
</head>

<body>

<div id="main">

<form action="signin">
	<dl>
		<dt>Username:</dt>
		<dd><input id="user" name="user" /></dd>
		<dt>Password:</dt>
		<dd><input type="password" id="password" name="password" /></dd>
		<dt></dt>
		<dd><input type="submit" value="Login" /></dd>
	</dl>
</form>

</div><!-- main -->

</body>
</html>
