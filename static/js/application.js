/**
 * Jquery monkey patching
 * - add the put ajax helper method
 */
(function($) {

  $.put = function(url, data) {
    return $.ajax({
      type     : 'put',
      url      : url,
      data     : data,
      dataType : 'json'
    });
  };

})(jQuery);

/**
 * API wrapper for the shell platform
 * - TODO convert to template and generate development/production
 */
(function($) {
  var common = {
    api : {
      base : "/api/v1/"
    },
    //base : "http://radiant-meadow-2958.herokuapp.com/api/v1/",
    template : {
      base : '/template/',
      compiled : {}
    }
  };

  $.shell = {};
  $.shell.template = {
    initialize : function(name) {
      name = name.replace('.', '/');
      $.get(common.template.base + name + '/', function(result) {
        common.template.compiled[name] = _.template(result);
      });
    },
    compile : function(name, context) {
      name = name.replace('.', '/');
      return common.template.compiled[name](context);
    }
  };
  $.shell.player = {
    all : function() {
      return $.getJSON(common.api.base + "player/?callback=?");
    },
    get : function(id) {
      return $.getJSON(common.api.base + "player/" + id + "/?callback=?");
    },
    create : function(data) {
      return $.post(common.api.base + "player/?callback=?", data);
    },
    update : function(data) {
      return $.put(common.api.base + "player/" + data.id + "/?callback=?", data);
    },
    trauma : function(id) {
      return $.getJSON(common.api.base + "player/" + id + "/trauma/?callback=?");
    },
    history : function(id) {
      return $.getJSON(common.api.base + "player/" + id + "/history/?callback=?");
    }
  };
  $.shell.contact = {
    all : function() {
      return $.getJSON(common.api.base + "contact/?callback=?");
    },
    get : function(id) {
      return $.getJSON(common.api.base + "contact/" + id + "/?callback=?");
    },
    create : function(data) {
      return $.post(common.api.base + "contact/?callback=?", data);
    },
    update : function(data) {
      return $.put(common.api.base + "contact/" + data.id + "/?callback=?", data);
    }
  };
  $.shell.history = {
    get : function(id) {
      return $.getJSON(common.api.base + "history/" + id + "/?callback=?");
    },
    create : function(data) {
      return $.post(common.api.base + "history/?callback=?", data);
    },
    update : function(data) {
      return $.put(common.api.base + "history/" + data.id + "/?callback=?", data);
    }
  };
  $.shell.trauma = {
    get : function(id) {
      return $.getJSON(common.api.base + "trauma/" + id + "/?callback=?");
    },
    create : function(data) {
      return $.post(common.api.base + "trauma/?callback=?", data);
    },
    update : function(data) {
      return $.put(common.api.base + "trauma/" + data.id + "/?callback=?", data);
    }
  };
})(jQuery);

/**
 * Web application code
 */
(function($) {
  Application = { };
  /**
   * filter view of current players on main page
   */
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

  /**
   * Toggle player information chart
   */
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

  /**
   * Toggle player information view
   */
  Application.select = function(event) {
    $.shell.player.history(event.data.player.id).then(Application.chart);
    $('#player-information').html(
      $.shell.template.compile('player.information', event.data));
    $('#player-dialog').dialog('option', 'title',
      event.data.player.firstname + ' ' + event.data.player.lastname);
    $('#player-dialog').dialog('open');
  };

  /**
   * Initialize the web application
   */
  Application.initialize = function() {
    /**
     * Initialize information dialog
     */
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

    /**
     * Initialize players for the front page:
     * - auto suggest initialize
     * - main helmet view initialize
     */
    $.shell.player.all().then(function(players) {
      $.each(players, function(i, player) {
        $("<img/>", {
          //src     : "/static/img/player.jpg",
          src     : "http://bashwork.github.com/shell-service/static/img/player.jpg",
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

    /**
     * Initialize templates for front page
     */
    _.templateSettings = { interpolate : /\{\{(.+?)\}\}/g };
    $.shell.template.initialize('player.information');
    $.shell.template.initialize('contact.information');
  };

})(jQuery);

/**
 * Start the web application
 */
$(document).ready(Application.initialize);
