 $(document).ready(function(){
    $('.sidenav').sidenav();
    $(".collapsible").collapsible();
    $('.modal').modal();
    $("select").formSelect();
  }); 





document.addEventListener('DOMContentLoaded', function () {
let sidenavs = document.querySelectorAll(".sidenav");
let sidenavsInstance = M.Sidenav.init(sidenavs);
});