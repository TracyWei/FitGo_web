function item_click() {

    var //记录当前已经添加active类的li的索引号
        curIndex = -1,
        //查找所有被点击的元素对象
        timeLine = document.getElementById("timeline"),
        clickArea = timeLine.getElementsByTagName("s"),
        //查找所有li元素对象
        timePoint = timeLine.getElementsByTagName("li");
    //为每个被点击的对象绑定单击事件
    var times = new Array();
    for (var i = 0, len = clickArea.length; i < len; i++) {
        times[i] = 0;
        (function(i) {
            clickArea[i].onclick = function() {
                //为被点击的时间点li添加active类
                timePoint[i].className = "active";
                if (curIndex != -1 && i != curIndex) {
                    timePoint[curIndex].className = "";
                    times[i] = 1;
                } else if (i == curIndex && times[i] == 1) {
                    timePoint[curIndex].className = "";
                    times[i] = 0;
                } else {
                    times[i] = 1;
                }
                curIndex = i;
            };
        })(i);
    }
};

function item_click_tuijian() {

    var //记录当前已经添加active类的li的索引号
        curIndex = -1,
        //查找所有被点击的元素对象
        timeLine = document.getElementById("timeline_tuijian"),
        clickArea = timeLine.getElementsByTagName("s"),
        //查找所有li元素对象
        timePoint = timeLine.getElementsByTagName("li");

    //为每个被点击的对象绑定单击事件
    for (var i = 0, len = clickArea.length; i < len; i++) {
        (function(i) {
            clickArea[i].onclick = function() {
                //为被点击的时间点li添加active类
                timePoint[i].className = "active";
                if (curIndex != -1) {
                    timePoint[curIndex].className = "";
                }
                curIndex = i;
            };
        })(i);
    }
};

$(document).ready(function() {


    $("#invite_new_btn").click(function(event) {
        /* Act on the event */
        var x = document.getElementsByTagName("input");
        for (var i = 0; i < x.length; i++) {
            x[i].value = '';
        }
        var y = document.getElementsByTagName("select");
        for (var i = 0; i < y.length; i++) {
            y[i].selectedIndex = y[i].value;
        }
        $("#create_new_invite").show('slow/400/fast');
        $("#invite_more_detail").hide();
        $(".invite_block").hide();
        $("#invite_message_list").hide();
        $("#invite_message_all_list").hide();
    });

    $("#search_more_btn").click(function(event) {
        /* Act on the event */

        $(".invite_block").show();
        $("#invite_more_detail").show('slow/400/fast');
        $("#create_new_invite").hide();
        $("#invite_message_list").hide();
        $("#invite_message_all_list").hide();
    });


    // $("#invite_message").click(function(event) {
    //  /* Act on the event */
    //  $(".invite_block").hide();
    //  $("#invite_more_detail").hide();
    //  $("#create_new_invite").hide();
    //  $("#invite_message_list").fadeIn();
    //  $("#invite_message_all_list").hide();
    //  });

    // $("#invite_message_all").click(function(event) {
    //  /* Act on the event */
    //  $(".invite_block").hide();
    //  $("#invite_more_detail").hide();
    //  $("#create_new_invite").hide();
    //  $("#invite_message_all_list").fadeIn();
    //  $("#invite_message_list").hide();
    //  });



        


    $('#search_invite_start_time').datetimepicker({
        startView: 2,
        forceParse: 0,
        showMeridian: 1,
        autoclose: true,
        todayBtn: true,
        todayHighlight: true,
    });

    $("#create_invite_start_time").datetimepicker({

        startView: 2,
        forceParse: 0,
        showMeridian: 1,
        autoclose: true,
        todayBtn: true,
        todayHighlight: true

    });
});
$(function() {
    $("#menu .home").removeClass("home");
    $($("#menu .bar").get(1)).addClass("home");
});