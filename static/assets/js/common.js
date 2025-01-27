/*Funtion to get de data in json and pass to the datatable*/
function get_data(url) {
        $.getJSON(url, function (data) {
                update_table(data)
            }
        );
    }

/*Funtion to generate de datatable and fill whit de json data */

function update_table(data) {
    banks = []
    $.each(data, function (i, element) {
        bank = []
        bank.push(element.id)
        bank.push(element.name)
        bank.push('<button type="button" class="btn btn-outline-primary" onclick="show_info('+element.id +', this)">'+
                            '<i class="fas fa-edit"></i>'+
                        '</button>')
        banks.push(bank)
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
            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
        },
        data: banks,
        columns: [
            {title: "ID"},
            {title: "NOMBRE"},
            {title: "ACCIONES"}
        ]
    });
}

