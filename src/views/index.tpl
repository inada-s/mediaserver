% include('header.tpl')
<body>

<div class="container">
<form class="navbar-form navbar-right" role="search">
<div class="form-group">
    <input type="text" class="form-control" placeholder="Search">
</div>
<button type="submit" class="btn btn-default">
    <span class="glyphicon glyphicon-search"></span>
</button>
<button type="submit" class="btn btn-default">
    <span class="glyphicon glyphicon-plus"></span>
</button>
</form>
</div>

<div class="container">
<table class="table">
 <tbody>
% for mp4 in mp4list:
      <tr>
        <td><img src="http://www.officetanaka.net/sample.jpg" class="img-thumbnail" width="200"></td>
        <td><h3>{{mp4.name}}</h3></td>
      </tr>
% end
    </tbody>
</table>

<nav>
  <ul class="pagination">
    <li>
      <a href="#" aria-label="Previous">
        <span aria-hidden="true">&laquo;</span>
      </a>
    </li>
    <li><a href="#">1</a></li>
    <li><a href="#">2</a></li>
    <li><a href="#">3</a></li>
    <li><a href="#">4</a></li>
    <li><a href="#">5</a></li>
    <li>
      <a href="#" aria-label="Next">
        <span aria-hidden="true">&raquo;</span>
      </a>
    </li>
  </ul>
</nav>

</div>


</body>
% include('footer.tpl')