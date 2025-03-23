    $(function () {
       get_members()
    });

    function get_members() {
        $.getJSON('/expirations/list/expired', function (data) {
                update_expired_table(data)
            }
        );
        $.getJSON('/expirations/list/expire_today', function (data) {
                update_expire_today_table(data)
            }
        );
        $.getJSON('/expirations/list/expire_future', function (data) {
                update_expire_future_table(data)
            }
        );
    }

    function update_expired_table(data) {
        let expirations = []
        $.each(data, function (i, element) {
            let expire = []
            expire.push(element.name)
            expire.push(element.expire_date)
            expire.push('$ '+element.amount)

            expirations.push(expire)
        })
        $('#table_expired').DataTable().clear();
        $('#table_expired').DataTable().destroy();
        $('#table_expired').DataTable({
            dom: 'lBfrtip',
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
            },
            data: expirations,
            responsive: true,
            columns: [
                {title: "NOMBRE"},
                {title: "FECHA DE EXPIRACIÓN"},
                {title: "MONTO"},
            ],
            paging: false,
            searching: false,
            info: false,
            lengthChange: false,

        });
    }

    function update_expire_today_table(data) {
        let expirations = []
        $.each(data, function (i, element) {
            let expire = []
            expire.push(element.name)
            expire.push(element.expire_date)
            expire.push('$ '+element.amount)

            expirations.push(expire)
        })
        $('#table_expire_today').DataTable().clear();
        $('#table_expire_today').DataTable().destroy();
        $('#table_expire_today').DataTable({
            dom: 'lBfrtip',
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
            },
            data: expirations,
            responsive: true,
            columns: [
                {title: "NOMBRE"},
                {title: "FECHA DE EXPIRACIÓN"},
                {title: "MONTO"},
            ],
            paging: false,
            searching: false,
            info: false,
            lengthChange: false,

        });
    }

    function update_expire_future_table(data) {
        let expirations = []
        $.each(data, function (i, element) {
            let expire = []
            expire.push(element.name)
            expire.push(element.expire_date)
            expire.push('$ '+element.amount)

            expirations.push(expire)
        })
        $('#table_expire_future').DataTable().clear();
        $('#table_expire_future').DataTable().destroy();
        $('#table_expire_future').DataTable({
            dom: 'lBfrtip',
            language: {
                url: 'https://cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
            },
            data: expirations,
            responsive: true,
            columns: [
                {title: "NOMBRE"},
                {title: "FECHA DE EXPIRACIÓN"},
                {title: "MONTO"},
            ],
            paging: false,
            searching: false,
            info: false,
            lengthChange: false,

        });
    }
