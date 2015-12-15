var times = 0;
//加载的js
$(document).ready(function() {
    init();



    getAllState();
    newState();
    searchState();
    serachFriend();
});

//初始化函数
function init() {
    $("#create_state_title_error").hide();
}


function newState() {
    var state_title = $("#create_state_title").val();
    var state_detail = $("#create_state_detail").val();
    $("#submit_state_btn").click(function(event) {
        if (state_title.length < 0) {
            $("#create_state_title_error").show();
            window.location.reload();
        } else {
            fileupload();
        }
    });

}



function fileupload() {
    var picURL = '';
    var state_title = $("#create_state_title").val();
    var state_detail = $("#create_state_detail").val();
    if ($("#up_img_WU_FILE_0").val()) {
        $("#up_img_WU_FILE_1").ajaxSubmit(function(message) {
            data = JSON.parse(message);
            picURL = data['content'];
            statePost(state_title, state_detail, picURL);
        });
    } else {
        statePost(state_title, state_detail, '');
    }
}

function statePost(title, detail, pic_URL) {
    jQuery.ajax({
        url: '/discover/create',
        type: 'POST',
        dataType: 'json',
        data: {
            'topic_title': title,
            'topic_content': detail,
            'topic_pic': pic_URL
        },
        success: function(data, textStatus, xhr) {
            if (data['code'] == 200) {
                $("#create_state_title_error").removeClass('alert-danger');
                $("#create_state_title_error").attr('class', 'alert alert-success showing')
                $("#create_state_title_error").html("success");
                $("#create_state_title_error").show();
                times=times-1;
                getAllState();
                console.log('get');

                setTimeout(function() {
                    $("#create_state_title_error").hide();
                    $("#create_new_invite").hide();
                    $(".create_state").hide();
                    $(".find_friend").hide();
                    $("#friend_state").show();
                    $(".container_friend").hide();
                    $("#search_state_list").hide();
                }, 1000);
            } else {
                $("#create_state_title_error").html(data['content']);
                $("#create_state_title_error").show();
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            $("#create_state_title_error").html("Network Error!");
            $("#create_state_title_error").show();
        }
    });

}

function searchState() {
    $("#search_state_btn").click(function(event) {
        /* Act on the event */
        var search_title = $("#search_state_tag").val();
        if (search_title.length < 1) {
            $("#search_state_tag").val("You must input something");
        } else {
            jQuery.ajax({
                url: '/discover/search/state',
                type: 'POST',
                data: {
                    'topic_title': search_title
                },
                success: function(data, textStatus, xhr) {
                    $("#discover_state_list").html(data);
                    other();
                    addLike();
                    $("#search_state_list").show();
                    $(".create_state").hide();
                    $(".container_friend").hide();
                    $(".find_friend").hide();
                    $("#friend_state").hide();
                },
                error: function(xhr, textStatus, errorThrown) {
                    $("#discover_state_list").html('Network Error!');
                }
            });

        }
    });
}


function serachFriend() {
    var gender = $("#gender").val();
    if (gender == "Gender") {
        gender = "";
    }
    $("#find_friend_btn").click(function(event) {
        /* Act on the event */
        jQuery.ajax({
            url: '/discover/search/friends',
            type: 'POST',
            data: {
                'name': $("#search_username").val(),
                'gender': gender,
                'campus': $("#search_campus").val(),
                'school': $("#search_school").val(),
                'user_enjoyment': $("#search_user_tag").val()
            },
            success: function(data, textStatus, xhr) {
                $("#serach_friend_list").html(data);
                friend_list_js()
                $(".container_friend").show();
                $(".create_state").hide();
                $(".find_friend").hide();
                $("#search_state_list").hide();
                $("#friend_state").hide();
            },
            error: function(xhr, textStatus, errorThrown) {
                $("#serach_friend_list").html('Network Error!');
            }
        });

    });
}

function getAllState() {
    jQuery.ajax({
        url: '/discover/discover_page',
        type: 'POST',
        data: {
            'times': times
        },
        success: function(data, textStatus, xhr) {
            // console.log(data);
            $("#discover_state_all").html(data);

            // other();
            // friendtState();
            AllStatezhan();
            addLike();
            times = times + 1;

        },
        error: function(xhr, textStatus, errorThrown) {
        }
    });
};

function AllStatezhan() {
    var opened = false;
    $('#discover_state_all > div.uc-container').each(function(i) {
        var $item = $(this),
            direction;
        switch (i % 12) {
            case 0:
                direction = ['right', 'bottom'];
                break;
            case 1:
                direction = ['right', 'bottom'];
                break;
            case 2:
                direction = ['left', 'bottom'];
                break;
            case 3:
                direction = ['left', 'bottom'];
                break;
            case 4:
                direction = ['top', 'right'];
                break;
            case 5:
                direction = ['bottom', 'right'];
                break;
            case 6:
                direction = ['top', 'left'];
                break;
            case 7:
                direction = ['bottom', 'left'];
                break;
            case 8:
                direction = ['right', 'top'];
                break;
            case 9:
                direction = ['right', 'top'];
                break;
            case 10:
                direction = ['left', 'top'];
                break;
            case 11:
                direction = ['left', 'top'];
                break;
        }
        var pfold = $item.pfold({
            folddirection: direction,
            speed: 200,
            onEndFolding: function() {
                opened = false;
            },
            centered: true
        });
        $item.find('span.icon-certificate').on('click', function() {
            if (!opened) {
                opened = true;
                pfold.unfold();
            }
        }).end().find('span.icon-remove').on('click', function() {
            pfold.fold();
        });
    });
};

function friendtState() {
    // say we want to have only one item opened at one moment
    var opened = false;
    $('#discover_state_friend > div.uc-container').each(function(i) {
        var $item1 = $(this),
            direction;
        switch (i % 8) {
            case 0:
                direction = ['right', 'bottom'];
                break;
            case 1:
                direction = ['right', 'bottom'];
                break;
            case 2:
                direction = ['left', 'bottom'];
                break;
            case 3:
                direction = ['left', 'bottom'];
                break;
            case 4:
                direction = ['right', 'top'];
                break;
            case 5:
                direction = ['right', 'top'];
                break;
            case 6:
                direction = ['left', 'top'];
                break;
            case 7:
                direction = ['left', 'top'];
                break;
        }
        var pfold = $item1.pfold({
            folddirection: direction,
            speed: 300,
            onEndFolding: function() {
                opened = false;
            },
            // centered : true
        });
        $item1.find('span.icon-certificate').on('click', function() {
            if (!opened) {
                opened = true;

                pfold.unfold();
            }
        }).end().find('span.icon-remove').on('click', function() {
            pfold.fold();
        });
    });
};

function other() {
    // say we want to have only one item opened at one moment
    var opened = false;
    $('#discover_state_list > div.uc-container').each(function(i) {
        var $item1 = $(this),
            direction;
        switch (i % 4) {
            case 0:
                direction = ['right', 'bottom'];
                break;
            case 1:
                direction = ['right', 'bottom'];
                break;
            case 2:
                direction = ['left', 'bottom'];
                break;
            case 3:
                direction = ['left', 'bottom'];
                break;
        }
        var pfold = $item1.pfold({
            folddirection: direction,
            speed: 300,
            onEndFolding: function() {
                opened = false;
            },
            // centered : true
        });
        $item1.find('span.icon-certificate').on('click', function() {
            if (!opened) {
                opened = true;
                pfold.unfold();
            }
        }).end().find('span.icon-remove').on('click', function() {
            pfold.fold();
        });
    });
};

function friend_list_js() {

    var a = new sHover("friend_item", "friend_cover");
    a.set({
        slideSpeed: 5,
        opacityChange: true,
        opacity: 80
    });
};

function refresfLike(topic_id){
    jQuery.ajax({
      url: '/discover/join',
      type: 'GET',
      dataType: 'json',
      data: {'topic_id': topic_id},
      success: function(data, textStatus, xhr) {
        //called when successful
        if(data['code'] == 200){
                    var htmlInsert = "";
                    for (var i = 0; i < data['content'].length; i++) {
                        htmlInsert+="<a href='/user/userinfo/"+data['content'][i]['uid']+"'>"+data['content'][i]['name']+",</a>";
                    };
                    $("p[value='"+topic_id+"']").html(htmlInsert);
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        //called when there is an error
      }
    });
    
}

function addLike(){
    $(".like").each(function(index, el) {
        var topic_id = $(this).attr('value');
        $(this).click(function(event) {
            jQuery.ajax({
              url: '/discover/join',
              type: 'POST',
              dataType: 'json',
              data: {'topic_id': topic_id},
              success: function(data, textStatus, xhr) {
                if(data['code'] == 200){
                    refresfLike(topic_id);
                }
              },
              error: function(xhr, textStatus, errorThrown) {
                //called when there is an error
              }
            });
            
        });
    });
}

$(function() {
    $(".icon-camera").click(function(event) {
        /* Act on the event */
        $("#warp").show('slow/400/fast');
        $("#discover_png").hide('slow/400/fast');
        $(".container_friend").hide();
        $("#friend_state").hide();
        $("#search_state_list").hide();
        $(".find_friend").hide();
    });


    $("#share_btn").click(function(event) {
        /* Act on the event */
        var x=document.getElementsByTagName("input");
        for (var i=0;i<x.length;i++) 
        { x[i].value='';}
        var y=document.getElementsByTagName("textarea");
        for (var i=0;i<y.length;i++) 
        { y[i].value='';}
        $(".create_state").show('slow/400/fast');
        $(".find_friend").hide('slow/400/fast');
        $(".container_friend").hide();
        $("#friend_state").hide();
        $("#search_state_list").hide();
    });
    $("#find_btn").click(function(event) {
        /* Act on the event */
        var x=document.getElementsByTagName("input");
        for (var i=0;i<x.length;i++) 
        { x[i].value='';}
        document.getElementsByTagName('select')[0].selectedIndex = document.getElementsByTagName('select')[0].value;
        $(".find_friend").show('slow/400/fast');
        $(".create_state").hide('slow/400/fast');
        $("#friend_state").hide();
        $("#search_state_list").hide();
        $(".create_state").hide();
    });

    $(".icon-double-angle-right").click(function(event) {
        /* Act on the event */
        console.log('here');
        getAllState();
        // window.location.reload();
    });
});
$(function() {
    $("#menu .home").removeClass("home");
    $($("#menu .bar").get(3)).addClass("home");
});


