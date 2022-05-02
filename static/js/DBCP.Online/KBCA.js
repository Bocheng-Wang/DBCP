viewConnectivity_operateEvent

/**
 * Created by Bocheng Wang on 2020/9/29.
 */

// Important ! For the csrf in ajax header, BC, wang
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function countIndex(value, row, index) {
    return [
        '<span>',
        index + 1,
        '</span>'
    ].join('');
}


function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    var inputname = '';
    var tablename = '';
    inputname = 'SearchAllInput';
    tablename = 'PreprocessingTable';

    input = document.getElementById(inputname);
    filter = input.value.toUpperCase();
    table = document.getElementById(tablename);
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        var j, tds;
        tds = tr[i].getElementsByTagName("td");
        for (j = 0; j < tds.length; j++) {
            td = tds[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                var txtValueNew = txtValue.replace(/^\s*|\s*$/g, "");
                var filterNew = filter.replace(/^\s*|\s*$/g, "");
                if (txtValueNew.toUpperCase().indexOf(filterNew) > -1) {
                    tr[i].style.display = "";
                    break;
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}

function dataRowStyle(row, index) {
    var group = row.group;
    var classes = [
        'success',
        'warning',
        'danger',
        'info'
    ];
    if (group === 'HC') {
        return {
            classes: 'success'
        };
    } else if (group === 'EMCI') {
        return {
            classes: 'info'
        };
    } else if (group === 'LMCI') {
        return {
            classes: 'warning'
        };
    } else if (group === 'AD') {
        return {
            classes: 'danger'
        };
    }


}

function operation_Formatter(value, row, index) {
    var isStaticStart = row.static_task_start;
    var isStaticFinished = row.static_task_Finish;
    var StaticProgressValue = row.static_progress_value;

    var isDynamicStart = row.dynamic_task_start;
    var isDynamicFinished = row.dynamic_task_Finish;
    var DynamicProgressValue = row.dynamic_progress_value;

    return [
        '<button class="btn btn-danger cancelPreprocessing">Cancel</button>'
    ].join('');
}


function progress_StaticFormatter(value, row, index) {
    var group = row.group;
    var isStart = row.task_start;
    var isFinished = row.task_Finish;
    var ProgressValue = row.progress_value;

    var progress_value = '100%';
    var progress_content = 'Waiting for dispatch';

    if (isStart) {
        // todo for test
        if (!isFinished) {
            // if ($('#UserOnline').text().indexOf(row.uploader) != -1) {
            progress_value = ProgressValue + '%';
            progress_content = progress_value;
            // }
        } else if (isFinished && row.Task_Status !== -1) {
            // if ($('#UserOnline').text().indexOf(row.uploader) != -1) {
            progress_value = '100%';
            progress_content = 'Finished';
            // }
        } else if (isFinished && row.Task_Status === -1) {
            progress_value = '100%';
            progress_content = 'Failed';
        }
    }


    var classes = [
        'progress-bar-success',
        'progress-bar-warning',
        'progress-bar-danger',
        'progress-bar-info'
    ];

    var classIs = '';
    if (progress_content === 'Finished') {
        classIs = 'progress-bar-success';
    } else if (progress_content === 'Waiting for dispatch') {
        classIs = 'progress-bar-info';
    } else {
        classIs = 'progress-bar-warning';
    }

    return [
        '<div class="progress">',
        '<div class="progress-bar ',
        classIs,
        ' progress-bar-striped active" role="progressbar"  aria-valuemin="0" aria-valuemax="100" style="min-width: 4em;width: ',
        progress_value,
        '">',
        '<span >',
        progress_content,
        '</span>',
        '</div>'
    ].join('');
}

function GetTimeSpan(milliSecond) {
    //计算出相差天数
    var days = Math.floor(milliSecond / (24 * 3600 * 1000));

    //计算出小时数

    var leave1 = milliSecond % (24 * 3600 * 1000);    //计算天数后剩余的毫秒数
    var hours = Math.floor(leave1 / (3600 * 1000));
    //计算相差分钟数
    var leave2 = leave1 % (3600 * 1000);        //计算小时数后剩余的毫秒数
    var minutes = Math.floor(leave2 / (60 * 1000));
    //计算相差秒数
    var leave3 = leave2 % (60 * 1000);      //计算分钟数后剩余的毫秒数
    var seconds = Math.round(leave3 / 1000);

    return [days, hours, minutes, seconds];
}

function progress_DynamicFormatter(value, row, index) {
    var group = row.group;
    var isStart = row.dynamic_task_start;
    var isFinished = row.dynamic_task_Finish;
    var ProgressValue = row.dynamic_progress_value;

    var progress_value = '100%';
    var progress_content = 'Waiting for dispatch';

    if (isStart) {
        // todo for test
        if (!isFinished) {
            // if ($('#UserOnline').text().indexOf(row.uploader) != -1) {
            progress_value = ProgressValue + '%';
            progress_content = progress_value;
            // }
        } else if (isFinished) {
            // if ($('#UserOnline').text().indexOf(row.uploader) != -1) {
            progress_value = '100%';
            progress_content = 'Finished';
            // }
        }
    }


    var classes = [
        'progress-bar-success',
        'progress-bar-warning',
        'progress-bar-danger',
        'progress-bar-info'
    ];

    var classIs = '';
    if (progress_content === 'Finished') {
        classIs = 'progress-bar-success';
    } else if (progress_content === 'Waiting for dispatch') {
        classIs = 'progress-bar-info';
    } else {
        classIs = 'progress-bar-warning';
    }

    return [
        '<div class="progress">',
        '<div class="progress-bar ',
        classIs,
        ' progress-bar-striped active" role="progressbar"  aria-valuemin="0" aria-valuemax="100" style="min-width: 2em; width: ',
        progress_value,
        '">',
        '<span >',
        progress_content,
        '</span>',
        '</div>'
    ].join('');
}

function viewConnectivityFormatter(value, row, index) {
    var group = row.group;
    var isStart = row.task_start;
    var isFinished = row.task_Finish;
    var ProgressValue = row.progress_value;


    var state_CSS = 'disabled hidden';
    var state_attri = 'disabled=disabled';
    if (isFinished && row.Task_Status !== -1) {
        state_CSS = '';
        state_attri = '';
    }

    return [
        '<a  role="button" ' + state_attri + ' class="label btn  btn-info ' + state_CSS + ' DownloadConnectivity">Download</a>',
    ].join('');
}

function resetProcessFormatter(value, row, index) {
    var group = row.group;
    var isStart = row.task_start;
    var isFinished = row.task_Finish;
    var ProgressValue = row.progress_value;


    var state_CSS = 'disabled hidden';
    var state_attri = 'disabled=disabled';
    if (row.task_start && !row.task_Finish) {
        state_CSS = '';
        state_attri = '';
    } else if (isFinished && row.Task_Status === -1) {
        state_CSS = '';
        state_attri = '';
    }

    return [
        '<a  role="button" ' + state_attri + ' class="label ResetProcess btn  btn-danger ' + state_CSS + ' ">Reset</a>',
    ].join('');
}

function myUpload_detailFormatter(index, row) {
    var html = []
    var endtime = ''
    var starttime = ''
    starttime = row['startTime']
    endtime = row['endTime'];
    server = row['Server']
    if (!server) {
        server = '尚未分配'
    }
    if (!endtime) {
        endtime = '尚未完成';
    }
    if (!starttime) {
        starttime = '尚未开始';
    }
    if (row['Task_Status'] == '-1') {
        endtime = '任务出错';
    }

    html.push('<p><b>ModalID：</b>' + row['ModalID']);
    html.push('<p><b>开始时间：</b>' + starttime);
    html.push('<p><b>完成时间：</b>' + endtime);
    html.push('<p><b>分配服务器：</b>' + server);
    html.push('<p><b>任务ID：</b>' + row['UUID']);

    return html.join('')
}

function queryParams(params) {
    params.sortName = 'Task_StartTime';
    return params;
}

function CheckProcessFormatter(value, row, index) {
    var formData = [];
    formData.push({
        name: "ModalID",
        value: row.ModalID
    }, {
        name: "type",
        value: "Parcellation"
    });


    var status = value;
    var isStart = row.task_start;
    var isFinished = row.task_Finish;
    // var ProgressValue = row.dynamic_progress_value;


    var state_CSS = 'disabled hidden';
    var state_attri = 'disabled=disabled';
    var task_status = 'Running'
    if (row.task_start && !row.task_Finish) {
        if (status === 200) {
            state_CSS = 'label label-success';
            task_status = 'Running';
        } else {
            state_CSS = 'label label-warning';
            task_status = 'Failed'
        }
        state_attri = '';
    }
    if (row.task_Finish && row.Task_Status === -1) {
        state_CSS = 'label label-warning';
        task_status = 'Failed'
    }


    return [
        '<span ' + state_attri + ' class="' + state_CSS + ' ">' + task_status + '</span>',
    ].join('');
}

function serverFormatter(value, index, row) {
    if (value) {
        return [
            '<a  > ' + value + ' </a>',
        ].join('');
    }

}

var viewConnectivity_operateEvent = {

    'click .DownloadConnectivity': function (e, value, row, index) {
        var ModalID = row.ModalID;
        window.location.href = 'http://dbcp.cuz.edu.cn/KalmanFilter/getConnectivityFiles/' + ModalID

    },

};


var resetProcess_operateEvent = {
    'click .ResetProcess': function (e, value, row, index) {
        var ModalID = row.ModalID;
        if (confirm('Sure to reset this?') === true) {
            $('#WaitModal').modal({backdrop: 'static'})
            $('#WaitModal').modal('show')

            $.ajax({
                url: "/KalmanFilter/ResetPreprocessingTask/" + ModalID,
                headers: {
                    'X-CSRFToken': csrftoken
                },
                type: 'post',
                async: true,
                dataType: 'text',

                success: function (result) {
                    // $('#PreprocessingTable').bootstrapTable('refresh');
                    row.task_start = false;
                    row.task_Finish = false;
                    $('#PreprocessingTable').bootstrapTable('updateRow', {index: index, row: row, replace: true});
                    $('#WaitModal').modal('hide');
                }
            });
        }
    }
    ,
};

var CheckProcess_operateEvent = {
    'click .CheckProcess': function (e, value, row, index) {
        var ModalID = row.ModalID;

        $.ajax({
            url: "/DBCPOnline/Preprocessing/CheckParcellationPreprocessingTask/" + ModalID,
            headers: {
                'X-CSRFToken': csrftoken
            },
            type: 'post',
            async: true,
            dataType: 'text',

            success: function (result) {
                alert(result);
            }
        });

    }
    ,
};

setInterval(function () {
        $('#PreprocessingTable').bootstrapTable('refresh');
    }, 300000
)
;

function Config_BootstrapSwitch() {
    var control = $('[name="status"]');
    control.bootstrapSwitch({
        onText: "调度任务",
        offText: "调度暂停",
        onColor: "success",
        offColor: "danger",
        size: "small",
        onSwitchChange: function (event, state) {
            if (state === true) {
                $(this).val("1");
            } else {
                $(this).val("2");
            }
        }
    })
    control.on('switchChange.bootstrapSwitch', function (event, state) {
        if (state === true) {
            $.ajax({
                url: "/DBCPScheduler/ServerSchedulerSwitch/CausalityConnectivity/on",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                type: 'get',
                async: true,
                dataType: 'text',

                success: function (result) {
                    // alert(result);
                }
            });
        } else {
            $.ajax({
                url: "/DBCPScheduler/ServerSchedulerSwitch/CausalityConnectivity/off",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                type: 'get',
                async: true,
                dataType: 'text',

                success: function (result) {
                    // alert(result);
                }
            });
        }
    });

}

var expanded_row = -1;
$(document).ready(function () {
    // Config_BootstrapSwitch();
    var table = $('#PreprocessingTable');
    table.on('click-row.bs.table', function (e, row, $element, field) {
        if ($element[0].sectionRowIndex === expanded_row) {
            table.bootstrapTable('collapseAllRows');
            expanded_row = -1;
        } else {
            table.bootstrapTable('collapseAllRows');
            table.bootstrapTable('expandRow', $element[0].sectionRowIndex);
            expanded_row = $element[0].sectionRowIndex;
        }
    })
    effect = 2;


})
;