     $(function() {
      get_data('/leads/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/leads/' + id
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
                url: '/leads/crud',
                data: data_form
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_data('/leads/list?page=0')
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
            url: '/leads/add'
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
        item.push(element.assist_date)
        item.push(element.phone)
        item.push(element.age)
        item.push(element.sample_class)
        item.push(element.social_media_link)
        if(element.observations){
            item.push(element.observations)
        }else{
            item.push('-')
        }
        let btns = ['<button type="button" class="btn btn-outline-primary" onclick="show_modal('+element.id+', \'/leads/'+element.id+'\')" title="Editar">'+
                                            '<i class="fas fa-edit"></i>'+
                                        '</button>'+'<button type="button" class="btn btn-outline-danger" onclick="delete_lead('+element.id+', this)">'+
                        '<i class="fas fa-trash"></i>'+'</button>'+'<button type="button" class="btn btn-outline-success" onclick="show_modal('+element.id+', \'/leads/add/observation/'+element.id+'\')">'+
                        '<i class="fas fa-info-circle"></i>'+'</button>']

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
            {title: "AGENDA"},
            {title: "TELÉFONO"},
            {title: "EDAD"},
            {title: "CLASE"},
            {title: "RED SOCIAL"},
            {title: "OBSERVACIONES"},
            {title: "ACCIONES"}

        ]
    });
}

function delete_lead(id) {
    let leadToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/leads/delete',
            data: {leadToDelete: leadToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/leads/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
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

    function register_observation(e) {
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
                url: '/leads/add/observation',
                data: data_form
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_data('/leads/list?page=0')
                $('#data_modal').modal("hide")
            }).catch(function (error) {
                toastr.error(error.response.data)
                console.log(error)
            }).finally(function () {

            });
        }
    }