     $(function() {
      get_data('/expenses/list?page=0')
    });
     function show_info(id, button) {
        $(button).attr('disabled', true);
        axios({
            method: 'get',
            url: '/expenses/' + id
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
                url: '/expenses/crud',
                data: data_form
            }).then(function (response) {
                toastr.success(response.data, { timeOut: 9500 })
                get_data('/expenses/list?page=0')
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
            url: '/expenses/add'
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
        update_table(data.expenses);
        update_total(data.total_expenses);
        update_graph(data.expenses_by_concept);  // Actualiza la gráfica con los datos filtrados o nuevos
    });
}

function update_total(total) {
    var formattedTotal = total.toLocaleString('es-MX', { style: 'currency', currency: 'MXN', minimumFractionDigits: 2, maximumFractionDigits: 2 });
    $("#total").text("Total de egresos: " + formattedTotal);
}


/*Funtion to generate de datatable and fill whit de json data */

function update_table(data) {
    let expenses = []
    $.each(data, function (i, element) {
        let expense = []
        expense.push(element.id)
        expense.push(element.date)
        expense.push(element.expense_concept)
        if(element.description == null){
            expense.push('-')
        }else{
            expense.push(element.description)
        }
        expense.push(element.payment_type)
        expense.push('$ '+element.amount)
        expense.push('<button type="button" class="btn btn-outline-danger" onclick="delete_expense('+element.id +', this)">'+
                            '<i class="fas fa-trash"></i>'+
                        '</button>')
        expenses.push(expense)
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
        data: expenses,
        columns: [
            {title: "ID"},
            {title: "FECHA"},
            {title: "CONCEPTO"},
            {title: "DESCRIPCION"},
            {title: "TIPO DE PAGO"},
            {title: "CANTIDAD"},
            {title: "ACCIONES"}
        ],
        "order": [[1, 'desc']]
    });
}

function delete_expense(id) {
    let expenseToDelete = id;

    $('#confirmationModal').modal('show');

    $('#confirmDeleteButton').off('click').on('click', function () {
        axios({
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            url: '/expenses/delete',
            data: {expense_concept_id: expenseToDelete}
        }).then(function (response) {
            toastr.success(response.data, {timeOut: 9500});
            get_data('/expenses/list?page=0');
            $('#confirmationModal').modal('hide'); // Cierra el modal
        }).catch(function (error) {
            toastr.error(error.response.data);
            console.log(error.response);
        });
    });
}

function update_graph(expenses_by_concept) {
    // Si ya existe la gráfica, destrúyela
    if (window.miGrafica) {
        window.miGrafica.destroy();
    }

    // Tomar las nuevas etiquetas y valores
    const labels = Object.keys(expenses_by_concept);
    const values = Object.values(expenses_by_concept);

    // Crear la gráfica con los nuevos datos
    const ctx = document.getElementById("graficaEgresos").getContext("2d");

    window.miGrafica = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Egresos por Concepto",
                data: values,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4CAF50", "#9C27B0"],
            }]
        },
        options: {
            responsive: false,  // ⚠️ Desactivar la responsividad
            maintainAspectRatio: false  // ⚠️ Permitir tamaños personalizados
        }
    });
}

function filterExpenses() {
    var startDate = $('#start_date_filter').val();
    var endDate = $('#end_date_filter').val();

    // Crear la URL con los parámetros de fecha
    var url = '/expenses/list?page=0'; // Puedes agregar paginación si la necesitas
    if (startDate) {
        url += '&start_date=' + startDate;
    }
    if (endDate) {
        url += '&end_date=' + endDate;
    }

    // Obtener los datos filtrados
    get_data(url);
}
function cargarDatos() {
    fetch("/expenses/list")
    .then(response => response.json())
    .then(data => {
        document.getElementById("total").innerText = "Total egresos: $" + data.total_expenses.toFixed(2);

        // Actualizar la gráfica con los datos completos al cargarla por primera vez
        update_graph(data.expenses_by_concept);
    })
    .catch(error => console.error("Error al cargar datos:", error));
}


        cargarDatos();
