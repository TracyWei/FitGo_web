$(document).ready(function() {
    // init();
    // search();
    NewInvitation();
    getNewInvite();
    getAllinvite();
    recom();
    $("#create_invite_information_message").hide();
    // $(".wrong_message").hide();
    $("#search_btn").click(function(event) {
        search();
        $(".list_name").show();
          $("#invite_message_list").hide();
          
          $("#invite_message_all_list").hide();
    });
});

function NewInvitation(){
    $("#NewButton").click(function(event) {
        var fit_location = $("#create_fit_location").val();
        if(fit_location=='Location'){fit_location='';}

        var fit_item = $("#create_fit_item").val();
        if(fit_item=='Fit Item'){fit_item='';}

        var gender = $("#create_gender").val();
        if(gender=='Gender'){gender='';}

        var duration = $("#create_duration").val();
        if(duration=='Duration'){duration='';}
        var start_time=$("#create_invite_start_time").val();
        var tag = $("#create_invite_tag").val();
        var moreInfo = $("#create_invite_more").val();
        jQuery.ajax({
          url: '/invite',
          type: 'POST',
          dataType: 'json',
          data: {
                'start_time':start_time,
                'duration':duration,
                'fit_location':fit_location,
                'fit_item':fit_item,
                'user_tag':tag,
                'gender':gender,
                'remark':moreInfo
          },
          success: function(data, textStatus, xhr) {
            console.log(data['code'])
            if(data['code']==200){
                console.log(data['code']);
                $("#create_invite_information_message").attr('class','alert alert-success showing');
                $("#create_invite_information_message").html('Success');
                $("#create_invite_information_message").show();
                setTimeout(function() {
                    $("#create_invite_information_message").hide();
                    $("#create_new_invite").hide();
                    },1000);
            }else{
                $("#create_invite_information_message").html(data['content']);
                $("#create_invite_information_message").show();
            }
          },
          error: function(xhr, textStatus, errorThrown) {
            $("#create_invite_information_message").html('Network Error!');
            $("#create_invite_information_message").show();
          }
        });
        
    });
}


function recom(){
  jQuery.ajax({
    url: '/recom/recominvite',
    type: 'GET',
    success: function(data, textStatus, xhr) {
      //called when successful
      $("#timeline_tuijian").html(data);
      $("#timeline_tuijian").show();
      $(".list_name_tuijian").show();
        item_click_tuijian();
        $("#timeline").hide();
        newInvite();
    },
    error: function(xhr, textStatus, errorThrown) {
      //called when there is an error
    }
  });
  
}

function search(){
    var tag=$("#search_invite_tag").val();
    var fit_location = $("#fit_location").val()
    if(fit_location=='Location'){fit_location='';}
    var fit_item=$("#fit_item").val();
    if(fit_item=='Fit Item'){fit_item='';}
    var gender = $("#gender").val();
    if(gender=="Gender"){gender='';}
    var start_time = $("#search_invite_start_time").val();
    jQuery.ajax({
      url: '/invite/search',
      type: 'POST',
      data: {
           'start_time':start_time,
           'fit_location':fit_location,
           'fit_item':fit_item,
           'user_tag':tag,
           'gender':gender
      },
      success: function(data, textStatus, xhr) {
        $("#timeline").html(data);
        $("#timeline").show();
        $("#timeline_tuijian").hide();
        $(".list_name_tuijian").hide();
        item_click();
        newInvite();
      },
      error: function(xhr, textStatus, errorThrown) {
        $("#timeline").html('<li class="wrong_message" ><div class="content" id="wrong_message"><h3>Network Error!</h3></div></li>');
      }
    });
};
function newInvite(){
  $(".confirm_invite").each(function(index, el) {
      $(this).click(function(event) {
          // console.log(index);
          var _id=$(this).attr('value');
          var uid=$("#"+_id).find('.user_index').attr('value');
          var thisButton = $(this);
          jQuery.ajax({
            url: '/invite/request',
            type: 'POST',
            dataType: 'json',
            data: {
              'uid': uid,
              '_id':_id
          },
            success: function(data, textStatus, xhr) {
              if(data['code']==200){
               thisButton.attr({"disabled":"disabled"});
              }
            },
            error: function(xhr, textStatus, errorThrown) {
              //called when there is an error
            }
          });
          
      });
  });

};

function getNewInvite(){
  $("#invite_message_btn").click(function(event) {
    /* Act on the event */

    jQuery.ajax({
      url: '/invite/respond',
      type: 'GET',
      success: function(data, textStatus, xhr) {
        $("#invite_message_list").html(data);
        inviteOperation()
        $(".invite_block").hide();
        $("#invite_more_detail").hide();
        $("#create_new_invite").hide();
        $("#invite_message_list").fadeIn();
        $("#invite_message_all_list").hide();
      },
      error: function(xhr, textStatus, errorThrown) {
        console.log(textStatus)
      }
    });
    
    
    });
};


function inviteOperation(){
  $(".btn-info").each(function(index, el) {
    
    $(this).click(function(event) {
      request_id = $(this).attr('value');
      request_uid = $("#"+request_id).find(".request_info").attr('value');
      // console.log(request_id+request_uid);

      /* Act on the event */
      RespondRequest(request_id,request_uid,1);
    });
  });

  $(".btn-danger").each(function(index, el) {
    $(this).click(function(event) {
      /* Act on the event */
      request_id = $(this).attr('value');
      request_uid = $("#"+request_id).find(".request_info").attr('value');
      // console.log(request_id+request_uid);
      RespondRequest(request_id,request_uid,2);
    });
  });
};

function RespondRequest(_id,request_id,code){
  // console.log(_id);
  // console.log(request_id);
  jQuery.ajax({
        url: '/invite/respond',
        type: 'PUT',
        dataType: 'json',
        data: {
          '_id': _id,
          'uid_request':request_id,
          'code':code
      },
        success: function(data, textStatus, xhr) {
          if(data['code']==200){
            $("#"+_id+" button").attr({'disabled':'disabled'});
          }
        },
        error: function(xhr, textStatus, errorThrown) {
          //called when there is an error
          console.log(textStatus)
        }
      });
};

function getAllinvite(){
    $("#invite_message_all_btn").click(function(event) {
      /* Act on the event */
      jQuery.ajax({
        url: '/invite/respondlist',
        type: 'GET',
        success: function(data, textStatus, xhr) {
          $("#invite_message_all_list").html(data);
          $(".invite_block").hide();
          $("#invite_more_detail").hide();
          $("#create_new_invite").hide();
          $("#invite_message_all_list").fadeIn();
          $("#invite_message_list").hide();
        },
        error: function(xhr, textStatus, errorThrown) {
        }
      });
      
    });
}

