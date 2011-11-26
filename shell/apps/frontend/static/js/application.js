(function($) {
  var common = {
    base : "/api/v1/",
    //base : "http://radiant-meadow-2958.herokuapp.com/api/v1/",
  };

  $.shell = {};
  $.shell.player = {
    all : function() {
      return $.getJSON(common.base + "player/?callback=?");
    },
    get : function(id) {
      return $.getJSON(common.base + "player/" + id + "/?callback=?");
    },
  };
  $.shell.history = {
    get : function(id) {
      return $.getJSON(common.base + "history/" + id + "/?callback=?");
    },
    player : function(id) {
      return $.getJSON(common.base + "player/" + id + "/history/?callback=?");
    },
  };
  $.shell.trauma = {
    get : function(id) {
      return $.getJSON(common.base + "trauma/" + id + "/?callback=?");
    },
    player : function(id) {
      return $.getJSON(common.base + "player/" + id + "/trauma/?callback=?");
    },
  };
})(jQuery);

(function($) {
  Application = { };
  Application.filter = function(value) {
    // todo split value and check if any in following
    $('a.player').each(function(index) {
      var $this = $('img', this);
      var result = ($this.data('firstname').toLowerCase().indexOf(value) > -1)
                || ($this.data('lastname').toLowerCase().indexOf(value)  > -1) 
                || ($this.data('number').toString().indexOf(value)       > -1);
      if (!result) { $(this).fadeOut(); }
      else { $(this).fadeIn(); }
    });
  };

  Application.chart  = function(history) {
    var chart = new Highcharts.Chart({
      chart : {
        renderTo : 'player-chart',
        defaultSeriesType : 'line',
      },
      title : { text : 'Player History' },
      yAxis : {
        title: { text : 'Values' }
      },
      xAxis : {
        title: { text : 'Dates' },
        categories : $.map(history, function (d, i) { return d.date.split(' ')[0]; })
      },
      series : [{
        name : 'Average',
        data : $.map(history, function (d, i) { return parseFloat(d.acceleration); })
      },
      {
        name : 'Hits',
        data : $.map(history, function (d, i) { return d.hits; })
      },
      {
        name : 'Humidity',
        data : $.map(history, function (d, i) { return parseFloat(d.humidity); })
      },
      {
        name : 'Temperature',
        data : $.map(history, function (d, i) { return parseFloat(d.temperature); })
      }]
    });
  };

  Application.select = function(event) {
    $.shell.history.player(event.data.player.id).then(Application.chart);
    $('#player-dialog').dialog('option', 'title',
      event.data.player.firstname + ' ' + event.data.player.lastname);
    $('#player-dialog').dialog('open');
    // todo, covert this to template
  };

  Application.initialize = function() {
    $('#player-dialog').dialog({
      autoOpen      : false,
      closeOnEscape : true,
      title         : 'Player Information',
      width         : 940,
      height        : 500,
      position      : 'center',
      modal         : true,
      draggable     : false,
      zIndex        : 10000
    });

    $.shell.player.all().then(function(players) {
      $.each(players, function(i, player) {
        $("<img/>", {
          src     : "/static/img/player.jpg",
          //src     : "https://github.com/bashwork/shell-service/raw/master/shell/apps/frontend/static/img/player.jpg",
          alt     : player.firstname + " " + player.lastname,
          'class' : 'thumbnail',
          data    : player
        }).hide().load(function() {
          $(this).appendTo("#player-gallery")
          .bind('click', { player : player }, Application.select)
          .wrap("<a class='player'>").wrap("<li/>").fadeIn('slow');
        });
      });
    }).then(function(players) {
      var names = $.map(players, function(player, i) {
        return [
		  player.number.toString(),
          player.firstname.toLowerCase(),
		  player.lastname.toLowerCase()];
      });
      $('#player-search').keyup(function() {
        Application.filter($(this).val());
      }).autocomplete({ source : names });
    });

  };

})(jQuery);

$(document).ready(Application.initialize);
