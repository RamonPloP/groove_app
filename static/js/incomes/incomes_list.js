$(function() {
    get_data('/incomes/list?page=0')
});

function show_info(id, button) {
    $(button).attr('disabled', true);
    axios({
        method: 'get',
        url: '/incomes/' + id
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
            url: '/incomes/crud',
            data: data_form
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 })
            get_data('/incomes/list?page=0')
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
        url: '/incomes/add'
    }).then(function (response) {
        $('#data_modal').html(response.data)
        $('#data_modal').modal("show")
    }).catch(function (error) {
        console.log(error)
    }).finally(function () {
        $(button).attr('disabled', false);
    });
}

function get_data(url) {
    $.getJSON(url, function (data) {
        update_table(data.incomes);
        update_total(data.total_incomes);
        update_chart(data.incomes_by_concept);  // Actualizar la gráfica con los nuevos datos
    });
}

function update_table(data) {
    let incomes = [];
    $.each(data, function (i, element) {
        let income = [];

        // Convertimos la fecha de DD/MM/YYYY a YYYY-MM-DD para una correcta ordenación
        let dateParts = element.date.split('/');
        let formattedDate = dateParts[0] + '/' + dateParts[1] + '/' + dateParts[2];  // Convertimos a YYYY-MM-DD

        income.push(element.id);
        income.push(formattedDate);
        income.push(element.income_concept);
        income.push(element.description || '-');
        income.push(element.member || '-');
        income.push(element.payment_type);
        income.push('$ ' + element.amount);
        income.push('<button type="button" class="btn btn-outline-danger" onclick="delete_income(' + element.id + ', this)">' +
                        '<i class="fas fa-trash"></i>' +
                    '</button>');
        incomes.push(income);
    });

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
        data: incomes,
        columns: [
            {title: "ID"},
            {title: "FECHA"},
            {title: "CONCEPTO"},
            {title: "DESCRIPCIÓN"},
            {title: "MIEMBRO"},
            {title: "TIPO DE PAGO"},
            {title: "CANTIDAD"},
            {title: "ACCIONES"}
        ],
        "order": [[1, 'desc']],  // Ordena por la columna de la fecha
        "columnDefs": [
            {
                "targets": [1],  // Aplica esta configuración a la columna 1 (la de la fecha)
                "type": "date"   // Indica que esta columna debe ser tratada como fecha
            }
        ]
    });
}

function update_chart(data) {
    const ctx = document.getElementById("graficaIngresos").getContext("2d");

    if (window.miGraficaIngresos) {
        window.miGraficaIngresos.destroy();
    }

    const labels = Object.keys(data);
    const values = Object.values(data);

    window.miGraficaIngresos = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Ingresos por Concepto",
                data: values,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#9C27B0"],
            }]
        },
        options: {
            responsive: false,
            maintainAspectRatio: false
        }
    });
}

function delete_income(id) {
    let incomeToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function() {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/incomes/delete',
            data: {income_concept_id: incomeToDelete}
        }).then(function (response) {
            toastr.success(response.data, { timeOut: 9500 });
            get_data('/incomes/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}

function filterIncomes() {
    var startDate = $('#start_date_filter').val();
    var endDate = $('#end_date_filter').val();

    var url = '/incomes/list?page=0';
    if (startDate) {
        url += '&start_date=' + startDate;
    }
    if (endDate) {
        url += '&end_date=' + endDate;
    }

    get_data(url);
}

function update_total(total) {
    var formattedTotal = total.toLocaleString('es-MX', { style: 'currency', currency: 'MXN', minimumFractionDigits: 2, maximumFractionDigits: 2 });
    $("#total").text("Total de ingresos: " + formattedTotal);
}
