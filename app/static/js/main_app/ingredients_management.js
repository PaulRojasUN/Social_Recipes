$('#input_search_ingredient').on('input', ()=> {
    $("#btn_approve").prop('disabled', true);
    $('#fixed_input_ingredient_name').val('');
    $('#input_classified_state').val('')
  });

  $('#input_search_mig').on('input', ()=>{
    $('#btn_del_mig').prop('disabled', true);
    $('#p_del_mig_info').prop('hidden', true);
  })
  
  
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
  

  $('#btn_search_mig').on('click', ()=>{
    let ingredient_name = $('#input_search_mig').val();
  
    $.ajax({
      url:'/get_ingredient_information/'+ingredient_name,
      datatype:'json',
      type:'GET',
      success:function(data){
        let target_ingredient = data.name.toLowerCase();
        let migrate_ingredient = $('#fixed_input_ingredient_name').val().toLowerCase();  
        
        if (target_ingredient != migrate_ingredient){
          if (data.classified==0){
            $('#p_del_mig_info').html(`The ingredient ${migrate_ingredient} is going to be deleted and associated instances' relations are going to migrate to ${target_ingredient}`);
            $('#btn_del_mig').prop('disabled', false);
          } else {
            $('#p_del_mig_info').html('This ingredient is unclassified too. Cannot be used as a target ingredient');
          }
        } else {
          $('#p_del_mig_info').html('The target ingredient cannot be that');
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
  
    
      let migrate_ingredient = $('#fixed_input_ingredient_name').val(); 
      let target_ingredient = $('#input_search_mig').val();
  
      let data = {
        migrate_ingredient:migrate_ingredient,
        target_ingredient:target_ingredient,
      }
  
      $.ajax({
        url:'/migrate_ingredient/',
        datatype:'text',
        type:'POST',
        data:data,
        success:function(res){
          $('#input_search_ingredient').val('');        
          $('#fixed_input_ingredient_name').val('');        
          $('#input_classified_state').val('');      
          $('#btn_approve').prop('disabled', true);      
          $('#input_search_mig').val('');
          $('#btn_search_mig').prop('disabled', true);      
          $('#btn_del_mig').prop('disabled', true);
          $('#p_del_mig_info').prop('hidden', true);
        },
        error:function(e){
          console.log(e);
        },
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