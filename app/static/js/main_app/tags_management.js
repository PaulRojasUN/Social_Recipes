$(function () {

    $('#btn_create_tag').on('click', () => {

        let tag_name = $('#input_tag_name').val();

        console.log(tag_name);

        if (tag_name != ''){
            $.ajax({
                url:'/create_tag/',
                datatype:'text',
                type:'POST',
                data:{
                    'tag_name':tag_name,
                },
                success:function(res, status, xhr){
                    status_code = xhr.status;
                    if (status_code == 200){
                        console.log('Tag created successfully');
                    } else if (status_code == 461){
                        console.log('Another tag exists with that name');
                    } 
                    else {
                        console.log('It has occurred an error');
                    }
                },
                error:function(e){
                    console.log(e);
                }
            })
        }


    })

});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
  const csrftoken = getCookie('csrftoken');
  
  
  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });