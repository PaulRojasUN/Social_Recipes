$('#input_search_tag').on('input', ()=> {
  $("#btn_approve").prop('disabled', true);
  $('#fixed_input_tag_name').val('');
  $('#input_classified_state').val('')
});


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
        $('#input_classified_state').val('Classified')
      } else {
        $("#btn_approve").prop('disabled', false);
        $('#input_classified_state').val('Not Classified')
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