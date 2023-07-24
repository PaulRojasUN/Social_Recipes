function load_posts(){
  $.ajax({
    url:'/get_homepage_posts',
    datatype:'json',
    type:'GET',
    success:function(data){
        $('#posts_container').html("");  
        
        if (data.length > 0){
          data.forEach(element => {
            let string_post = `<div class="post">
                    <p><span class="fw-bold">${element['author_user_id__first_name']}</span>
                    posted <span class="fw-bold">${element['recipe_name']}</span>
                     on <span class="fw-bold">${element['post_date']}</span></p>
                     <div><pre>${element['body_text']}</pre></div>
                    <p>Likes <span class="fw-bold">#</span>
                    ${element['liked']===1 ? `<button id=\"btn_like_${element['id']}\" class="btn_like">Remove Like</button></p>`
                  : `<button id=\"btn_like_${element['id']}\" class="btn_like">Like</button></p>`}
                    
            </div><hr>`;
            $('#posts_container').append(string_post);            
          });


        $('.btn_like').on('click', (e)=>{
          let post_id = e.target.id.split('_')[2];

          let data = {
              'post_id':post_id,
          }

          $.ajax({
              url:'/add_remove_like_post/',
              datatype:'json',
              type:'POST',
              data:data,
              success:function(data, status, xhr){
                  let status_code = xhr.status;
                  if (status_code === 250){
                    console.log('Like successfully added');
                    $(`#btn_like_${post_id}`).html('Remove like');
                  } else {
                    console.log('Like successfully removed');
                    $(`#btn_like_${post_id}`).html('Like');
                  }
                  
              },
              error:function(e){
                  console.log(e);
              },
              });
          })

          $('#btn_reset_posts').prop('hidden', true);
          $('#btn_display_more_posts').prop('hidden', false);
        } else {
          $('#btn_reset_posts').prop('hidden', false);
          $('#btn_display_more_posts').prop('hidden', true);
        }
    },
    error:function(e){
        console.log(e);
    }
}); 
}

$(function(){
    load_posts();
});

$('#btn_display_more_posts').on('click', ()=>{
  $.ajax({
    url:'/increment_post_seed/',
    datatype:'text',
    type:'POST',
    success:function(){
      console.log("Showing more posts");
      load_posts();
    },
    error:function(e){
      console.log(e);
    },
  });
  
});


$('#btn_reset_posts').on('click', ()=>{
  $.ajax({
    url:'/reset_posts/',
    datatype:'text',
    type:'POST',
    success:function(){
      console.log("Resetting posts");
      load_posts();
    },
    error:function(e){
      console.log(e);
    },
  });
  
});



// Cookies

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