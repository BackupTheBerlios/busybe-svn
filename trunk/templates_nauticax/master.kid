<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
import sitetemplate
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master_base.kid'">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]"/>

	<link rel="stylesheet" type="text/css" href="/static/css/busybe.css" />
	<link rel="stylesheet" type="text/css" href="/static/css/nauticax.css" />
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">

<!-- PAGE START -->
<div id="outer-wrapper">

<div id="inner-wrapper">

<div id="content-wrapper">

	<div id="content">

		<form name="search" action="" id="search-form">
		</form>

		<ul py:if="session.has_key('user')" id="nav">
			<li><a>Welcome ${session['user']}</a></li>
			<li><a href="/" title="Home">Home</a></li>
			<li><a href="logout" title="Logout">Logout</a></li>
			<li><a href="login" title="Login">Change User</a></li>
		</ul>
		<ul py:if="not session.has_key('user')" id="nav">
			<li><a href="/" title="Home">Home</a></li>
			<li><a href="login" title="Login">Login</a></li>
		</ul>

		<div id="content-inner">
			<h1>${head}</h1>

			<div class="content-right">
			<div py:if="tg_flash" class="flash" py:content="tg_flash"></div>
			</div><!-- content-right -->

			<div class="content-full">
			<div py:replace="[item.text]+item[:]"/>
			</div><!-- content-full -->

		</div><!-- content-inner -->

	</div><!-- content -->

	<div id="sidebar">
		<div id="logo">
			<img src="/static/images/logo.gif" alt="Logo Here" />
		</div><!-- logo -->

		<h4>Main menu</h4>
		<ul class="side-nav">
			<!-- Admin
			<li><a href="/access_level">Access Level</a></li>
			<li><a href="/permission">Permission</a></li>
			-->
			<li><a href="/call_type">Call Type</a></li>
			<li><a href="/community">Group</a></li>
			<li><a href="/event">Event</a></li>
			<li><a href="/inbound">Inbound</a></li>
			<li><a href="/membership">Membership</a></li>
			<li><a href="/outbound">Outbound</a></li>
			<li><a href="/participant">Participant</a></li>
			<li><a href="/person">Person</a></li>
			<li><a href="/user">User</a></li>
		</ul>

		<h4>Test menu</h4>
		<ul class="side-nav">
			<li><a href="#">Test item</a></li>
		</ul>
	</div><!-- sidebar -->

</div><!-- content-wrapper -->
<!-- End of main_content -->

<div id="footer">
	<ul py:if="session.has_key('user')" id="footer-nav">
		<li><a href="/" title="Home">Home</a></li>
		<li><a href="logout" title="Logout">Logout</a></li>
		<li><a href="login" title="Login">Change User</a></li>
		<li class="last"><a>Logged in as ${session['user']}</a></li>
	</ul>
	<ul py:if="not session.has_key('user')" id="footer-nav">
		<li><a href="/" title="Home">Home</a></li>
		<li class="last"><a href="login" title="Login">Login</a></li>
	</ul>
	<p class="copyright">
	Sample <a href="http://busybe.berlios.de/">BusyBe</a> application.
	</p>
</div>

</div><!-- inner-wrapper -->

</div><!-- outer-wrapper -->
</body>

</html>
