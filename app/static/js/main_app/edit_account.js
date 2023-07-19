function update_tags_list(){
    let tags = localStorage.getItem('tags').split(',');
    $('#ul_tags').html('');
    tags.forEach(e => $('#ul_tags').append('<li>' + e + '</li>'));
}


$(function(){

    let input_target_username = $('#input_target_username').val();

    $.ajax({
        url:'/get_interested_tags_user/'+input_target_username,
        datatype:'json',
        type:'GET',
        success:function(data){            
            localStorage.setItem('tags', data.toString());
            update_tags_list();
        },
        error:function(e){
            console.log(e);
        },
    }); 
})

$('#input_name').on('input', ()=>{
    $('#btn_save_changes').prop('disabled', false);
});

$('#input_search_tag').on('input', ()=>{
    $('#span_found_tag').html('');
    $('#btn_add_tag').prop('disabled', true);
});

$('#btn_add_tag').on('click', ()=> {
    
    let input_search_tag = $('#input_search_tag').val();

    let tags_string = localStorage.getItem('tags');
    
    localStorage.setItem('tags', tags_string + ',' + input_search_tag);
    
    update_tags_list();
});

$('#btn_search_tag').on('click',()=>{
    
    let input_search_tag = $('#input_search_tag').val();

    if (input_search_tag != ''){
        $.ajax({
            url:'/get_tag_information/'+input_search_tag,
            datatype:'json',
            type:'GET',
            success:function(data, status, xhr){
                status_code = xhr.status;
                if (status_code == 200){

                    let tags = localStorage.getItem('tags').split(',');

                    if (tags.includes(input_search_tag)){
                        $('#span_found_tag').html('You already have that tag');
                    } else {
                        $('#span_found_tag').html('Tag was found');
                        $('#btn_add_tag').prop('disabled', false);    
                    }
                    
                    
                } else {
                    console.log('An error ocurred');
                }
            },
            error:function(e){
                $('#span_found_tag').html('Tag was not found');
                $('#btn_add_tag').prop('disabled', true);
                console.log(e);
            },
        })
    }

});

$('#btn_save_changes').on('click', ()=> {
    
    let input_target_username = $('#input_target_username').val();
    let input_name = $('#input_name').val();

    let data = {
        'username':input_target_username,
        'name':input_name,
    }

    if (input_name != ''){
        $.ajax({
            url:'/edit_account_fields/',
            datatype:'text',
            type:'POST',
            data: data,
            successful:function(data, status, xhr){
                status_code = xhr.status;
                if (status_code === 200){
                    $('#btn_save_changes').prop('disabled', true);
                    console.log('User data has been successfully updated');
                } else {
                    console.log('An error has ocurred');
                }
            },
            error:function(e){
                console.log(e);
            },
        });
    }
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