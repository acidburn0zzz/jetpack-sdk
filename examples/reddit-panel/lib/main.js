var data = require("self").data;

var reddit_panel = require("panel").Panel({
  width: 240,
  height: 320,
  contentURL: "http://www.reddit.com/.mobile?keep_extension=True",
  contentScriptFile: [data.url("jquery-1.4.2.min.js"),
                      data.url("panel.js")]
});

reddit_panel.port.on("click", function(url) {
  require("tabs").open(url);
});

require("widget").Widget({
  id: "open-reddit-btn",
  label: "Reddit",
  contentURL: "http://www.reddit.com/static/favicon.ico",
  panel: reddit_panel
});
