     $(function() {
      get_data('/attendances/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/attendances/' + id
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
    let attendances = []
    $.each(data, function (i, element) {
        let attendance = []
        attendance.push(element.id)
        attendance.push(element.name)
        attendance.push('<button type="button" class="btn btn-outline-danger" onclick="delete_class('+element.id +', this)">'+
                            '<i class="fas fa-trash"></i>'+
                        '</button>')
        attendances.push(attendance)
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
        data: attendances,
        columns: [
            {title: "ID"},
            {title: "MIEMBRO"},
            {title: "FECHA"},
            {title: "ACCIONES"}
        ]
    });
}

function delete_attendance(id) {
    let attendanceToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/attendances/delete',
            data: {attendance_id: attendanceToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/attendances/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}


