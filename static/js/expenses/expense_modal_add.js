document.getElementById("description").hidden = true;
document.getElementById("description").querySelector('input').disabled = true;
document.getElementById("staff").hidden = true;
document.getElementById("staff").querySelector('select').disabled = true;

$('#concept, #staff').on('change', () => {
    // Verificar si 'concept' o 'staff' tienen el valor 'other'
    if ($('#concept').val() == 'other' || $('#concept').val() == 8 || $('#concept').val() == 15 || $('#concept').val() == 9 ||$('#worker').val() == 'other') {
        document.getElementById("description").hidden = false;
        document.getElementById("description").querySelector('input').disabled = false;  // Habilitar el input
    } else {
        document.getElementById("description").hidden = true;
        document.getElementById("description").querySelector('input').disabled = true;  // Deshabilitar el input
    }

    // Mostrar el campo de 'staff' solo si 'concept' tiene valor 7
    if ($('#concept').val() == 7) {
        document.getElementById("staff").hidden = false;
        document.getElementById("staff").querySelector('select').disabled = false;  // Habilitar el select
    } else {
        document.getElementById("staff").hidden = true;
        document.getElementById("staff").querySelector('select').disabled = true;  // Deshabilitar el select
    }
});

$('.select2').select2({
    placeholder: 'Selecciona una opción',
    allowClear: true,
});

