(function($) {
  'use strict';
  $(function() {
    $(".nav-settings").on("click", function() {
      $("#right-sidebar").toggleClass("open");
    });
    $(".settings-close").on("click", function() {
      $("#right-sidebar,#theme-settings").removeClass("open");
    });

    $("#settings-trigger").on("click" , function(){
      $("#theme-settings").toggleClass("open");
    });
    $("#settings-trigger-from-profile").on("click" , function(){
      $("#theme-settings").toggleClass("open");
    });


    //background constants
    var navbar_classes = "navbar-danger navbar-success navbar-warning navbar-dark navbar-light navbar-primary navbar-info navbar-pink";
    var sidebar_classes = "sidebar-light sidebar-dark";
    var $body = $("body");

    //sidebar backgrounds
    $("#sidebar-light-theme").on("click" , function(){
      $body.removeClass(sidebar_classes);
      $body.addClass("sidebar-light");
      $(".sidebar-bg-options").removeClass("selected");
      $(this).addClass("selected");
    });
    $("#sidebar-dark-theme").on("click" , function(){
      $body.removeClass(sidebar_classes);
      $body.addClass("sidebar-dark");
      $(".sidebar-bg-options").removeClass("selected");
      $(this).addClass("selected");
    });


    //Navbar Backgrounds
    $(".tiles.primary").on("click" , function(){
      change_navbar("primary", this);
    });
    $(".tiles.success").on("click" , function(){
      change_navbar("success", this);
    });
    $(".tiles.warning").on("click" , function(){
      change_navbar("warning", this);
    });
    $(".tiles.danger").on("click" , function(){
      change_navbar("danger", this);
    });
    $(".tiles.light").on("click" , function(){
      change_navbar("light", this);
    });
    $(".tiles.info").on("click" , function(){
      change_navbar("info", this);
    });
    $(".tiles.dark").on("click" , function(){
      change_navbar("dark", this);
    });
    $(".tiles.default").on("click" , function(){
      $(".navbar").removeClass(navbar_classes);
      $(".tiles").removeClass("selected");
      $(this).addClass("selected");
    });

    function change_navbar(color, that){
      $(".navbar").removeClass(navbar_classes);
      $(".navbar").addClass(`navbar-${color}`);
      $(".tiles").removeClass("selected");
      $(that).addClass("selected");
    }
  });
})(jQuery);
