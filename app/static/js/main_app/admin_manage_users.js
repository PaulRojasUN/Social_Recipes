$(function () {

  const username_parameter = $('#input_username').val();


    $.ajax({
      url:'/prepare_admin_manage_users/' + username_parameter,
      datatype: 'json',
      type:'GET',
      success:function (res) {
        if (res['is_moderator']==0){
          $('#btn_role').html('Remove from Moderators');
        } else {
          $('#btn_role').html('Add to Moderators');
        }
      },
      error:function(e) {
        console.log(e);
      }
    })

    $("#btn_search").on('click', ()=>{


      $.ajax({
        url: '/get_user_username/' + username_parameter,
        dataType: 'json',
        type: 'GET',
        success: function (res) {
          $("#input_name").val(res['name']);
          $("#input_email").val(res['email']);
          $("#input_role").val(res['role']);
        },
        error: function (e) {
          console.log(e);
        }
      })

      // if (username_parameter){
      //   $.ajax({
      //     url: '/predict_username/' + username_parameter,
      //     dataType: 'json',
      //     type: 'GET',
      //     success: function (res) {
      //       $("#input_username").autocomplete({
      //         source: res
      //       });
      //     },
      //     error: function (e) {
      //       console.log(e);
      //     }
      //   })
      // }
      
      });


      $("#btn_role").on('click', ()=>{


        $.ajax({
          url: '/add_remove_moderator/',
          dataType: 'text',
          type: 'POST',
          data:{
            'username_parameter':username_parameter,
          },
          success: function (res, status, xhr) {
            const status_code = xhr.status;

            if (status_code == 250){
              $('#btn_role').html('Remove from Moderators');
            } else if (status_code == 251) {
              $('#btn_role').html('Add to Moderators');
            } else {
              console.error("An error has ocurred");
            }
          },
          error: function (e) {
            console.log(e);
          }
        })
        
        });

        
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