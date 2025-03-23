     $(function() {
      get_data('/classes/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/classes/' + id
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
        if (!form.checkValidity())
            form.reportValidity()
        else {
            $("#create_button").prop("disabled", true)
            axios({
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                url: '/classes/crud',
                data: new FormData(form)
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_data('/classes/list?page=0')
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
            url: '/classes/add'
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
    let classes = []
    $.each(data, function (i, element) {
        let clase = []
        clase.push(element.id)
        clase.push(element.name)
        clase.push('<button type="button" class="btn btn-outline-primary" onclick="show_info('+element.id +', this)">'+
                            '<i class="fas fa-edit"></i>'+
                        '</button>'+'<button type="button" class="btn btn-outline-danger" onclick="delete_class('+element.id +', this)">'+
                            '<i class="fas fa-trash"></i>'+
                        '</button>')
        classes.push(clase)
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
        data: classes,
        columns: [
            {title: "ID"},
            {title: "NOMBRE"},
            {title: "ACCIONES"}
        ]
    });
}

function delete_class(id) {
    let classToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/classes/delete',
            data: {class_id: classToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/classes/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}


