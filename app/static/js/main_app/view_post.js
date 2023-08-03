//Update ingredients list in the DOM
function update_ingredients_list(){
    let ingredients = localStorage.getItem('ingredients').split(',');
    $('#ul_ingredients').html('');
    if (ingredients[0] != "") {
        ingredients.forEach(e => $('#ul_ingredients').append('<li>' +
        '<span class=\"badge rounded-pill text-bg-secondary\">' +
        e + '</span>' + '</li>'));
    }
    
}

//Update tags list in the DOM
function update_tags_list(){
    let tags = localStorage.getItem('tags').split(',');
    $('#ul_tags').html('');
    if (tags[0] != "") {
        tags.forEach(e => $('#ul_tags').append('<li>' +
        '<span class=\"badge rounded-pill text-bg-secondary\">' +
        e + '</span>' + '</li>'));
    }
    
}

$(function(){

    let post_id = $('#input_post_id').val();

    $.ajax({
        url:'/get_post_information/' + post_id,
        datatype:'json',
        type:'GET',
        success:function(data){
            $('#input_recipe_name').val(data['recipe_name']);
            localStorage.setItem('ingredients', data['ingredients']);
            localStorage.setItem('tags', data['tags']);
            $('#select_visibility').val(data['visibility']).change();
            $('#textarea_instructions').val(data['instructions']);

            update_ingredients_list();

            update_tags_list();

        },
        error:function(e){
            console.log(e);
        },
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