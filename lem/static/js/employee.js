var Employee = function () {
    var handleRecords = function () {
        $('#datatable_employees').DataTable( {
            "sAjaxDataProp":"employees",
            "processing": true,
            "serverSide": true,
            "searching": false,
            "paginate": false,
            "ajax": Employee.options.fetchUrl,
            "columns": [
                { "data": "id" },
                { "data": "name" },
                { "data": "email" },
                { "data": "department" },
                {
                    data: function (row) {
                        return '<a href="' + Employee.options.editUrl + '/'  + row.id + '" class="btn btn-info" ><i class="fa fa-edit"></i></a> <a href="javascript:Employee.remove(\'' + row.id + '\');" class="btn btn-danger"><i class="fa fa-remove"></i></a>';
                    }
                }
            ]
        } );
    };
    return {
        dataTable: null,
        options: {},
        init: function (options) {
            this.options = options;
            handleRecords();
        },
        remove: function (id) {
            $.ajax({
                type : "POST",
                url: Employee.options.removeUrl,
                data: JSON.stringify({employee_id: id.toString()}),
                contentType: 'application/json;charset=UTF-8',
                }).done(function () {
                    window.location.reload();
            }).fail(function () {
                alert('Erro ao chamar a API');
            });
        }
    };
}();