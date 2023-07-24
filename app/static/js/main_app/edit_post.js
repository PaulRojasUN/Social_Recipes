//Update ingredients list in the DOM
function update_ingredients_list(){
    let ingredients = localStorage.getItem('ingredients').split(',');
    $('#ul_ingredients').html('');
    if (ingredients[0] != "") {
        ingredients.forEach(e => $('#ul_ingredients').append('<li>' + e + '<button id=\"'+ 'btn_li_ing_' + e +'\">x</button></li>'));
    }
    
}

//Update tags list in the DOM
function update_tags_list(){
    let tags = localStorage.getItem('tags').split(',');
    $('#ul_tags').html('');
    if (tags[0] != "") {
        tags.forEach(e => $('#ul_tags').append('<li>' + e + '<button id=\"'+ 'btn_li_tags_' + e +'\">x</button></li>'));
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

// Add item to list in localstorage
function add_item_localstorage(list_name, item){
    let list_string = localStorage.getItem(list_name);

    if (!list_string == ''){
        localStorage.setItem(list_name, list_string+ ',' + item);
    } else {
        localStorage.setItem(list_name, item);
    }

}


// Input Events
$('#input_modal_add_ingredient').on('input', ()=>{
    $('#btn_modal_add_ingredient').prop('disabled', true);
    $('#span_modal_add_ingredient').html('');
});

$('#input_modal_add_tag').on('input', ()=>{
    $('#btn_modal_add_tag').prop('disabled', true);
    $('#span_modal_add_tag').html('');
});

//// Click Events

// Ingredient

$('#btn_add_ingredient').on('click', function() {
    new Modal({el: document.getElementById('modal_ingredients')}).show();
});

$('#btn_modal_search_ingredient').on('click', ()=>{
    
    let input_modal_add_ingredient = $('#input_modal_add_ingredient').val().toLowerCase();

    let ingredients = localStorage.getItem('ingredients').split(',');
    
    if (input_modal_add_ingredient != ''){
        if (!ingredients.includes(input_modal_add_ingredient)){
            $.ajax({
                url:'/get_ingredient_information/'+input_modal_add_ingredient,
                datatype:'json',
                type:'GET',
                success:function(data){
                    $('#btn_modal_add_ingredient').prop('disabled', false);
                    $('#span_modal_add_ingredient').html('Ingredient was found');
                },
                error:function(e){
                    $('#span_modal_add_ingredient').html('Ingredient was not found');
                    console.error(e);
                },
            });
        } else {
            $('#span_modal_add_ingredient').html('You already have that ingredient');
        }
    } else {
        $('#span_modal_add_ingredient').html('Please, enter a valid name');
    }
    
    

    
});

$('#btn_modal_add_ingredient').on('click', ()=>{
    let  input_modal_add_ingredient = $('#input_modal_add_ingredient').val().toLowerCase();
    
    if (input_modal_add_ingredient != ''){
        console.log(input_modal_add_ingredient)
        add_item_localstorage('ingredients', input_modal_add_ingredient);

        update_ingredients_list();
    }

    $('#btn_modal_add_ingredient').prop('disabled', true);
    $('#span_modal_add_ingredient').html('');
    $('#input_modal_add_ingredient').val('');

});

// Add click event to each li in ul_ingredients component
$('#ul_ingredients').on('click', 'button[id^="btn_li_ing_"]', (event) =>  {

    let clicked_button = event.target.id;

    let ingredients = localStorage.getItem('ingredients').split(',');

    let filtered_ingredients = ingredients.filter(e => "btn_li_ing_" + e != clicked_button);
    
    localStorage.setItem('ingredients', filtered_ingredients);

    update_ingredients_list();

  });

$('#btn_modal_create_ingredient').on('click', ()=>{

    let input_modal_create_ingredient = $('#input_modal_create_ingredient').val().toLowerCase();

    if (input_modal_create_ingredient != ''){
        let data = {
            'ingredient_name':input_modal_create_ingredient,
        };
    
        $.ajax({
            url:'/propose_new_ingredient/',
            datatype:'text',
            type:'POST',
            data:data,
            success:function(data, status, xhr){
                add_item_localstorage('ingredients', input_modal_create_ingredient);
                update_ingredients_list();
                $('#input_modal_create_ingredient').val('');
                $('#span_modal_create_ingredient').html('Ingredient has been successfully created and added');
                
            },
            error:function(e){
                let status_code = e.status;
                if (status_code === 461){                    
                    $('#span_modal_create_ingredient').html('That ingredient already exists');
                } else {
                    $('#span_modal_create_ingredient').html('Something went wrong');
                    $('#input_modal_create_ingredient').val('');
                }
            },
        });
    } else {
        $('#span_modal_create_ingredient').html('Please, enter a valid name');
    }
    

});



// Tags

$('#btn_add_tag').on('click', function() {
    new Modal({el: document.getElementById('modal_tags')}).show();
});

$('#btn_modal_search_tag').on('click', ()=>{
    
    let input_modal_add_tag = $('#input_modal_add_tag').val().toLowerCase();;

    let tags = localStorage.getItem('tags').split(',');

    if (input_modal_add_tag != ''){
        if (!tags.includes(input_modal_add_tag)){
            $.ajax({
                url:'/get_tag_information/'+input_modal_add_tag,
                datatype:'json',
                type:'GET',
                success:function(data){
                    $('#btn_modal_add_tag').prop('disabled', false);
                    $('#span_modal_add_tag').html('tag was found');
                },
                error:function(e){
                    $('#span_modal_add_tag').html('tag was not found');
                    console.error(e);
                },
            });
        } else {
            $('#span_modal_add_tag').html('You already have that tag');
        }
    } else {
        $('#span_modal_add_tag').html('Please, enter a valid name');
    }
    

});

$('#btn_modal_add_tag').on('click', ()=>{
    let  input_modal_add_tag = $('#input_modal_add_tag').val().toLowerCase();;
    
    if (input_modal_add_tag != ''){ 

            add_item_localstorage('tags', input_modal_add_tag);

            update_tags_list();

            $('#btn_modal_add_tag').prop('disabled', true);
            $('#span_modal_add_tag').html('');
            $('#input_modal_add_tag').val('');


    }

    
});

// Add click event to each li in ul_tags component
$('#ul_tags').on('click', 'button[id^="btn_li_tags_"]', (event) =>  {

let clicked_button = event.target.id;

let tags = localStorage.getItem('tags').split(',');

let filtered_tags = tags.filter(e => "btn_li_tags_" + e != clicked_button);

localStorage.setItem('tags', filtered_tags);

update_tags_list();

});

$('#btn_modal_create_tag').on('click', ()=>{

    let input_modal_create_tag = $('#input_modal_create_tag').val();

    if (input_modal_create_tag != ''){
        let data = {
            'tag_name':input_modal_create_tag,
        };
    
        $.ajax({
            url:'/propose_new_tag/',
            datatype:'text',
            type:'POST',
            data:data,
            success:function(data, status, xhr){
                add_item_localstorage('tags', input_modal_create_tag);
                update_tags_list();
                $('#span_modal_create_tag').html('Tag has been successfully created and added');
                $('#input_modal_create_tag').val('');
            },
            error:function(e){
                let status_code = e.status;
                if (status_code === 461){                    
                    $('#span_modal_create_tag').html('That tag already exists');
                } else {
                    $('#span_modal_create_tag').html('Something went wrong');
                    $('#input_modal_create_tag').val('');
                }
            },
        });
    } else {
        $('#span_modal_create_tag').html('Please, enter a valid name');
    }

});

// Delete Post

$('#btn_delete_post').on('click', ()=>{

    if (confirm('Are you sure that you want to delete this post?')){

        let post_id = $('#input_post_id').val();

        let data = {
            'post_id':post_id,
        };

        $.ajax({
            url:'/delete_post/',
            datatype:'text',
            type:'POST',
            data:data,
            success:function(){
                console.log('Post Deleted Successfully');
                window.location = '/';
            },
            error:function(e){
                console.log(e);
            },
        });
    }
});


// Update Post


$('#btn_edit_post').on('click', ()=> {

    let post_id = $('#input_post_id').val();
  
    let input_recipe_name = $('#input_recipe_name').val();
  
    let ingredients_list = localStorage.getItem('ingredients');
  
    let tags_list = localStorage.getItem('tags');
  
    let visibility = $('#select_visibility').val();
    
    let textarea_instructions = $('#textarea_instructions').val();
  
    let data = {
      'post_id':post_id,
      'recipe_name':input_recipe_name, 
      'ingredients':ingredients_list,
      'tags':tags_list,
      'visibility':visibility,
      'instructions':textarea_instructions,
    };
  
    $.ajax({
        url:'/edit_post/',
        datatype:'text',
        type:'POST',
        data:data,
        success:function(data){
            console.log('Post has been successfully updated');
            window.location = '/';
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