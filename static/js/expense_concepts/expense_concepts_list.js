     $(function() {
      get_data('/expense-concepts/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/expense-concepts/' + id
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
                url: '/expense-concepts/crud',
                data: new FormData(form)
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_data('/expense-concepts/list?page=0')
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
            url: '/expense-concepts/add'
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
    let expense_concepts = []
    $.each(data, function (i, element) {
        let expense_concept = []
        expense_concept.push(element.id)
        expense_concept.push(element.name)
        expense_concept.push('<button type="button" class="btn btn-outline-primary" onclick="show_info('+element.id +', this)">'+
                            '<i class="fas fa-edit"></i>'+
                        '</button>'+'<button type="button" class="btn btn-outline-danger" onclick="delete_expense_concept('+element.id +', this)">'+
                            '<i class="fas fa-trash"></i>'+
                        '</button>')
        expense_concepts.push(expense_concept)
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
        data: expense_concepts,
        columns: [
            {title: "ID"},
            {title: "NOMBRE"},
            {title: "ACCIONES"}
        ]
    });
}

function delete_expense_concept(id) {
    let expense_conceptToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/expense-concepts/delete',
            data: {expense_concept_id: expense_conceptToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/expense-concepts/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}
