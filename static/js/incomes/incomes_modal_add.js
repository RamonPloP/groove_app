
document.getElementById("description").hidden = true;
document.getElementById("description").querySelector('input').disabled = true;
document.getElementById("members").hidden = true;
document.getElementById("members").querySelector('select').disabled = true;

$('#concept').on('change', () => {
    if (['other', '9', '8'].includes($('#concept').val())){
        document.getElementById("description").hidden = false;
        document.getElementById("description").querySelector('input').disabled = false;  // Habilitar el input
    } else {
        document.getElementById("description").hidden = true;
        document.getElementById("description").querySelector('input').disabled = true;  // Deshabilitar el input
    }

    if ($('#concept').val() == 4 || $('#concept').val() == 5) {
        document.getElementById("members").hidden = false;
        document.getElementById("members").querySelector('select').disabled = false;  // Habilitar el select
    } else {
        document.getElementById("members").hidden = true;
        document.getElementById("members").querySelector('select').disabled = true;  // Deshabilitar el select
    }

    if ($('#concept').val() == 4 ){
        document.getElementById("total_group").hidden = true;
        document.getElementById("total").disabled = true;  // Deshabilitar el select
    }else{
        document.getElementById("total_group").hidden = false;
        document.getElementById("total").disabled = false;
    }

});

$('.select2').select2({
    placeholder: 'Selecciona una opción',
    allowClear: true,
});
