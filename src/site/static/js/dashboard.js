function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min)
}

(function ($) {
  'use strict';
  $(function () {


    $.contextMenu({
      selector: '#context-menu-multi',
      autoHide: true,
      callback: function (key, options) {
        var m = "clicked: " + key + " :: " + $(this).contents.name;
        console.log(m);
      },
      events: {
        hide: function (opt) {
          var values = $.contextMenu.setInputValues(opt)
        }
      },
      items: {
        "edit": {
          name: "Open",
          icon: function () {
            return 'context-menu-icon ti-power-off';
          }
        },
        "cut": {
          name: "Restart",
          icon: function () {
            return 'context-menu-icon ti-reload';
          }
        },
        "copy": {
          name: "Close",
          icon: function () {
            return 'context-menu-icon ti-unlink';
          }
        },
        "sep1": "---------",
        "quit": {
          name: "Quit",
          icon: function () {
            return 'context-menu-icon context-menu-icon-quit';
          }
        }
      }
    });


  });

})(jQuery);

/*   
var table = $('#example').DataTable( {
    "ajax": "{{ url_for('static', filename='js/data.txt') }}",
    "columns": [
        { "data": "Quote" },
        { "data": "Product" },
        { "data": "Business" },
        { "data": "Policy" }, 
        { "data": "Premium" }, 
        { "data": "Status" }, 
        { "data": "Updated" }, 
        {
          "className":      'details-control',
          "orderable":      false,
          "data":           null,
          "defaultContent": ''
        }
    ],
    "order": [[1, 'asc']],
    "paging":   false,
    "ordering": true,
    "info":     false,
    "filter": false,
    columnDefs: [{
      orderable: false,
      className: 'select-checkbox',
      targets: 0
    }],
    select: {
      style: 'os',
      selector: 'td:first-child'
    }
  } );

  
*/
