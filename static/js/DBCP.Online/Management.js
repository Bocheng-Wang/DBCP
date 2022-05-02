/**
 * Created by Bocheng Wang on 2021.06.10
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


function Config_BootstrapSwitch() {
    var Causality_ctl = $('#CausalityScheduler');
    Causality_ctl.bootstrapSwitch({
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
    Causality_ctl.on('switchChange.bootstrapSwitch', function (event, state) {
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

    var Parcellation_ctl = $('#ParcellationScheduler');
    Parcellation_ctl.bootstrapSwitch({
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
    Parcellation_ctl.on('switchChange.bootstrapSwitch', function (event, state) {
        if (state === true) {
            $.ajax({
                url: "/DBCPScheduler/ServerSchedulerSwitch/CorrelationConnectivity/on",
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
                url: "/DBCPScheduler/ServerSchedulerSwitch/CorrelationConnectivity/off",
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


    var ParcellationDevyg_ctl = $('#ParcellationDebug');
    ParcellationDevyg_ctl.bootstrapSwitch({
        onText: "调试任务",
        offText: "调试取消",
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
    ParcellationDevyg_ctl.on('switchChange.bootstrapSwitch', function (event, state) {
        if (state === true) {
            $.ajax({
                url: "/DBCPScheduler/DebugSwitch/CorrelationConnectivity/on",
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
                url: "/DBCPScheduler/DebugSwitch/CorrelationConnectivity/off",
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

    var CausalityDebug_ctl = $('#CausalityDebug');
    CausalityDebug_ctl.bootstrapSwitch({
        onText: "调试任务",
        offText: "调试取消",
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
    CausalityDebug_ctl.on('switchChange.bootstrapSwitch', function (event, state) {
        if (state === true) {
            $.ajax({
                url: "/DBCPScheduler/DebugSwitch/CausalityConnectivity/on",
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
                url: "/DBCPScheduler/DebugSwitch/CausalityConnectivity/off",
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

$(document).ready(function () {
    Config_BootstrapSwitch();

    $("#TodeleteModalBTN").click(function () {
        modalID = $('#modaltoDelete').val();
        $.ajax({
            url: "/DBCPOnline/Preparation/DeleteVisitByModalIDTmp/7788/" + modalID,
            headers: {
                'X-CSRFToken': csrftoken
            },
            type: 'get',
            async: true,
            dataType: 'text',

            success: function (result) {
                $("#modaltoDelete").val('');
                alert(result);
            }
        });
    });

    $("#ToResetModalBTN").click(function () {
        modalID = $('#modaltoReset').val();
        $.ajax({
            url: "/DBCPOnline/Preprocessing/ResetPreprocessingTask/" + modalID,
            headers: {
                'X-CSRFToken': csrftoken
            },
            type: 'get',
            async: true,
            dataType: 'text',

            success: function (result) {
                $("#modaltoDelete").val('');
                alert(result);
            }
        });
    });

    $("#ToResetCausalityBTN").click(function () {
        modalID = $('#causalitytoReset').val();
        $.ajax({
            url: "/KalmanFilter/ResetPreprocessingTask/" + modalID,
            headers: {
                'X-CSRFToken': csrftoken
            },
            type: 'get',
            async: true,
            dataType: 'text',

            success: function (result) {
                $("#causalitytoReset").val('');
                // alert(result);
            }
        });
    });


})
;