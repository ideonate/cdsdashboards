require(["jquery", "jhapi", "utils"], function($, JHAPI, utils) {
    "use strict";

    var update = function(d1, d2) {
        $.map(d2, function(i, key) {
            d1[key] = d2[key];
        });
        return d1;
    };

    JHAPI.prototype.delete_dashboard = function(dashboard_name, options) {
        options = options || {};
        options = update(options, { type: "DELETE", dataType: null });
        this.api_request(
            utils.url_path_join("..", "hub", "dashboards-api", dashboard_name),
            options
        );
    };

    var base_url = window.jhdata.base_url;
    var api = new JHAPI(base_url);

    function getRow(element) {
        while (!element.hasClass("home-dashboard-row")) {
            element = element.parent();
        }
        return element;
      }

    function disableRow(row) {
        row
          .find(".btn")
          .attr("disabled", true)
          .off("click");
      }

    function deleteDashboard() {
        var row = getRow($(this));
        var dashboardName = row.data("dashboard-name");
    
        disableRow(row);
    
        api.delete_dashboard(dashboardName, {
            success: function() {
              row.remove();

              var remaining_rows = $('.dashboard-table tbody tr');
              if (remaining_rows.length == 0) {
                $('.dashboard-table').remove();
                $('#dashboards-none').removeClass('hidden');
              }

            },
        });
      }


    $(".delete-dashboard").click(deleteDashboard);

  });

  