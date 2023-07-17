$(function () {

    const target_username = $('#target_username').val();

    $('#btn_follow').on('click', ()=>{

      const follower_user = $('#input_follower').val();
      const target_user = $('#input_target').val();

      $.ajax({
        url: '/add_following/',
        dataType: 'text',
        type: 'POST',
        data:{
          'follower_user':follower_user,
          'target_user':target_user
        },
        success: function (res, status, xhr) {
          const status_code = xhr.status;
            
          if (status_code == 250){
            $('#btn_follow').hide();
          } else if (status_code == 251) {
              $('#btn_follow').html('Follow User');
          } else if (status_code == 252) {
              $('#btn_follow').html('Unfollow User');                
          } else {
              console.error("An error has ocurred");
          }
        },
        error: function (e) {
          console.log(e);
        }
      })
    });

//btn_follow
    

      $.ajax({
        url: '/prepare_view_account/' + target_username,
        dataType: 'text',
        type: 'GET',
        success: function (res, status, xhr) {
            const status_code = xhr.status;
            
            if (status_code == 250){
              $('#btn_follow').hide();
            } else if (status_code == 251) {
                $('#btn_follow').html('Follow User');
            } else if (status_code == 252) {
                $('#btn_follow').html('Unfollow User');                
            } else {
                console.error("An error has ocurred");
            }
        },
        error: function (e) {
          console.log(e);
        }
      })


    }
    );




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