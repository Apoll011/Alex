function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min)
}

function CreateChart(data_chart, data_plot) {
  dst = []
  for (const [key, value] of Object.entries(data_chart)) {
    dst.push({
      data: value,
      borderColor: [
        `rgb(${random(0, 254)},${random(0, 254)},${random(0, 254)})`
      ],
      borderWidth: 2,
      fill: false,
      label: key.replace("_", " ")
    })
  }

  var areaData = {
    labels: ["7am", "8am", "9am", "10am", "11am", "12pm", "13pm", "14pm", "15pm", "16pm", "17pm", "18pm", "19pm", "20pm", "21pm", "22pm", "23pm", "0am", "1am", "2am", "3am", "4am", "5am", "6am", "7am"],
    datasets: dst
  };
  var areaOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      filler: {
        propagate: false
      }
    },
    scales: {
      xAxes: [{
        display: true,
        ticks: {
          display: true,
          padding: 10,
          fontColor: "#6C7383"
        },
        gridLines: {
          display: false,
          drawBorder: false,
          color: 'transparent',
          zeroLineColor: '#eeeeee'
        }
      }],
      yAxes: [{
        display: true,
        ticks: {
          display: true,
          autoSkip: false,
          maxRotation: 0,
          stepSize: 10,
          min: 0,
          max: 100,
          padding: 18,
          fontColor: "#6C7383"
        },
        gridLines: {
          display: true,
          color: "#f2f2f2",
          drawBorder: false
        }
      }]
    },
    legend: {
      display: true,
      class: "text-capitalize"
    },
    tooltips: {
      enabled: true
    },
    elements: {
      line: {
        tension: .35
      },
    }
  }
  var revenueChartCanvas = $("#functionality-chart").get(0).getContext("2d");
  var revenueChart = new Chart(revenueChartCanvas, {
    type: 'line',
    data: areaData,
    options: areaOptions
  });

  var scatterChartCanvas = $("#scatterChart").get(0).getContext("2d");
  var scatterChart = new Chart(scatterChartCanvas, {
    type: 'scatter',
    data: data_plot,
    options: {
      scales: {
        xAxes: [{
          type: 'linear',
          position: 'bottom',
          display: true,
          ticks: {
            display: true,
            autoSkip: false,
            maxRotation: 0,
            stepSize: 1,
            min: 0,
            max: 24,
            padding: 18,
            fontColor: "#6C7383"
          },
          gridLines: {
            display: true,
            color: "#f2f2f2",
            drawBorder: false
          }
        }],
        yAxes: [{
          display: true,
          ticks: {
            display: true,
            autoSkip: false,
            maxRotation: 0,
            stepSize: 10,
            min: 0,
            max: 100,
            padding: 18,
            fontColor: "#6C7383"
          },
          gridLines: {
            display: true,
            color: "#f2f2f2",
            drawBorder: false
          }
        }]
      },
      legend: {
        display: true,
        class: "text-capitalize"
      },
      tooltips: {
        enabled: true
      }
    }
  });
}



(function ($) {
  'use strict';
  $(function () {


    $.contextMenu({
      selector: '#context-menu-multi',
      autoHide: true,
      callback: function (key, options) {
        var m = "clicked: " + key + " :: ";
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

    function Notify(options, func) {
      options.onClick = func
      $("#notifications").easyNotify(options);
    }
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
