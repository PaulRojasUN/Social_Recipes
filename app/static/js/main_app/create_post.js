
// When DOM is ready
$(function(){
    localStorage.setItem('ingredients',""); 
    localStorage.setItem('tags',""); 
 });

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
    
    let  input_modal_add_ingredient = $('#input_modal_add_ingredient').val();

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
    
});

$('#btn_modal_add_ingredient').on('click', ()=>{
    let  input_modal_add_ingredient = $('#input_modal_add_ingredient').val();
    
    if (input_modal_add_ingredient != ''){
        let ingredients_string = localStorage.getItem('ingredients');

        if (!ingredients_string == ''){
            localStorage.setItem('ingredients', ingredients_string+ ',' + input_modal_add_ingredient);
        } else {
            localStorage.setItem('ingredients', input_modal_add_ingredient);
        }

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



// Tags

$('#btn_add_tag').on('click', function() {
    new Modal({el: document.getElementById('modal_tags')}).show();
});

$('#btn_modal_search_tag').on('click', ()=>{
    
    let  input_modal_add_tag = $('#input_modal_add_tag').val();

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
    
});

$('#btn_modal_add_tag').on('click', ()=>{
    let  input_modal_add_tag = $('#input_modal_add_tag').val();
    
    if (input_modal_add_tag != ''){
        let tags_string = localStorage.getItem('tags');

        if (!tags_string == ''){
            localStorage.setItem('tags', tags_string+ ',' + input_modal_add_tag);
        } else {
            localStorage.setItem('tags', input_modal_add_tag);
        }

        update_tags_list();
    }

    $('#btn_modal_add_tag').prop('disabled', true);
    $('#span_modal_add_tag').html('');
    $('#input_modal_add_tag').val('');

});

// Add click event to each li in ul_tags component
$('#ul_tags').on('click', 'button[id^="btn_li_tags_"]', (event) =>  {

let clicked_button = event.target.id;

let tags = localStorage.getItem('tags').split(',');

let filtered_tags = tags.filter(e => "btn_li_tags_" + e != clicked_button);

localStorage.setItem('tags', filtered_tags);

update_tags_list();

});
