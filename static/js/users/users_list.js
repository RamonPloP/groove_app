    $(function () {
       get_users()
    });

    function get_users() {
        $.getJSON('/users/list', function (data) {
                update_table(data)
            }
        );
    }

    function update_table(data) {
        users = []
        $.each(data, function (i, element) {
            user = []
            user.push(element.id)
            user.push(element.name)
            user.push(element.username)
            if (element.role == 'ADMIN') {
                user.push('Administrador')
            }
            else if (element.role =='USER') {
                user.push('Usuario')
            }

            if (element.status == 1) user.push('Activo');

            if (element.status == 0) user.push('Inactivo');

            if(element.status == 0){
                btn = '<button type="button" class="btn btn-outline-success" title="Cambiar a activo" onclick="changeActive('+element.id +')">'+
                                '<i class="fas fa-check"></i>'+
                            '</button>';
            }else{
                if(current_user_id == element.id){
                    btn = ''
                }else{
                    btn = '<button type="button" class="btn btn-outline-danger" title="Cambiar a inactivo" onclick="changeInactive('+element.id +')">'+
                                '<i class="fas fa-times"></i>'+
                            '</button>'+'<button type="button" class="btn btn-outline-danger" onclick="delete_user('+element.id +', this)">'+
                            '<i class="fas fa-trash"></i>'+
                        '</button>';
                }
            }

            user.push('<button type="button" class="btn btn-outline-primary" onclick="show_info('+element.id +', this)">'+
                                '<i class="fas fa-edit"></i>'+
                            '</button>'+btn)
            users.push(user)
        })
        $('#table_list').DataTable().clear();
        $('#table_list').DataTable().destroy();
        $('#table_list').DataTable({
            dom: 'lBfrtip',
              "buttons": [
                'excel'
              ],
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
            },
            data: users,
            responsive: true,
            columns: [
                {title: "ID"},
                {title: "NOMBRE"},
                {title: "CORREO"},
                {title: "PERMISO"},
                {title: "ESTATUS"},
                {title: "ACCIONES"}
            ]

        });
    }

    function changeActive(id){
        url = '/users/changeactive/'+id;
        console.log(url);
        axios.post(url).then(function (response) {
            console.log(response);
            get_users();
          }).catch(function (error) {
            console.log(error);
          })
    }

    function changeInactive(id){
        url = '/users/changeinactive/'+id;
        console.log(url);
        axios.post(url).then(function (response) {
            console.log(response);
            get_users()
          }).catch(function (error) {
            console.log(error);
          })
    }

     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/users/' + id
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
        if ($('#password').val() != $('#password2').val()){
            toastr.error('Las contraseñas no coinciden')
            return 0
        }
        var form = $("#addForm")[0]
        if (!form.checkValidity())
            form.reportValidity()
        else {
            $("#create_button").prop("disabled", true)
            axios({
                method: 'post',
                url: '/users/crud',
                data: new FormData(form)
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_users()
                $('#data_modal').modal("hide")
            }).catch(function (error) {
                toastr.error(error.response.data)
                $("#create_button").prop("disabled", false)
                console.log(error.response)
            }).finally(function () {
            });
        }
    }
function edit(e) {
        e.preventDefault()
        if ($('#password').val() != $('#password2').val()){
            toastr.error('Las contraseñas no coinciden')
            return 0
        }
        var form = $("#addForm")[0]
        if (!form.checkValidity())
            form.reportValidity()
        else {
            $("#create_button").prop("disabled", true)
            axios({
                method: 'post',
                url: '/users/edit',
                data: new FormData(form)
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_users()
                $('#data_modal').modal("hide")
            }).catch(function (error) {
                toastr.error(error.response.data)
                $("#create_button").prop("disabled", false)
                console.log(error.response)
            }).finally(function () {
            });
        }
    }
    function add_new(button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/users/add'
        }).then(function (response) {
            $('#data_modal').html(response.data)
            $('#data_modal').modal("show")
        }).catch(function (error) {
            console.log(error)
        }).finally(function () {
            $(button).attr('disabled', false);
        });
     }

    function delete_user(id) {
        $('#confirmationModal').modal('show');
        $('#confirmDeleteButton').off('click').on('click', function() {
            axios({
                    method: 'post',
                    headers: {
                    'Content-Type': 'application/json'
                    },
                    url: '/users/delete',
                    data: {user_id:id}
                }).then(function (response) {
                    $('#confirmationModal').modal('hide');
                    toastr.success(response.data, { timeOut: 9500 })
                    get_users()
                }).catch(function (error) {
                    $('#confirmationModal').modal('hide');
                    toastr.error(error.response.data)
                    $("#create_button").prop("disabled", false)
                    console.log(error.response)
                }).finally(function () {
                    $('#confirmationModal').modal('hide');
                    $("form :input").prop("readonly", false)
                    $('form select').css('pointer-events', 'all')
            });
        });
    }