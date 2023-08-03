
function load_posts(){

    let par1 = $('#input_par1').val();

    $.ajax({
      url:`/filter_search/?par1=${par1}`,
      datatype:'json',
      type:'GET',
      success:function(data){
          $('#posts_container').html("");  
          
          if (data.length > 0){
            data.forEach(element => {
              let string_post = `<div class="card div_post">
            <div class="card-body">
              <h5 class="card-title"><a href="/view_post/${element['id']}">${element['recipe_name']}</a></h5>
              <h6 class="card-subtitle mb-2 text-body-secondary">Posted by <a href="/view_account/${element['author_user_id__username']}"><p><span class="fw-bold">${element['author_user_id__first_name']}</span></a></h6>
              <p class="card-text">${element['body_text']}</p>
              <p>Likes <span id="span_likes_${element['id']}" class="fw-bold">${element['likes']!=null ? element['likes'] : 0}</span>
                      ${element['liked']===1 ? `<button id=\"btn_like_${element['id']}\" class="btn btn-secondary btn_like">Remove Like</button></p>`
                    : `<button id=\"btn_like_${element['id']}\" class="btn btn-secondary btn_like">Like</button></p>`}

            </div>
          </div>
          `
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
                    let current_likes = $(`#span_likes_${post_id}`).html();
                    if (status_code === 250){
                      console.log('Like successfully added');
                      $(`#span_likes_${post_id}`).html(parseInt(current_likes)+1);
                      $(`#btn_like_${post_id}`).html('Remove like');
                    } else {
                      console.log('Like successfully removed');
                      $(`#span_likes_${post_id}`).html(parseInt(current_likes)-1);
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


// $(function(){
//     let par1 = $('#par1').val();

//     $.ajax({
//         url: `/filter_search?par1=${par1}`,
//         datatype:'json',
//         type:'GET',
//         success:function(data){

//         },
//         error:function(e){
//             console.log(e);
//         },
//     });
// })

  
  $(function(){
      load_posts();
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