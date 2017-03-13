var Employee = function () {
    var bindEvents = function () {
        $('#btnNew').click(Employee.create);
    };
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
                        return '<a href="javascript:Employee.edit(\'' + row.id + '\');" class="btn btn-info" ><i class="fa fa-edit"></i></a> <a href="javascript:Employee.remove(\'' + row.id + '\');" class="btn btn-danger"><i class="fa fa-remove"></i></a>';
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
            bindEvents();
        },
        create: function () {
            alert('Criar Empregado');
        },
        edit: function (id){
            alert(id);
        },
        remove: function (id) {
            alert(id);
        }
    };
}();