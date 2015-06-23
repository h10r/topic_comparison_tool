
$(document).ready(function(){

  function load_topic_comparison( SCALE_FACTOR ) {
    $("#topic_module").empty();

    var width = 1170,
        height = 900,
        center = [width / 2, height / 2];

    var projection = d3.geo.mercator()
        .translate([width / 2, height / 2])
        .scale(5* (width - 1) / 2 / Math.PI);

    var zoom = d3.behavior.zoom()
        .on("zoom", zoomed);

    var path = d3.geo.path()
        .projection(projection);

    var svg = d3.select("#topic_module").append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g");

    var g = svg.append("g");

    svg.append("rect")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height);

    svg
        .call(zoom)
        .call(zoom.event);

    g.selectAll("text.topics_a")
      .data( window.topics_a )
      .enter().append( "text" )
      .attr( "class", "topic_a" )
      .attr( "fill", "#E74C3C" )
      .attr( "fill-opacity", 1.0 )
      .attr( "x", function(d) { return SCALE_FACTOR*d.x; } )
      .attr( "y", function(d) { return SCALE_FACTOR*d.y; } )
      .style("font-size","10px")
      .text( function(d) { return d.title; } )
    
    g.selectAll("text.topics_b")
      .data( window.topics_b )
      .enter().append( "text" )
      .attr( "class", "topic_b" )
      .attr( "fill", "#E67E22" )
      .attr( "fill-opacity", 1.0 )
      .attr( "x", function(d) { return SCALE_FACTOR*d.x; } )
      .attr( "y", function(d) { return SCALE_FACTOR*d.y; } )
      .style("font-size","10px")
      .text( function(d) { return d.title; } )

    g.selectAll("text.topics_i")
      .data( window.topics_i )
      .enter().append( "text" )
      .attr( "class", "topic_i" )
      .attr( "fill", "white" )
      .attr( "fill-opacity", 1.0 )
      .attr( "x", function(d) { return SCALE_FACTOR*d.x; } )
      .attr( "y", function(d) { return SCALE_FACTOR*d.y; } )
      .style("font-size","10px")
      .text( function(d) { return d.title; } )

    function zoomed() {
      g.attr("transform", "translate(" + zoom.translate() + ")scale(" + zoom.scale() + ")");
    }

    d3.select(self.frameElement).style("height", height + "px");

    var intervalID;
    var topic_a_is_visible = true;
    var topic_b_is_visible = true;
    var topic_i_is_visible = true;

    d3.select('#button_zoom_in').on('mousedown', function() {
        var factor = 1.1;
        intervalID = setInterval(zoom_by, 40, factor);
    });

    d3.select('#button_zoom_in').on('mouseup', function() {
        clearInterval(intervalID);
        intervalID = undefined;
    });

    d3.select('#button_zoom_out').on('mousedown', function() {
        var factor =  1/1.1;
        intervalID = setInterval(zoom_by, 40, factor);
    });

    d3.select('#button_zoom_out').on('mouseup', function() {
        clearInterval(intervalID);
        intervalID = undefined;
    });

    d3.select('#button_toggle_topic_a').on('click', function() {
        if ( topic_a_is_visible) {
            d3.selectAll(".topic_a").style( "fill-opacity", 0.0);
        } else {
            d3.selectAll(".topic_a").style( "fill-opacity", 1.0);
        }

        topic_a_is_visible = !topic_a_is_visible;
    });

    d3.select('#button_toggle_topic_b').on('click', function() {
        if ( topic_b_is_visible ) {
            d3.selectAll(".topic_b").style( "fill-opacity", 0.0);
        } else {
            d3.selectAll(".topic_b").style( "fill-opacity", 1.0);
        }

        topic_b_is_visible = !topic_b_is_visible;
    });

    d3.select('#button_toggle_topic_i').on('click', function() {
        if ( topic_i_is_visible ) {
            d3.selectAll(".topic_i").style( "fill-opacity", 0.0);
        } else {
            d3.selectAll(".topic_i").style( "fill-opacity", 1.0);
        }

        topic_i_is_visible = !topic_i_is_visible;
    });

    function zoom_by(factor){
        var scale = zoom.scale(),
            extent = zoom.scaleExtent(),
            translate = zoom.translate(),
            x = translate[0], y = translate[1],
            target_scale = scale * factor;

        // If we're already at an extent, done
        if (target_scale === extent[0] || target_scale === extent[1]) { return false; }
        // If the factor is too much, scale it down to reach the extent exactly
        var clamped_target_scale = Math.max(extent[0], Math.min(extent[1], target_scale));
        if (clamped_target_scale != target_scale){
            target_scale = clamped_target_scale;
            factor = target_scale / scale;
        }

        // Center each vector, stretch, then put back
        x = (x - center[0]) * factor + center[0];
        y = (y - center[1]) * factor + center[1];

        // Enact the zoom immediately
        zoom.scale(target_scale)
            .translate([x,y]);
        zoomed();
    }
  }

  function save_topics_in_window_scope( topics_a, topics_b, topics_i ) {
    window.topics_a = topics_a;
    window.topics_b = topics_b;
    window.topics_i = topics_i;
  }

  function get_scale_factor_and_load_topic_comparison() {
    var current_scale_factor = $("#input_scale_factor").val();

    load_topic_comparison( current_scale_factor );
  }

  $("#input_scale_factor").change( function() {
    var scale_element = $("#input_scale_factor");
    var current_scale_factor = parseFloat( scale_element.val() );
    load_topic_comparison( current_scale_factor );
  });

  $("#button_scale_in").click(function() {
    change_scale_factor_by( -0.001 );
  });

  $("#button_scale_out").click(function() {
    change_scale_factor_by( +0.001 );
  });

  function change_scale_factor_by( value ) {
    var scale_element = $("#input_scale_factor");
    var current_scale_factor = parseFloat( scale_element.val() );

    current_scale_factor = current_scale_factor + value;

    scale_element.val( current_scale_factor );

    load_topic_comparison( current_scale_factor );
  }

  $("#button_load_file").click(function() {
    var new_filename = $("#input_load_file").val();
    
    //var new_filepath = "/json/" + new_filename + ".json";

    $.getJSON( new_filename, function(topics) {
      save_topics_in_window_scope( topics["topics_a"] , topics["topics_b"], topics["topics_i"] );
      get_scale_factor_and_load_topic_comparison();
    })
  
  });


  $.getJSON( "http://hen-drik.de/topic_comparison_tool/json/game_of_thrones.json", function(topics) {
    save_topics_in_window_scope( topics["topics_a"] , topics["topics_b"], topics["topics_i"] );
    get_scale_factor_and_load_topic_comparison();
  })
  
})