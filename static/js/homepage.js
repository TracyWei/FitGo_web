$(function(){



function xuanran(){
    $(".activity-0").each(function(index, el) {
     var o=$(this).find("div");
     var s = o.html();
     var p = document.createElement("span");
     var n = document.createElement("a");
     p.innerHTML = s.substring(0,150);
     n.innerHTML = s.length > 150 ? "余下全文" : "";
     console.log(n.innerHTML)
     n.onclick = function(){
        if (n.innerHTML == "余下全文"){
          n.innerHTML = "收起";
          p.innerHTML = s;
        }else{
          n.innerHTML = "余下全文";
          p.innerHTML = s.substring(0,150);
        }
      }
      o.html("");
      o.append(p);
      o.append(n);
      });

}

    function getHot(){
    jQuery.ajax({
      url: '/hot',
      type: 'GET',
      dataType: 'json',
      success: function(data, textStatus, xhr) {
        if(data['code']==200){
          $("#state_one h4").html(data['content']['topics'][0]['topic_title']);
          $("#state_one .content").html(data['content']['topics'][0]['topic_content']);
          $("#state_one .time").html('<span>'+data['content']['topics'][0]['topic_time']+'</span>');

          $("#state_two h4").html(data['content']['topics'][1]['topic_title']);
          $("#state_two .content").html(data['content']['topics'][1]['topic_content']);
          $("#state_two .time").html('<span>'+data['content']['topics'][1]['topic_time']+'</span>');

          $("#state_three h4").html(data['content']['topics'][2]['topic_title']);
          $("#state_three .content").html(data['content']['topics'][2]['topic_content']);
          $("#state_three .time").html('<span>'+data['content']['topics'][2]['topic_time']+'</span>');

          $("#activity_one h4").html(data['content']['act'][0]['title']);
          $("#activity_one .content").html(data['content']['act'][0]['detail']);
          $("#activity_one .time").html('<span>'+data['content']['act'][0]['start']+'</span><span>'+data['content']['act'][0]['act_location']+'</span>');

          $("#invite_one h4").html(data['content']['invite'][0]['fit_item']);
          $("#invite_one .content").html(data['content']['invite'][0]['remark']);
          $("#invite_one .time").html('<span>'+data['content']['invite'][0]['start_time']+'</span><span>'+data['content']['invite'][0]['location']+'</span>');

          $("#invite_two h4").html(data['content']['invite'][1]['fit_item']);
          $("#invite_two .content").html(data['content']['invite'][1]['remark']);
          $("#invite_two .time").html('</span>'+data['content']['invite'][1]['start_time']+'</span><span>'+data['content']['invite'][1]['location']+'</span>');

          xuanran();
        }
      },
      error: function(xhr, textStatus, errorThrown) {
        //called when there is an error
      }
    });
    
};


getHot();


    $('.carousel').carousel({
    interval: 2000
    })
    $('#moredown').mouseover(function(event) {
            $('.absoluteul').show();
        });
    var flag=false;
    $('#moredown').mouseout(function(event) {

    	setTimeout(hide,4000);
    });
    $('.absoluteul').mouseover(function(event) {
    	flag=true;
    	$('#morecolor').removeClass('bar');
    	$('#morecolor').addClass('more-color');
    });
    $('.absoluteul').mouseout(function(event) {
    	$('.absoluteul').hide();
    	flag=false;
    	$('#morecolor').removeClass('more-color');
    	$('#morecolor').addClass('bar');
    });
    $('#move-to-contact').click(function(event) {
    	$('html,body').animate({scrollTop:$('#startfooter').offset().top}, 1000);
    });
    $('#show-introduce').click(function(event) {
        $('.ag-content-customer-wrap').show();
        $('html,body').animate({scrollTop:$('.ag-content-customer-wrap').offset().top}, 500);
    });
    function hide(){
    	if(!flag){
    		$('.absoluteul').hide();
    	}
    }

    });

function toTop(){
    $("body").animate({scrollTop:0}, 500);
}
