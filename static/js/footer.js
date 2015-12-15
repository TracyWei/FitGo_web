$(document).ready(function() {
    var uid="";
    if($("#user_state").val()=='0'){
        $("#verify_dropdown").hide();
        $("#signup_dropdown").hide();
        $("#login_div").fadeIn();
        $("#find_password_dropdown").hide();
        $("#find_password_new_pwd").hide();
        $("#login_message").hide();
        $("#sign_up_message").hide();
        $("#change_password_message").hide();
        $("#find_message").hide();
        $("#verify_message").hide();
    };
    if ($("meta[name=toTop]").attr("content") == "true") {
        $("<div id='toTop'><img id='toTopbtn' src='/static/images/top1.png'></div>").appendTo('body');
        $("#toTop").css({
            width: '50px',
            height: '50px',
            bottom: '10px',
            right: '10px',
            position: 'fixed',
            cursor: 'pointer',
            zIndex: '999999',
        });
        if ($(this).scrollTop() == 0) {
            $("#toTop").hide();
        }
        $(window).scroll(function(event) {
            if ($(this).scrollTop() == 0) {
                $("#toTop").hide();
            }
            if ($(this).scrollTop() != 0) {
                $("#toTop").show();
            }
        });
        $("#toTop").click(function(event) {
            $("html,body").animate({
                    scrollTop: "0px"
                },
                666)
        });
    }
    
    $("#code_img").attr("src",'/auth/code/'+Math.random());
    $(".dropdown_close").click(function(event) {
        /* Act on the event */
        $("#verify_dropdown").hide();
        $("#signup_dropdown").hide();
        $("#login_div").hide();
        $("#find_password_dropdown").hide();
        $("#find_password_new_pwd").hide();
    });
    $(".forgot-password").click(function(event) {
        /* Act on the event */
        $("#verify_dropdown").hide();
        $("#signup_dropdown").hide();
        $("#login_div").hide();
        $("#find_password_dropdown").fadeIn();
    });
    $("#check_btn").click(function(event) {
        /* Act on the event */
        $("#verify_dropdown").hide();
        $("#signup_dropdown").hide();
        $("#login_div").hide();
        $("#find_password_new_pwd").fadeIn();
    });
    // $("#code_img").click(function(event) {
    //     /* change code */
    //     time=new time()
    //     codes = time.getTime()+Math.random()
    //     document.getElementById('code_img').src="/auth/code/"+codes;
    // )};
    $("#login").click(function(event) {
        /* Act on the event */
        $("#verify_dropdown").hide();
        $("#signup_dropdown").hide();
        $("#login_div").fadeIn();
        $("#find_password_dropdown").hide();
        $("#find_password_new_pwd").hide();
        $("#login_message").hide();
        $("#sign_up_message").hide();
        $("#change_password_message").hide();
        $("#find_message").hide();
        $("#verify_message").hide();
    });
    $("#sign_up_btn").click(function(event) {
        /* Act on the event */
        $("#verify_dropdown").hide();
        $("#signup_dropdown").fadeIn();
        $("#login_div").hide();
        $("#find_password_dropdown").hide();
    });
    // 验证

    $("#verify").click(function(event) {
        /* Act on the event */
        jQuery.ajax({
            url: '/auth/register/verify',
            type: 'POST',
            dataType: 'json',
            data: {
                'info_email': $("#info_email_signup").val(),
                'student_card': $("#student_card_signup").val(),
                'student_id': $("#student_id_signup").val()
            },
            success: function(data, textStatus, xhr) {
                if (data['code'] == 200) {
                    $("#login_div").hide();
                    $("#verify_dropdown").fadeIn();
                    $("#signup_dropdown").hide();
                    $("#find_password_dropdown").hide();
                    uid = data['content']['uid'];
                } else {
                    $("#verify_message").html(data['content']);
                    $("#verify_message").fadeIn();
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                //called when there is an error
                $("#verify_message").html("Network error!");
            }
        });


    });

    //注册
    $("#signup_btn").click(function(event) {
        if ($("#password_signup").val().length < 6) {
            $("#sign_up_message").html("password is too short");
            $("#sign_up_message").fadeIn();
        } else if ($("#password_signup").val() != $("#password_confirm").val()) {
            $("#sign_up_message").html("Confirm password is not the same as password");
            $("#sign_up_message").fadeIn();
        } else {
            jQuery.ajax({
                url: '/auth/register',
                type: 'POST',
                dataType: 'json',
                data: {
                    'uid': uid,
                    'name': $("#name_signup").val(),
                    'password': $("#password_signup").val()
                },
                success: function(data, textStatus, xhr) {
                    //called when successful
                    if (data['code'] == 200) {
                        location.href = "/";
                    } else {
                        $("#sign_up_message").html(data['content']);
                        $("#sign_up_message").fadeIn();
                    }
                },
                error: function(xhr, textStatus, errorThrown) {
                    $("#sign_up_message").html("Network error!");
                }
            });
        }

    });

    // 登录
    $("#login_btn").click(function() {
        if ($("#password_login").val().length < 6) {
            $("#login_message").html("password is too short");
            $("#login_message").fadeIn();
        } else {
            var is_remember = 0;
            if ($("#login_check").is(':checked')) {
                is_remember = 1;
            }
            jQuery.ajax({
                url: '/auth/login',
                type: 'POST',
                dataType: "json",
                data: {
                    'info_email': $("#info_email_login").val(),
                    'user_password': $("#password_login").val(),
                    'code': $("#code_login").val(),
                    'code_random':$("#code_img").attr("src"),
                    'is_remember': is_remember
                },
                success: function(data, textStatus, xhr) {
                    if (data['code'] == 200) {
                        location.href = "/";
                    } else {
                        $("#login_message").html(data['content']);
                        $("#login_message").fadeIn();
                    }
                },
                error: function(xhr, textStatus, errorThrown) {
                    $("#login_message").html("Network error!");
                }
            });
        }
    });
    // 登出
    $("#who-name").click(function(event) {
        /* Act on the event */
        jQuery.ajax({
            url: '/auth/logout',
            method: 'DELETE',
            complete: function(xhr, textStatus) {
                //called when complete
            },
            success: function(data, textStatus, xhr) {
                var date = new Date();
                date.setTime(date.getTime() - 10000);
                document.cookie = "username=null; expires=" + date.toGMTString();
                location.href = "/";
                //called when successful
            },
            error: function(xhr, textStatus, errorThrown) {
                //called when there is an error
            }
        });

    });

    //找回密码
    $("#find_password_btn").click(function(event) {
        var newPassword = $("#password_find_password").val();
        var passwordConfirm = $("#password_confirm_find_password").val();
        var email = $("#info_email_find_password").val();
        var card = $("#student_card_find_password").val();
       if(email.length<1||card.length<1||newPassword.length<1||passwordConfirm.length<1){
            $("#change_password_message").html('Something is Null!');
            $("#change_password_message").show();
        }
        else if (newPassword != passwordConfirm) {
            $("#change_password_message").html('You must input the same password');
            $("#change_password_message").show();
        } else {
            /* Act on the event */
            console.log('here')
           jQuery.ajax({
                url: '/auth/password',
                type: 'POST',
                dataType: 'json',
                data: {
                    'info_email': email,
                    'student_card': card,
                    'new_password':newPassword
                },
                success: function(data, textStatus, xhr) {
                    console.log(data)
                    if (data['code'] == 200) {
                        $("#change_password_message").html('Success');
                        $("#change_password_message").show();
                         setTimeout(function(){

                        $("#signup_dropdown").hide();
                        $("#login_div").fadeIn();
                        $("#find_password_dropdown").hide();
                        $("#find_password_new_pwd").hide();
                        $("#login_message").hide();
                        $("#sign_up_message").hide();
                        $("#change_password_message").hide();
                        $("#find_message").hide();
                        $("#verify_message").hide();
                    },1000);
                    } else {
                        $("#change_password_message").html(data['content']);
                        $("#change_password_message").show();
                    }
                    //called when successful
                },
                error: function(xhr, textStatus, errorThrown) {
                    console.log(textStatus)
                        $("#change_password_message").html('Network error!');
                        $("#change_password_message").show();
                }
            });
        }

});

});
 var ctrlBar = false;

    var float_timer = null;
    var float_max_X;
    var float_max_Y;
    var float_ctrl_X = true;
    var float_ctrl_Y = true;
    $(function () {
        float_max_X = $(window).width();
        float_max_Y = $(window).height();
    });
    function showVideoImage() {
        if ($('.vjs-poster').css('display') == 'none') {
        $('.vjs-poster').addClass('index').show();
        } else {
            setTimeout('showVideoImage()', 50);
        }
    }

    function startMove() {
        var obj = $('#floatAdv');
        var limit_X = float_max_X - obj.width();
        var limit_Y = float_max_Y - obj.height();
        float_timer = setInterval(function () {
            var _x = parseInt(obj.css('left'));
            var _y = parseInt(obj.css('top'));
            if (_x >= limit_X) {
                float_ctrl_X = false;
            }
            if (_x <= 0) {
                float_ctrl_X = true;
            }
            if (_y >= limit_Y) {
                float_ctrl_Y = false;
            }
            if (_y <= 0) {
                float_ctrl_Y = true;
            }
            if (float_ctrl_X) {
                _x += 1;
            } else {
                _x -= 1;
            }
            if (float_ctrl_Y) {
                _y += 1;
            } else {
                _y -= 1;
            }
            obj.css({
                'left': _x + 'px',
                'top': _y + 'px'
            });
        }, 10);
    }

    function endMove() {
        clearInterval(float_timer);
    }

    $(document).ready(function () {
        $('.ag-header ul li:eq(0)').addClass('current-page');
        showVideoImage();

        $('#floatAdv').mouseenter(function () {
            endMove();
        });
        $('#floatAdv').mouseleave(function () {
            startMove();
        });
        $('#floatAdv span').click(function (e) {
            endMove();
            $('#floatAdv').attr('href', 'javascript:;').removeAttr('target').hide();
        });

        $(".ag-content-customer-ele").bind("mouseenter mouseleave", function (e) {
            var w = $(this).width();
            var h = $(this).height();
            var x = (e.pageX - this.offsetLeft - (w / 2)) * (w > h ? (h / w) : 1);
            var y = (e.pageY - this.offsetTop - (h / 2)) * (h > w ? (w / h) : 1);
            var direction = Math.round((((Math.atan2(y, x) * (180 / Math.PI)) + 180) / 90) + 3) % 4;
            if (e.type == 'mouseenter') {
                // 0:up - 1:right - 2:down - 3:left
                if(direction == 0) {
                    $(this).find('div').css({
                        'top' : '-470px',
                        'left' : '0px'
                    });
                    $(this).find('div').animate({ 'top': 0 }, { queue: false, duration: 300 });
                } else if(direction == 2) {
                    $(this).find('div').css({
                        'top' : '470px',
                        'left' : '0px'
                    });
                    $(this).find('div').animate({ 'top': 0 }, { queue: false, duration: 300 });
                } else if(direction == 1) {
                    $(this).find('div').css({
                        'top' : '0px',
                        'left' : '167px'
                    });
                    $(this).find('div').animate({ 'left': 0 }, { queue: false, duration: 300 });
                } else if(direction == 3) {
                    $(this).find('div').css({
                        'top' : '0px',
                        'left' : '-167px'
                    });
                    $(this).find('div').animate({ 'left': 0 }, { queue: false, duration: 300 });
                }
                $(this).find('span').css('color', '#fff');
                $(this).find('img').animate({ 'left': $(this).find('img').attr('data-hover') }, { queue: false, duration: 200 });
            }else{
                if(direction == 0) {
                    $(this).find('div').animate({ 'top': -470 }, { queue: false, duration: 300 });
                } else if(direction == 2) {
                    $(this).find('div').animate({ 'top': 470 }, { queue: false, duration: 300 });
                } else if(direction == 1) {
                    $(this).find('div').animate({ 'left': 167 }, { queue: false, duration: 300 });
                } else if(direction == 3) {
                    $(this).find('div').animate({ 'left': -167 }, { queue: false, duration: 300 });
                }
                $(this).find('span').css('color', '#262626');
                $(this).find('img').animate({ 'left': $(this).find('img').attr('data-normal') }, { queue: false, duration: 200 });
            }
        });

        $(".ag-content-customer-ele").bind('click', function (e) {

            var navIndex = $(e.target).parent().index();
            $('.ag-content-customer-ele-detail ul li').removeClass('current');
            $('.ag-content-customer-ele-detail ul li').eq(navIndex).addClass('current');

            $('.ag-content-customer-wrap').css('background-color', '#fff');
            $('.ag-content-customer-ele').animate({ 'width': 0 }, 500);

            $('.ag-content-customer-ele-detail').animate({ 'width': 1002 }, {
                duration: 500,
                complete: function () {
                    $('.ag-content-customer-ele-detail ul li').eq(navIndex).click();
                }
            });
        });

        $('.ag-content-customer-ele-detail-return').bind('click', function (e) {

            $('.ag-content-customer-wrap').css('background-color', '#fff');
            $('.ag-content-customer-ele-detail').css('overflow', 'hidden');
            $('.ag-content-customer-ele').animate({ 'width': 167 }, 500);
            $('.ag-content-customer-ele-detail').animate({ 'width': 0 }, 500);
            $('.ag-content-customer-ele-detail-display').hide();
        });

        $('.ag-content-customer-ele-detail ul li').bind('click', function () {

            $('.ag-content-customer-ele-detail ul li').removeClass('current');
            $(this).addClass('current');
            $('.ag-content-customer-ele-detail').css('overflow', 'visible');

            var disIndex = $(this).index();
            $('.ag-content-customer-ele-detail-display').hide();
            $('.ag-content-customer-ele-detail-display').eq(disIndex).show();

            // IE
            if ("ActiveXObject" in window) {
                $('.ag-content-customer-ele-detail-display-left').css({
                    'left': '0px',
                    'opacity':'1'
                });
                $('.ag-content-customer-ele-detail-display-right').css({
                    'right': '-120px',
                    'opacity': '1'
                });
                $('.ag-content-customer-ele-detail-display-left').eq(disIndex).animate({ 'left': 120 }, { duration: 1000, easing: 'easeOutQuint' });
                $('.ag-content-customer-ele-detail-display-right').eq(disIndex).animate({ 'right': 0 }, { duration: 1000, easing: 'easeOutQuint' });
            }
        });

        $('body').on('click', '.vjs-big-play-button', function () {
            $(this).hide();
            ctrlBar = true;
            $('.vjs-control-bar').removeClass('vjs-fade-out').addClass('vjs-fade-in');
        });

        $('.ag-content-app-wytgg-right').click(function () {
            if (!$('#ag-app-video').hasClass('vjs-playing')) {
                $('.vjs-big-play-button').css('display', 'none');
                ctrlBar = true;
                $('.vjs-control-bar').removeClass('vjs-fade-out').addClass('vjs-fade-in');
            }
        });

        // IE7
        if (window.navigator.userAgent.indexOf('MSIE 7.0') >= 0) {
            $('#ag-app-video').css({
                'width': '570px',
                'height': '380px',
                'position': 'relative'
            });
            $('#ag-app-video').find('div.vjs-poster').css({
                'width': '570px',
                'height': '380px',
                'position': 'absolute',
                'top': '0px'
            });
            $('.vjs-big-play-button').css({
                'width': '100px',
                'height': '100px',
                'position': 'absolute',
                'top': '140px',
                'left': '235px'
            });
            $('.ag-content-app-wytgg-right').css('overflow', 'hidden');
        } else {
            $('.ag-content-app-wytgg-right').hover(
                function () {
                    if (ctrlBar) {
                        $('.vjs-control-bar').removeClass('vjs-fade-out').addClass('vjs-fade-in');
                    }
                },
                function () {
                    $('.vjs-control-bar').removeClass('vjs-fade-in').addClass('vjs-fade-out');
                }
            );
        }
    });
