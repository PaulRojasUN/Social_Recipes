$('#input_search_ingredient').on('input', ()=> {
    $("#btn_approve").prop('disabled', true);
    $('#fixed_input_ingredient_name').val('');
    $('#input_classified_state').val('')
  });
  
  
  $('#btn_create_ingredient').on('click', () => {
  
    let ingredient_name = $('#input_ingredient_name').val();
  
    if (ingredient_name != ''){
        $.ajax({
            url:'/create_ingredient/',
            datatype:'text',
            type:'POST',
            data:{
                'ingredient_name':ingredient_name,
            },
            success:function(res, status, xhr){
                status_code = xhr.status;
                if (status_code == 200){
                    $('#input_ingredient_name').val('');
                    console.log('ingredient created successfully');
                } else if (status_code == 461){
                    console.log('Another ingredient exists with that name');
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
  
  $('#btn_search_ingredient').on('click', () => {
        
    let ingredient_name = $('#input_search_ingredient').val();
    
    $.ajax({
      url:'/get_ingredient_information/'+ingredient_name,
      datatype:'json',
      type:'GET',
      success:function(data){
        $('#fixed_input_ingredient_name').val(data.name);
  
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
      let ingredient_name = $('#input_search_ingredient').val();
      
      let data = {
        'ingredient_name':ingredient_name,
      }
  
      $.ajax({
        url:'/set_classified_ingredient/',
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