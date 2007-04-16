<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python
import sitetemplate
?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="'../master_base.kid'">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta py:replace="item[:]"/>
	<link rel="stylesheet" type="text/css" href="/static/css/busybe.css" />
	<link rel="stylesheet" type="text/css" href="/static/carbonated/default.css" />
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
<div id="header">
	<div id="logo">
		<h1><a href="#">Carbonated</a></h1>
		<h2><a href="http://www.freecsstemplates.org/">By Free CSS Templates</a></h2>
	</div>
	<div id="menu">
	<ul py:if="session.has_key('user')">
		<li class="first">Welcome ${session['user']}</li>
		<li><a href="/" title="Home">Home</a></li>
		<li><a href="logout" title="Logout">Logout</a></li>
		<li><a href="login" title="Login">Change User</a></li>
	</ul>
	<ul py:if="not session.has_key('user')">
		<li class="first"><a href="/" title="Home">Home</a></li>
		<li><a href="login" title="Login">Login</a></li>
	</ul>
	</div>
</div><!-- header -->

<div id="page">
	<div id="content">

<h1>${head}</h1>

<div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

<div py:replace="[item.text]+item[:]"/>

	</div><!-- content -->

	<div id="sidebar">
		<ul>
			<li>
				<h2>News &amp; Events</h2>
				<dl>
					<dt><strong>April 5, 2007</strong></dt>
					<dd>In posuere eleifend odio quisque semper augue mattis wisi maecenas ligula. <a href="#">More&hellip;</a></dd>
					<dt><strong>April 2, 2007</strong></dt>
					<dd>Donec leo, vivamus fermentum nibh in augue praesent a lacus at urna congue rutrum. <a href="#">More&hellip;</a></dd>
					<dt><strong>March 30, 2007</strong></dt>
					<dd>Quisque dictum integer nisl risus, sagittis convallis, rutrum id, congue, and nibh. <a href="#">More&hellip;</a></dd>
				</dl>
			</li>
			<li>
				<h2>Numbered List</h2>
				<ol>
					<li><a href="#">Ut semper vestibulum est</a></li>
					<li><a href="#">Vestibulum luctus venenatis</a></li>
					<li><a href="#">Integer rutrum nisl in mi</a></li>
					<li><a href="#">Etiam malesuada rutrum enim</a></li>
					<li><a href="#">Aenean elementum facilisis</a></li>
					<li><a href="#">Ut tincidunt elit vitae augue</a></li>
					<li><a href="#">Sed quis odio sagittis leo</a></li>
				</ol>
			</li>
			<li>
				<h2>A Sidebar's Blockquote</h2>
				<blockquote>
					<p>&ldquo;Quisque dictum integer nisl risus, sagittis convallis, rutrum id, congue, and nibh. Donec leo, vivamus fermentum nibh in augue praesent a lacus at urna congue rutrum.&rdquo;</p>
				</blockquote>
				<ul>
					<li><a href="#">Ut semper vestibulum est</a></li>
					<li><a href="#">Vestibulum luctus venenatis</a></li>
					<li><a href="#">Integer rutrum nisl in mi</a></li>
				</ul>
			</li>
		</ul>
	</div>

	<div style="clear: both;">&nbsp;</div>
</div><!-- page -->

<div id="footer">
	<p id="legal">Copyright &copy; 2007 Carbonated. All Rights Reserved. Designed by <a href="http://www.freecsstemplates.org/">Free CSS Templates</a>.</p>
	<p id="links"><a href="#">Privacy Policy</a> | <a href="#">Terms of Use</a></p>
</div>
</body>

</html>
