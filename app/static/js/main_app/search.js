$('#btn_search').on('click', ()=>{

    let par1 = $('#input_search').val();

    window.location = `/filter/?par1=${par1}`;
});