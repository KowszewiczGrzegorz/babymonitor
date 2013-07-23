var volsteps = 5;
var urlroot = location.protocol + '//' + location.host + '/';

function execAjax(action, args) {
    url = urlroot + "audio?cmd=" + action;
    if ( args ) {
        url = urlroot + "audio?cmd=" + action + "&args=" + args;
    };
    $.ajax({
            url: url,
            error: function(data, exception) {
                console.log(exception);
            },
    });
};

function updateVolumeDisplay() {
    $.getJSON(urlroot + "audio?cmd=status", function(stat) {
        $("#currentvol").text(stat.volume);
        $("#volumebar").css({ "width": stat.volume + "%"});
    });
};

function updateCurrentPlay() {
    $("#currentplaystateicon").remove()
    $.getJSON(urlroot + "audio?cmd=status", function(stats) {
        if ( stats.status !== "stop" ) {
            $("#currentplaystate").append('<i class="icon-' + stats.status + '" id="currentplaystateicon"></i>');
            $("#currenttitle").text(stats.current);
            
        } else {
            $("#currentplaystate").append('<i class="icon-stop" id="currentplaystateicon"></i>');
            $("#currenttitle").text("Playback stopped");
        };
    });
};

// main function
$(document).ready(function() {
    var simplecommands = [ "play", "stop", "volume", "status" ];
    var updateplay = [ "play", "stop" ];

    // current volume
    updateVolumeDisplay()
    // current playback
    updateCurrentPlay()

    // audio controller
    $('button[id^="audio"]').click(function(event) {
        var clickedbutton = this.id.split("-")[1];
        if ( $.inArray(clickedbutton, simplecommands) > -1 ) {
            execAjax(clickedbutton);
        };
    
        if ( $.inArray(clickedbutton, updateplay) > -1 ) {
            updateCurrentPlay();
        };

    });

    // volume change
    $('button[id^="vol"]').click(function(event) {
        var buttonID = this.id
        $.getJSON(urlroot + "audio?cmd=status", function(stats) {
            var currentvol = parseInt(stats.volume);
            if (buttonID === "volup") {
                execAjax("setvolume", (currentvol + volsteps));
            } else if (buttonID === "voldown") {
                execAjax("setvolume", (currentvol - volsteps));
            };
            updateVolumeDisplay();
        });

    });
});
