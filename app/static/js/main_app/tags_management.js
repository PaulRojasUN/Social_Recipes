$('#input_search_tag').on('input', ()=> {
  $("#btn_approve").prop('disabled', true);
  $('#fixed_input_tag_name').val('');
  $('#input_classified_state').val('');
  $('#input_search_mig').val('');
  $('#input_search_mig').prop('disabled', true);
  $('#btn_search_mig').prop('disabled', true);
  $('#btn_del_mig').prop('disabled', true);
  $('#p_del_mig_info').prop('hidden', true);
});

$('#input_search_mig').on('input', ()=>{
  $('#btn_del_mig').prop('disabled', true);
  $('#p_del_mig_info').prop('hidden', true);
})


$('#btn_create_tag').on('click', () => {

  let tag_name = $('#input_tag_name').val();

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
                  $('#input_tag_name').val('');
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

$('#btn_search_tag').on('click', () => {
      
  let tag_name = $('#input_search_tag').val();
  
  $.ajax({
    url:'/get_tag_information/'+tag_name,
    datatype:'json',
    type:'GET',
    success:function(data){
      $('#fixed_input_tag_name').val(data.name);

      if (data.classified==0){
        $("#btn_approve").prop('disabled', true);
        $('#input_classified_state').val('Classified');
        $('#input_search_mig').prop('disabled', true);
        $('#btn_search_mig').prop('disabled', true);
        $('#btn_del_mig').prop('disabled', true);
      } else {
        $("#btn_approve").prop('disabled', false);
        $('#input_classified_state').val('Not Classified');
        $('#input_search_mig').prop('disabled', false);
        $('#btn_search_mig').prop('disabled', false);
        $('#btn_del_mig').prop('disabled', true);
      }
    },
    error:function(e){
      console.log(e);
    }
  })
});

$('#btn_approve').on('click', () => {
      
  if (confirm("Are you sure that you want to do that? Results may be irrevocable")){
    let tag_name = $('#input_search_tag').val();
    
    let data = {
      'tag_name':tag_name,
    }

    $.ajax({
      url:'/set_classified_tag/',
      datatype:'text',
      type:'POST',
      data:data,
      success:function(data){
        $("#btn_approve").prop('disabled', true);
        $('#input_classified_state').val('Classified')
      },
      error:function(e){
        console.log(e);
      }
    })
  }
  
});

$('#btn_search_mig').on('click', ()=>{
  let tag_name = $('#input_search_mig').val();

  $.ajax({
    url:'/get_tag_information/'+tag_name,
    datatype:'json',
    type:'GET',
    success:function(data){
      let target_tag = data.name.toLowerCase();
      let migrate_tag = $('#fixed_input_tag_name').val().toLowerCase();  
      
      if (target_tag != migrate_tag){
        if (data.classified==0){
          $('#p_del_mig_info').html(`The tag ${migrate_tag} is going to be deleted and associated instances' relations are going to migrate to ${target_tag}`);
          $('#btn_del_mig').prop('disabled', false);
        } else {
          $('#p_del_mig_info').html('This tag is unclassified too. Cannot be used as a target tag');
        }
      } else {
        $('#p_del_mig_info').html('The target tag cannot be the same as ' + target_tag);
      }
      $('#p_del_mig_info').prop('hidden', false);
    },
    error:function(e){
      $('#p_del_mig_info').prop('hidden', true);

    }
  })
})

$('#btn_del_mig').on('click', ()=>{

  if (confirm('Are you sure you want to do that? Changes may be irrevocable')){

  
    let migrate_tag = $('#fixed_input_tag_name').val(); 
    let target_tag = $('#input_search_mig').val();

    let data = {
      migrate_tag:migrate_tag,
      target_tag:target_tag,
    }

    $.ajax({
      url:'/migrate_tag/',
      datatype:'text',
      type:'POST',
      data:data,
      success:function(res){
        $('#input_search_tag').val('');        
        $('#fixed_input_tag_name').val('');        
        $('#input_classified_state').val('');      
        $('#btn_approve').prop('disabled', true);      
        $('#input_search_mig').val('');
        $('#btn_search_mig').prop('disabled', true);      
        $('#btn_del_mig').prop('disabled', true);
        $('#p_del_mig_info').prop('hidden', true);
      },
      error:function(e){
        console.log(e);
      }

    
    });

  }
})



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