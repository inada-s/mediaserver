% include('header.tpl')
<body>

<div class="container">
<form class="navbar-form navbar-right" role="search" action="/mediasv/index">
<div class="form-group">
    <input type="text" name="search" class="form-control" placeholder="Search" value="{{search}}">
</div>
<button type="submit" class="btn btn-default" formmethod="get">
    <span class="glyphicon glyphicon-search"></span>
</button>
</form>
</div>

<div class="container">
<table class="table">
 <tbody>
% for mp4 in mp4list:
      <tr>
        <td><img src="{{mp4.thumb}}" class="img-thumbnail" width="300"></td>
        <td>
          <h3><a href="{{mp4.playpath}}" type="video/mp4">{{mp4.name}}</a></h3>
	  <p>{{"%.2f GB" % (float(mp4.size)/1024.0/1024.0/1024.0)}}</p>
	  <p>{{mp4.ctime}}</p>
	</td>
      </tr>
% end
    </tbody>
</table>

<nav>
  <ul class="pagination">
    <li>
      <a href="/mediasv/index?page={{str(max(1, page - 1)) + search_query}}" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
% for i in xrange(maxpage):
    <li><a href="/mediasv/index?page={{str(i + 1) + search_query}}">{{i + 1}}</a></li>
% end
    <li>
    <a href="/mediasv/index?page={{str(min(page + 1, maxpage)) + search_query}}" aria-label="Next">
      <span aria-hidden="true">&raquo;</span>
    </a>
    </li>
  </ul>
</nav>

</div>


</body>
% include('footer.tpl')
