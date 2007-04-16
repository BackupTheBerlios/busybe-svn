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
	<link rel="stylesheet" type="text/css" href="/static/css/nauticax2.css" />
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
<div class="main">
  <div class="header">
  <div class="header-top">
    <div class="search-box">
      <input name="textfield" type="text" class="search-input" />
    </div>
	<div class="login-bg">
	<span py:if="session.has_key('user')">
		<a href="/" title="Home">Home</a> ::
		<a href="logout" title="Logout">Logout</a>
	</span>
	<span py:if="not session.has_key('user')">
		<a href="/" title="Home">Home</a> ::
		<a href="login" title="Login">Login</a>
	</span>
	</div>
  </div>
  <div class="header-bottom">
  <div id="navcontainer">
	  <ul>
		  <li><a href="/" title="Home">Home</a></li>
		  <li><a href="call_type">Call Type</a></li>
		  <li><a href="community">Group</a></li>
		  <li><a href="event">Event</a></li>
		  <li><a href="inbound">Inbound</a></li>
		  <li><a href="outbound">Outbound</a></li>
		  <li><a href="person">Person</a></li>
		  <li><a href="user">User</a></li>
	  </ul>
      </div>
  </div>
  </div><!-- header -->
  <div class="body-main">
  <div class="body-top">
	  <div class="box">

<h1>${head}</h1>

<div py:if="tg_flash" class="flash" py:content="tg_flash"></div>

<div py:replace="[item.text]+item[:]"/>

	  </div>
  </div><!-- body-top -->
  <div class="body-bottom">
    <div class="bottom-box1">
		<div class="bottom-box1-inside">
			<span class="title-14">BusyBe Sample Project</span>
			<div>This is a sample busybe project.</div>
			<div>You can also replace the photo if you want.</div>
		   <div class="bottom-box-th"><img src="/static/images/nauticax2/my-space-th.jpg" alt="" width="165" height="79" /></div>
			<div>You can insert any text here.</div>
		   <div class="green-link-box"><a href="#" class="read-more">Or insert links More </a></div>
		</div>
     </div>

	  <div class="bottom-box1">
      <div class="bottom-box1-inside"><span class="title-14">Creative Blogs </span>
	    <div>Here is where the details of your
		   projects and specs will go.</div>
		   <div class="bottom-box-th"><img src="images/design-award-th.jpg" alt="" width="165" height="79" /></div>
		   <div class="green-link-box"><a href="#" class="read-more">View Gallery </a></div>
	  </div>
	  </div>

	  <div class="bottom-box1" style="border-right:none;">
      <div class="bottom-box1-inside"><span class="title-14">Idea Boards </span>
	    <div>Here is where the details of your
		   projects and specs will go.</div>
		   <div class="bottom-box-th"><img src="/static/images/nauticax2/about-us-th.jpg" alt="" width="165" height="79" /></div>
		   <div class="green-link-box"><a href="#" class="read-more">Comments</a></div>
	  </div>
	  </div>
  </div><!-- body-bottom -->
  </div><!-- body-main -->
  <div class="footer">
	<span py:if="session.has_key('user')">
		Welcome ${session['user']} |
		<a href="/" title="Home" class="footer-link">Home</a> |
		<a href="logout" title="Logout" class="footer-link">Logout</a> |
		<a href="login" title="Login" class="footer-link">Change User</a>
	</span>
	<span py:if="not session.has_key('user')">
		<a href="/" title="Home" class="footer-link">Home</a> |
		<a href="login" title="Login" class="footer-link">Login</a>
	</span>
  </div>
</div><!-- main -->

<!-- End of main_content -->

</body>

</html>
