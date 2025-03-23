
     $(function() {
      get_data('/teachers/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/teachers/' + id
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
        e.preventDefault();
        var form = $("#form")[0];

        let data_form = new FormData(form);

        if(!data_form.get('id')){
            data_form.set('payment', $('#payment').maskMoney('unmasked')[0]);
        }

        let selectedClasses = $('#classes').val();
        data_form.set('classes', JSON.stringify(selectedClasses));

        if (!form.checkValidity()) {
            form.reportValidity();
        } else {
            $("#create_button").prop("disabled", true);

            axios({
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                url: '/teachers/crud',
                data: JSON.stringify({
                    id: data_form.get('id'),
                    name: data_form.get('name'),
                    phone: data_form.get('phone'),
                    payment: data_form.get('payment'),
                    classes: JSON.parse(data_form.get('classes'))
                })
            })
            .then(function (response) {
                toastr.success(response.data, { timeOut: 9500 });
                get_data('/teachers/list?page=0');
                $('#data_modal').modal("hide");
            })
            .catch(function (error) {
                toastr.error(error.response.data);
                console.log(error);
            })
            .finally(function () {
                $("#create_button").prop("disabled", false);
            });
        }
    }



    function add_new(button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/teachers/add'
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
    let teachers = []
    $.each(data, function (i, element) {
        let teacher = []
        teacher.push(element.id)
        teacher.push(element.name)
        teacher.push(element.phone)
        teacher.push('$'+element.payment)
        let classes = ''
        for(let i in element.classes){
            classes += '<span class="badge badge-success">'+element.classes[i]+'</span> '
        }
        teacher.push(classes)
        teacher.push('<button type="button" class="btn btn-outline-primary" onclick="show_info('+element.id +', this)">'+
                            '<i class="fas fa-edit"></i>'+
                        '</button>'+'<button type="button" class="btn btn-outline-danger" onclick="delete_teacher('+element.id +', this)">'+
                            '<i class="fas fa-trash"></i>'+
                        '</button>')
        teachers.push(teacher)
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
        data: teachers,
        columns: [
            {title: "ID"},
            {title: "NOMBRE"},
            {title: "TELÉFONO"},
            {title: "SUELDO"},
            {title: "CLASES"},
            {title: "ACCIONES"}
        ]
    });
}

function delete_teacher(id) {
    let teacherToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/teachers/delete',
            data: {teacher_id: teacherToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/teachers/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}
