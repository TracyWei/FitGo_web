function toNew(){
    $('#after-show').show('slow/400/fast');
    $('html, body').animate({scrollTop:0}, 'slow');
}
function refrshJoin(act_id){
    jQuery.ajax({
      url: '/activity/add',
      type: 'GET',
      data: {'act_id': act_id},
      success: function(data, textStatus, xhr) {
        $("#"+act_id).html(data);
      },
      error: function(xhr, textStatus, errorThrown) {
        alert(xhr);
        alert(textStatus);
        alert(errorThrown);
        $("#"+act_id).html("Error!");
      }
    });
};

function addJoin(){
    // alert("hello1");
    $(".join").click(function(event) {
        /* Act on the event */
        var act_id = $(this).attr('value');
        jQuery.ajax({
                  url: '/activity/add',
                  type: 'POST',
                  dataType: 'json',
                  data: {
                    'uid': $("#uid").attr('value'),
                    'act_id':act_id
                        },
                  success: function(data, textStatus, xhr) {
                    refrshJoin(act_id);
                  },
                  error: function(xhr, textStatus, errorThrown) {
                  }
                });

    });
};


function refresh(){
    jQuery.ajax({
      url: '/activity',
      type: 'POST',
      data: {'length': 'value1'},
      success: function(data, textStatus, xhr) {
            divContent = $("#cd-timeline");
            divContent.html(data);
            addJoin();
    },
      error: function(xhr, textStatus, errorThrown) {
        $("#error_message_content").val("Network Error!");
        $("#error_message").show("slow");
      }
    });
    
}

function search(){
    var location = $("#options-search").val();
    if(location=='Location'){location='';}
    var start_time = $("#Start-Time-Search").val();
    var title=$("#search_title").val();
    if(!start_time&&!location&&!title){
    }
    else{
        console.log(start_time)
        jQuery.ajax({
          url: '/activity/search',
          type: 'POST',
          data: {
            'act_title': title,
            'start_time':start_time,
            'location':location
        },
          success: function(data, textStatus, xhr) {
            //called when successful
            divContent = $("#cd-timeline");
            divContent.html(data);
            addJoin();
          },
          error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
            $("#error_message_content").val("Network Error!");
            $("#error_message").show("slow");
          }
        });
        
    }

}

$(document).ready(function() {
    function init() {
        $('#hide-new').click(function(event) {
            $("#after-show").toggle('slow/4000/fast');
        });

        $("#menu .home").removeClass("home");
        $($("#menu .bar").get(2)).addClass("home");
        $('#Start-Time').datepicker('hide');
        $('#Start-Time').datepicker({
            format: 'yyyy-mm-dd'
        });

        $('#End-Time').datepicker('hide');
        $('#End-Time').datepicker({
            format: 'yyyy-mm-dd'
        });
        $('#Start-Time-Search').datepicker('hide');
        $('#Start-Time-Search').datepicker({
            format: 'yyyy-mm-dd'
        });
        $('#below').click(function(event) {
            $('#after-show').hide('slow/400/fast');
        });
        $("#toSearch").click(function(event) {
            $('#toSearch').hide();
            $('#searchText').show('slow/400/fast');
            $('.confirmSearch').show('slow/400/fast');
        });

        $("#alertPaopao").click(function(event) {
            if (!$("#uid").attr('value')) {
                $('#alertPaopao').attr("data-content", "Login First!");
                $('#alertPaopao').popover('show');
                // $('#alertPaopao').popover(options);
            } else if ($("#newActivity").val().length < 1 || $("#options").val().length < 1 || $("#activity_detail").val().length < 1) {
                $('#alertPaopao').attr("data-content", "Invalid input");
                $('#alertPaopao').popover('show');
            } else {
                var all_time = $("#reservation-start").val().split(' ')
                var start_time = all_time[0];
                var end_time=all_time[2];
                console.log(start_time+end_time);
                $.ajax({
                    url: '/activity/create',
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        'uid': $("#uid").attr('value'),
                        'act_title': $("#newActivity").val(),
                        'start_time': start_time,
                        'end_time': end_time,
                        'location': $("#options").val(),
                        'details': $("#activity_detail").val()
                    },
                    success: function(data, textStatus, xhr) {
                        if (data['code'] == 200) {
                            $('#alertPaopao').attr("data-content", "Success!");
                            $('#alertPaopao').popover('show');
                            refresh();
                            setTimeout(function(){$("#after-show").hide('slow/400/fast');},500);
                             $("#wholeNew :input").not(":button, :submit, :reset, :hidden").val("").removeAttr("checked").remove("selected");
                        } else {
                            $('#alertPaopao').attr("data-content", data['content']);
                            $('#alertPaopao').popover('show');
                        }
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        $('#alertPaopao').attr("data-content", "Network Error!");
                        $('#alertPaopao').popover('show');
                    }
                });
            }

        });
            $('#specialFliter').mouseout(function(event) {
                $('body').bind('click', function(event) {
                    $('#searchText').hide();
                    $('.confirmSearch').hide();
                    $('#toSearch').show();
                    // $('#after-show').hide();
                });
            });
            $('#specialFliter').mouseover(function(event) {
                $('body').unbind('click');
            });
    };

    $("#search_btn").click(function(event) {
        /* Act on the event */
        search();
    });

    init();
    refresh();
    addJoin();
});
