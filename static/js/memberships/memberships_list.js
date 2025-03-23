
     $(function() {
      get_data('/memberships/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/memberships/' + id
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
        if(!data_form.get('id')){
            data_form.set('cost',$('#cost').maskMoney('unmasked')[0])
        }
        if (!form.checkValidity())
            form.reportValidity()
        else {
            $("#create_button").prop("disabled", true)
            axios({
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                url: '/memberships/crud',
                data: data_form
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_data('/memberships/list?page=0')
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
            url: '/memberships/add'
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
    let memberships = []
    $.each(data, function (i, element) {
        let membership = []
        membership.push(element.id)
        membership.push(element.name)
        membership.push('$ '+element.cost)
        membership.push('<button type="button" class="btn btn-outline-primary" onclick="show_info('+element.id +', this)">'+
                            '<i class="fas fa-edit"></i>'+
                        '</button>'+'<button type="button" class="btn btn-outline-danger" onclick="delete_membership('+element.id +', this)">'+
                            '<i class="fas fa-trash"></i>'+
                        '</button>')
        memberships.push(membership)
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
        data: memberships,
        columns: [
            {title: "ID"},
            {title: "NOMBRE"},
            {title: "COSTO"},
            {title: "ACCIONES"}
        ]
    });
}

function delete_membership(id) {
    let membershipToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/memberships/delete',
            data: {membership_id: membershipToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/memberships/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}
