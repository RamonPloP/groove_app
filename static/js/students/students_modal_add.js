    // Lógica para mostrar y ocultar los campos dependiendo de las selecciones
    document.getElementById("chronic_disease_group").hidden = true;
    document.getElementById("allergies_group").hidden = true;
    document.getElementById("restricted_activities_group").hidden = true;
    document.getElementById("mental_conditions_group").hidden = true;

    // Enfermedades crónicas
    $('#has_chronic_disease').on('change', function() {
        if ($(this).val() == 'true') {
            document.getElementById("chronic_disease_group").hidden = false;
            $("#chronic_disease_group input").prop('disabled', false);
        } else {
            document.getElementById("chronic_disease_group").hidden = true;
            $("#chronic_disease_group input").prop('disabled', true);
        }
    });

    // Alergias
    $('#has_allergies').on('change', function() {
        if ($(this).val() == 'true') {
            document.getElementById("allergies_group").hidden = false;
            $("#allergies_group input").prop('disabled', false);
        } else {
            document.getElementById("allergies_group").hidden = true;
            $("#allergies_group input").prop('disabled', true);
        }
    });

    // Actividades restringidas
    $('#has_restricted_activities').on('change', function() {
        if ($(this).val() == 'true') {
            document.getElementById("restricted_activities_group").hidden = false;
            $("#restricted_activities_group input").prop('disabled', false);
        } else {
            document.getElementById("restricted_activities_group").hidden = true;
            $("#restricted_activities_group input").prop('disabled', true);
        }
    });

    // Condiciones mentales
    $('#has_mental_conditions').on('change', function() {
        if ($(this).val() == 'true') {
            document.getElementById("mental_conditions_group").hidden = false;
            $("#mental_conditions_group input").prop('disabled', false);
        } else {
            document.getElementById("mental_conditions_group").hidden = true;
            $("#mental_conditions_group input").prop('disabled', true);
        }
    });

    $('.select2').select2({
        placeholder: 'Selecciona una opción',
        allowClear: true,
    });