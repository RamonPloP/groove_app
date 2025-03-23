     $(function() {
      get_data('/students/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/students/' + id
        }).then(function (response) {
            $('#data_modal').html(response.data)
            $('#data_modal').modal("show")
        }).catch(function (error) {
            console.log(error)
        }).finally(function () {
            $(button).attr('disabled', false);
        });


    }
    function register(e) {
        e.preventDefault()
        var form = $("#addForm")[0]
        let data_form = new FormData(form)

        if (!form.checkValidity())
            form.reportValidity()
        else {
            $("#create_button").prop("disabled", true)
            axios({
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                url: '/students/crud',
                data: data_form
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_data('/students/list?page=0')
                $('#data_modal').modal("hide")
            }).catch(function (error) {
                toastr.error(error.response.data)
                console.log(error)
            }).finally(function () {

            });
        }
    }

    function add_new(button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/students/add'
        }).then(function (response) {
            $('#data_modal').html(response.data)
            $('#data_modal').modal("show")
        }).catch(function (error) {
            console.log(error)
        }).finally(function () {
            $(button).attr('disabled', false);
        });
     }

     /*Funtion to get de data in json and pass to the datatable*/
function get_data(url) {
        $.getJSON(url, function (data) {
                update_table(data)
            }
        );
    }

/*Funtion to generate de datatable and fill whit de json data */

function update_table(data) {
    let elements = []
    $.each(data, function (i, element) {
        let item = []
        item.push(element.id)
        item.push(element.name)
        item.push(element.last_name)
        item.push(element.second_last_name || '-')
        item.push(element.start_date || '-')
        item.push(element.email || '-')
        item.push(element.membership)
        item.push(element.how_find_us_text)
        item.push(element.expire_date)
        item.push(element.dance_reason_text || '-')
        item.push(element.address || '-')
        item.push(element.birth_date || '-')
        item.push(element.birth_place || '-')
        item.push(element.nationality || '-')
        item.push(element.blood_type_text)
        item.push(element.phone || '-')
        item.push(element.dad_name || '-')
        item.push(element.dad_phone || '-')
        item.push(element.mom_name || '-')
        item.push(element.mom_phone || '-')
        item.push(element.emergency_contact_name || '-')
        item.push(element.emergency_contact_phone || '-')
        item.push(element.has_chronic_disease ? 'Sí' : 'No')
        item.push(element.chronic_disease || '-')
        item.push(element.has_allergies ? 'Sí' : 'No')
        item.push(element.allergies || '-')
        item.push(element.has_restricted_activities ? 'Sí' : 'No')
        item.push(element.restricted_activities || '-')
        item.push(element.has_mental_conditions ? 'Sí' : 'No')
        item.push(element.mental_conditions || '-')
        let btns = ['<button type="button" class="btn btn-outline-primary" onclick="show_modal('+element.id+', \'/students/'+element.id+'\')" title="Editar">'+
                                            '<i class="fas fa-edit"></i>'+
                                        '</button>'+'<button type="button" class="btn btn-outline-danger" onclick="delete_student('+element.id+', this)">'+
                        '<i class="fas fa-trash"></i>'+'</button>'+
                    '<button type="button" class="btn btn-outline-secondary" onclick="show_modal('+element.id+', \'/students/modal/regulation-pdf/'+element.id+'\')" title="Agregar reglamento">'+
                                        '<i class="fas fa-file-pdf"></i>'+
                                    '</button>']

        item.push(btns.join(''));
        elements.push(item)
    })


    $('#datatable_list').DataTable().clear();
    $('#datatable_list').DataTable().destroy();
    $('#datatable_list').DataTable({
        dom: 'lBfrtip',
          "buttons": [
            'excel'
          ],
        responsive: true,
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
        },
        data: elements,
        columns: [
            {title: "ID"},
            {title: "NOMBRE"},
            {title: "APELLIDO PATERNO"},
            {title: "APELLIDO MATERNO"},
            {title: "FECHA DE INICIO"},
            {title: "EMAIL"},
            {title: "MEMBRESÍA"},
            {title: "CÓMO NOS CONOCIÓ"},
            {title: "FECHA DE VENCIMIENTO"},
            {title: "RAZÓN PARA BAILAR"},
            {title: "DIRECCIÓN"},
            {title: "FECHA DE NACIMIENTO"},
            {title: "LUGAR DE NACIMIENTO"},
            {title: "NACIONALIDAD"},
            {title: "TIPO DE SANGRE"},
            {title: "TELÉFONO"},
            {title: "NOMBRE DEL PADRE"},
            {title: "TELÉFONO DEL PADRE"},
            {title: "NOMBRE DE LA MADRE"},
            {title: "TELÉFONO DE LA MADRE"},
            {title: "CONTACTO DE EMERGENCIA"},
            {title: "TELÉFONO DE EMERGENCIA"},
            {title: "ENFERMEDAD CRÓNICA"},
            {title: "DETALLES DE ENFERMEDAD"},
            {title: "ALERGIAS"},
            {title: "DETALLES DE ALERGIAS"},
            {title: "ACTIVIDADES RESTRINGIDAS"},
            {title: "DETALLES DE RESTRICCIONES"},
            {title: "CONDICIONES MENTALES"},
            {title: "DETALLES DE CONDICIONES"},
            {title: "ACCIONES"}

        ],
        "order": [[1, 'desc']]
    });
}

function delete_student(id) {
    let studentToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/students/delete',
            data: {studentToDelete: studentToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/students/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}

function register_pdf(e){
         e.preventDefault()
        var pdf = $('#pdf').val();
        if(pdf=='')
        {
            toastr.error('Selecciona un pdf, el campo no puede ir vacio')
            return false;
        }
        var form_data = new FormData();
        form_data.append('pdf', $('#pdf').prop('files')[0]);
        form_data.append('item_id', $('#item_id').val());
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            url: '/students/add/regulation-pdf',
            data: form_data
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 })
            get_data()
            $('#data_modal').modal("hide")
        }).catch(function (error) {
            toastr.error(error.response.data)
            $("#create_button").prop("disabled", false)
            console.log(error.response)
        }).finally(function () {
            $("form :input").prop("readonly", false)
            $('form select').css('pointer-events', 'all')
        });
    }


    function show_modal(id,url) {
        axios({
            method: 'get',
            url: url
        }).then(function (response) {
            $('#data_modal').html(response.data)
            $('#data_modal').modal("show")
        }).catch(function (error) {
            console.log(error)
            toastr.error(error.data, { timeOut: 9500 })
        });
    }