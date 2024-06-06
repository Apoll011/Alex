(function ($) {
  'use strict';
  $(function () {
    $(".nav-settings").on("click", function () {
      $("#right-sidebar").toggleClass("open");
    });
    $(".settings-close").on("click", function () {
      $("#right-sidebar,#theme-settings").removeClass("open");
    });

    $("#settings-trigger").on("click", function () {
      $("#theme-settings").toggleClass("open");
    });
    $("#settings-trigger-from-profile").on("click", function () {
      $("#theme-settings").toggleClass("open");
    });

  });
})(jQuery);
