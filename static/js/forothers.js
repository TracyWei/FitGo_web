$(document).ready(function(){


    var user_uid = $("#forothers_uid").val();
    console.log(user_uid)
    function init(){
        $('#to-plans').click(function(event) {
            $("html,body").animate({scrollTop:$("#myplans").offset().top},800);
        });
        $('#to-states').click(function(event) {
            $("html,body").animate({scrollTop:$("#mystates").offset().top},800);
        });
        $(".tabFocus a").click(function(event) {
            $('.a-active').removeClass('a-active');
            $(event.target).addClass('a-active');
        });
        $("#menu .home").removeClass("home");
        $($("#menu .bar").get(3)).addClass("home");
}
    init();
    getPlan(user_uid);
    getState(user_uid);
});


function getPlan(user_uid){
    jQuery.ajax({
      url: '/plans/detail',
      type: 'GET',
      data:{
        'uid':user_uid
      },
      success: function(data, textStatus, xhr) {
        // console.log(data);
        $("#myTab_plan_show").html(data);
      },
      error: function(xhr, textStatus, errorThrown) {
        
      }
    });
    
};

function getState(user_uid){
  jQuery.ajax({
      url: '/user/usertopic',
      type: 'POST',
      data:{
        'uid':user_uid
      },
      success: function(data, textStatus, xhr) {
        $("#my_state_show").html(data);
      },
      error: function(xhr, textStatus, errorThrown) {
        
      }
    });
}






    























