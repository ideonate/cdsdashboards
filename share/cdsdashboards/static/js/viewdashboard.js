require(["jquery"], function($) {
    "use strict";
  
    // hook up event-stream for progress
    var evtSource = new EventSource(dashboard_progress_url);

    var progressMessage = $("#progress-message");
    var progressBar = $("#progress-bar");
    var srProgress = $("#sr-progress");
    var progressLog = $("#progress-log");

    var launchA = $("#launch");
    
    evtSource.onmessage = function(e) {
        var evt = JSON.parse(e.data);

        if (evt.progress !== undefined) {
            // update progress
            var progText = evt.progress.toString();
            progressBar.attr('aria-valuenow', progText);
            srProgress.text(progText + '%');
            progressBar.css('width', progText + '%');
        }
        // update message
        var html_message;
        if (evt.html_message !== undefined) {
            progressMessage.html(evt.html_message);
            html_message = evt.html_message;
        } else if (evt.message !== undefined) {
            progressMessage.text(evt.message);
            html_message = progressMessage.html();
        }
        if (html_message) {
            progressLog.append(
                $("<div>")
                .addClass('progress-log-event')
                .html(html_message)
            );
        }
    
        if (evt.ready) {
            evtSource.close();

            window.location = evt.url;
            
//            launchA.attr('href', evt.url);
//            launchA.show();
        }
    
        if (evt.failed) {
            evtSource.close();
            // turn progress bar red
            progressBar.addClass('progress-bar-danger');
            // open event log for debugging
            $('#progress-details').prop('open', true);

            launchA.attr('href', evt.url);

            launchA.text('Try Again');

            launchA.attr('target', '');

            launchA.show();
        }

    }

  });

  