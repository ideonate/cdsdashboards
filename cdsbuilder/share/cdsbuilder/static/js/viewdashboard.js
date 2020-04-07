require(["jquery"], function($) {
    "use strict";
  
    // hook up event-stream for progress
    var evtSource = new EventSource(dashboard_progress_url);

    
    evtSource.onmessage = function(e) {
        var evt = JSON.parse(e.data);
        console.log(evt);


        if (evt.ready || evt.failed) {
            evtSource.close();
            
            console.log("Close progress eventstream");
        }
    }

  });

  