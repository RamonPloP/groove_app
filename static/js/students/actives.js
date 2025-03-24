$(function() {
  let currentDate = new Date();
  let firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
  let today = currentDate.toISOString().split('T')[0];

  $('#startDateFilter').val(firstDayOfMonth.toISOString().split('T')[0]);
  $('#endDateFilter').val(today);

  get_data('/students/active-members/get', firstDayOfMonth.toISOString().split('T')[0], today);

  $('#filterButton').click(function() {

    var startDate = $('#startDateFilter').val();
    var endDate = $('#endDateFilter').val();

    if (!startDate || !endDate) {
      alert('Por favor, selecciona ambas fechas.');
      return;
    }

    if (startDate > endDate) {
      alert('La fecha de inicio no puede ser posterior a la fecha de fin.');
      return;
    }

    get_data('/students/active-members/get', startDate, endDate);
  });
});

function get_data(url, startDate = '', endDate = '') {
  $.getJSON(url, { start_date: startDate, end_date: endDate }, function(data) {
    update_table(data[0]);
    update_graph(data[0]);
    update_totals(data);
  });
}

function update_totals(data){
  $('#inactives').html('Bajas: '+data[1]);
  $('#total_members').html(data[2]);
  $('#amount_total').html('Total: '+data[3].toLocaleString("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
}

function update_table(data) {
  let elements = []
  $.each(data, function(i, element) {
    let item = []
    item.push(element.name);
    item.push(element.actives);
    item.push('$ ' + element.total.toLocaleString("es-MX", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
    elements.push(item);
  });

  // Limpiar y recrear la tabla
  $('#datatable_list').DataTable().clear();
  $('#datatable_list').DataTable().destroy();
  $('#datatable_list').DataTable({
    responsive: true,
    language: {
      url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
    },
    data: elements,
    columns: [
      {title: "Membresía"},
      {title: "Activos"},
      {title: "Total"},
    ],
    paging: false,
    searching: false,
    info: false,
    lengthChange: false,
  });
}

function update_graph(memberships) {
  if (window.miGrafica) {
    window.miGrafica.destroy();
  }

  let data = {};

  // Crear los datos para la gráfica
  for (const membership of memberships) {
    data[membership.name] = membership.total;
  }

  const labels = Object.keys(data);
  const values = Object.values(data);

  const ctx = document.getElementById("grafica").getContext("2d");

  // Crear o actualizar la gráfica
  window.miGrafica = new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [{
        label: "Total por membresía",
        data: values,
        backgroundColor: ["#e56300", "#000000", "#FFCE56", "#ffda02", "#9C27B0"],
      }]
    },
    options: {
      responsive: false,
      maintainAspectRatio: false
    }
  });
}
