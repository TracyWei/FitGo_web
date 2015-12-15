$(window).load(function() {
    var options =
    {
        thumbBox: '.thumbBox',
        spinner: '.spinner',
        imgSrc: ''
    }
    var cropper = $('.imageBox').cropbox(options);
    var img="";
    $('#upload-file').on('change', function(){
        var reader = new FileReader();
        reader.onload = function(e) {
            options.imgSrc = e.target.result;
            cropper = $('.imageBox').cropbox(options);
            getImg();
        }
        reader.readAsDataURL(this.files[0]);
        this.files = [];
        //getImg();
    })
    $('#btnCrop').on('click', function(){
        alert("图片上传喽");
    })
    function getImg(){
        img = cropper.getDataURL();
        $('.cropped').html('');
        $('.cropped').append('<img src="'+img+'" align="absmiddle" style="width:180px;margin-top:4px;border-radius:180px;box-shadow:0px 0px 12px #7E7E7E;"><p>180px*180px</p>');
        $('.cropped').append('<img src="'+img+'" align="absmiddle" style="width:128px;margin-top:4px;border-radius:128px;box-shadow:0px 0px 12px #7E7E7E;"><p>128px*128px</p>');
        $('.cropped').append('<img src="'+img+'" align="absmiddle" style="width:64px;margin-top:4px;border-radius:64px;box-shadow:0px 0px 12px #7E7E7E;" ><p>64px*64px</p>');
        }
        
    $(".imageBox").on("mouseup",function(){
        getImg();
        });
        
        
    $('#btnZoomIn').on('click', function(){
        cropper.zoomIn();
    })
    $('#btnZoomOut').on('click', function(){
        cropper.zoomOut();
    })
});


$(document).ready(function() {
    $('#subPor').click(function(event) {
        console.log('get');
        fileupload();
        // window.location.href="/plans/Info";
        });


});

function fileupload(){
    if($("#upload-file").val()){
        $("#upload_form").ajaxSubmit(function(message){
           data = JSON.parse(message);
           console.log(data)
           if(data['code']==200){
           window.location.href="/plans/Info";
        }
        });
    }
    else{
        
    }
};
