/**
 * Created by Boc Wang on 2020/9/24.
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

function myUpload_operateFormatter(value, row, index) {
    var IsCIFTIFY_Finished = false;
    IsCIFTIFY_Finished = row.IsCIFTIFY_Finished;

    var ciftify_state_CSS = '';
    var visualize_state_CSS = 'disabled';
    var delete_state_CSS = visualize_state_CSS;
    var ciftify_state_attri = '';
    var visualize_state_attri = 'disabled=disabled';
    var delete_state_attri = visualize_state_attri;

    if (IsCIFTIFY_Finished) {
        ciftify_state_CSS = 'disabled';
        visualize_state_CSS = '';
        delete_state_CSS = visualize_state_CSS;
        ciftify_state_attri = 'disabled=disabled';
        visualize_state_attri = '';
        delete_state_attri = visualize_state_attri;
    }
    return [
        '<button ' + ciftify_state_attri + ' class="btn ' + ciftify_state_CSS + '  btn-success ciftifyVisit">CIFTIFY</button>',
        '   ',
        '<button ' + visualize_state_attri + ' class="btn  ' + visualize_state_CSS + ' btn-primary viewVisit">Visualization</button>',
        '   ',
        '<button  class="btn  btn-danger deleteVisit">Delete</button>'
    ].join('');
}

function subject_operateFormatter(value, row, index) {
    return [
        '<button class="btn   btn-info modification">Modification</button>',
    ].join('');
}


// update details for each subject
$(document).on('expand-row.bs.table', '#myUploadedTable', function (e, field, row, old, $el) {
    var $table = $("#detailTable_" + row.subjectID);
    var formData = [];
    formData.push({
        name: "subjectID",
        value: row.subjectID
    });
    $.ajax({
        url: "/DBCPOnline/Preparation/Find_Visit_By_SubjectID",
        headers: {
            'X-CSRFToken': csrftoken
        },
        type: 'post',
        async: true,
        dataType: 'text',
        data: formData,
        // todo subtable
        success: function (result) {
            var obj = $.parseJSON(result);
            $table.bootstrapTable({
                data: obj
            });
        }
    });
});

function dataRowStyle(row, index) {
    var group = row.Diagnosis;
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

function myUpload_detailFormatter(index, row) {
    var html = "<table data-row-style='dataRowStyle' class='table table-striped' id='detailTable_" + row.subjectID + "'>";
    html += "<thead><tr>";
    html += '<th data-align="center" data-field="index" data-formatter="countIndex">Index</th>';
    html += '<th data-align="center" data-field="Phase">Phase</th>';
    html += '<th data-align="center" data-field="Diagnosis">Diagnosis</th>';
    html += '<th data-align="center" data-field="Visit_age">Visit_age</th>';
    html += '<th data-align="center" data-field="visit_time">Visit_time</th>';
    html += '<th data-align="center" data-field="MMSE">MMSE</th>';
    html += '<th data-align="center" data-field="CDR">CDR</th>';
    html += '<th data-align="center"  data-field="SubjectID">SubjectID</th>';
    html += '<th data-align="center"  data-visible="false" data-field="ModalID">ModalID</th>';
    html += '<th data-align="center" data-visible="false" data-field="uploader">uploader</th>';
    html += '<th data-align="center" data-visible="false" data-field="IsCIFTIFY_Finished">IsCIFTIFY_Finished</th>';
    html += '<th data-field="operate" data-align="center" data-events="myUpload_operateEvent" data-formatter="myUpload_operateFormatter">Operation</th>';
    html += '</tr></thead></table>';
    return html;
}


function countIndex(value, row, index) {
    return [
        '<span>',
        index + 1,
        '</span>'
    ].join('');
}

function myUploadTableStyle(row, index) {
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
    // return {
    //     css: {
    //         height: '10px'
    //     }
    // };

}

function aUpload_operateFormatter(value, row, index) {
    return [
        '<button class="btn  btn-success viewVisit">View</button>'
    ].join('');
}


var myUpload_operateEvent = {
    'click .deleteVisit': function (e, value, row, index) {
        var formData = [];
        formData.push({
            name: "ModalID",
            value: row.ModalID
        });
        // console.log(formData)
        if (confirm("确认删除？")) {
            $.ajax({
                url: "/DBCPOnline/Preparation/DeleteVisit",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                type: 'post',
                async: true,
                dataType: 'text',
                data: formData,
                // headers: {
                //     "Cache-Control": "no-cache, no-store, must-revalidate",
                //     "Pragma": "no-cache",
                //     "Expires": "0"
                // },
                // contentType: 'application/x-www-form-urlencoded',
                success: function (data) {
                    // var dassta = JSON.parse(data);
                    // alert(data.msg);
                    $('#myUploadedTable').bootstrapTable('refresh');
                    $('#AllUploadedTable').bootstrapTable('refresh');
                },
                error: function (XMLResponse, XMLHttpRequest, textStatus, errorThrown) {
                    // alert(XMLHttpRequest.status);
                    // alert(XMLHttpRequest.readyState);
                    // alert(textStatus);
                    // alert(XMLResponse)
                    $('#myUploadedTable').bootstrapTable('refresh');
                    $('#AllUploadedTable').bootstrapTable('refresh');
                    // alert(XMLResponse.responseText)
                }

            });
        } else {
            return;
        }
    },
    'click .ciftifyVisit': function (e, value, row, index) {
        window.location.href = 'http://dbcp.cuz.edu.cn/DBCPOnline/Preprocessing';
    },
    'click .viewVisit': function (e, value, row, index) {
        $("html,body").animate({scrollTop: $("#visualize_for_visit").offset().top}, 300);
        BrainBrowser.config.set("color_maps", [
            {
                name: "Gray",
                url: "color_maps/gray_scale.txt",
                cursor_color: "#FF0000"
            },
            {
                name: "Spectral",
                url: "color_maps/spectral-brainview.txt",
                cursor_color: "#FFFFFF"
            },
            {
                name: "Thermal",
                url: "color_maps/thermal.txt",
                cursor_color: "#FFFFFF"
            },
            {
                name: "Blue",
                url: "color_maps/blue.txt",
                cursor_color: "#FFFFFF"
            },
            {
                name: "Green",
                url: "color_maps/green.txt",
                cursor_color: "#FF0000"
            }
        ]);
        BrainBrowser.VolumeViewer.start("visualize_for_visit", function (viewer) {
            $('#visualizationTitle').text('Visualization for Subject: ' + row.SubjectID + '  in Visit: ' + row.Phase);
            viewer.clearVolumes();
            $('#visualizeProgress').removeClass('hidden').addClass('show');
            // Add an event listener.
            // viewer.addEventListener("volumesloaded", function () {
            //     // console.log("Viewer is ready!");
            // });

            // Load the default color map.
            // (Second argument is the cursor color to use).
            viewer.loadDefaultColorMapFromURL('/static/brainbrowser.colormap/thermal.txt', "#FF0000");
            // var color_map_config = BrainBrowser.config.get("color_maps")[0];
            // viewer.loadDefaultColorMapFromURL(color_map_config.url, color_map_config.cursor_color);
            // BrainBrowser.set("color_maps.spectral.name", "Spectral");
            // Set the size of slice display panels.
            viewer.setDefaultPanelSize(300, 300);

            // Start rendering.
            viewer.render();
// can't assign to property "name" on "No color map set for this volume. Cannot render slice
            // Load volumes.
            viewer.loadVolume({
                type: "nifti1",
                nii_url: '/DBCPOnline/Preparation/getNIIfile/' + row.Visit_ID,
                template: {
                    element_id: "volume-ui-template",
                    viewer_insert_class: "volume-viewer-display"
                }
            }, function () {
                $('#visualizeProgress').removeClass('show').addClass('hidden');
                $(".slice-display").css("display", "inline");
                $(".volume-viewer-display").css("text-align", "center");
                // $(".slice-display").css("margin-left", "30px");
                $(".volume-controls").css("width", "auto");

            });

        });

        return false;// 返回false可以避免在原链接后加上#
    }
};

var subject_operateEvent = {
    'click .modification': function (e, value, row, index) {
        alert('modification');
    }
};

function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    var inputname = '';
    var tablename = '';
    inputname = 'SearchMyInput';
    tablename = 'myUploadedTable';

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

// Hide or display loading icon.
var loading_div = $("#loading");

function showLoading() {
    loading_div.show();
}

function hideLoading() {
    loading_div.hide();
}

function defaultCancelOptions(request_number) {
    return function () {
        return request_number !== current_request;
    };
}

$(document).ready(function () {

    // Currently, BrainBrowser.SurfaceViewer and VolumeViewer cannot be put together in a single webpage.

    // Load BrainBrowser.SurfaceViewer
    // BrainBrowser.config.set("worker_dir", "/static/brainbrowser-2.5.5/release/workers");
    // var examples = {
    //     cortical_thickness: function (viewer) {
    //         // viewer.annotations.setMarkerRadius(1);
    //         viewer.loadModelFromURL("/static/brainbrowser-2.5.5/examples/models/realct.obj", {
    //             // viewer.loadModelFromURL("https://brainbrowser.cbrain.mcgill.ca/models/brain-surface.obj", {
    //             // viewer.loadModelFromURL("https://brainbrowser.cbrain.mcgill.ca/models/realct.obj", {
    //             // format: "mniobj",
    //             // parse: {split: true},
    //             complete: function () {
    //                 viewer.loadIntensityDataFromURL("/static/brainbrowser-2.5.5/examples/models/realct.txt", {
    //                     //     //     name: "Cortical Thickness",
    //                     //     //     complete: hideLoading,
    //                     //     //     // cancel: defaultCancelOptions(current_request)
    //                 });
    //             },
    //             // cancel: defaultCancelOptions(current_request)
    //         });
    //     },
    // };
    // BrainBrowser.SurfaceViewer.start('Brain_3D', function (viewer_3D) {
    //
    //     // viewer_3D.addEffect("AnaglyphEffect");
    //
    //     // Start rendering the scene.
    //     viewer_3D.render();
    //     viewer_3D.loadColorMapFromURL('/static/brainbrowser-2.5.5/examples/color-maps/spectral.txt');
    //     examples['cortical_thickness'](viewer_3D);
    //     viewer_3D.autorotate.x = true;
    //     viewer_3D.autorotate.y = true;
    //     viewer_3D.autorotate.z = true;
    // });


    // Load BrainBrowser.VolumeViewer
    BrainBrowser.VolumeViewer.start("visualize_for_visit", function (viewer) {
        viewer.clearVolumes();
        $('#visualizeProgress').removeClass('hidden').addClass('show');
        $('#visualizationTitle').text('Demo shown here. Click the corresponding Visit Operation for a detail visualization');
        // Add an event listener.
        // viewer.addEventListener("volumesloaded", function () {
        //     // console.log("Viewer is ready!");
        // });

        // Load the default color map.
        // (Second argument is the cursor color to use).
        viewer.loadDefaultColorMapFromURL('/static/brainbrowser.colormap/spectral-brainview.txt', "#FF0000");
        // var color_map_config = BrainBrowser.config.get("color_maps")[0];
        // viewer.loadDefaultColorMapFromURL(color_map_config.url, color_map_config.cursor_color);
        // BrainBrowser.set("color_maps.spectral.name", "Spectral");

        // Set the size of slice display panels.
        viewer.setDefaultPanelSize(300, 300);
        // viewer.setPanelSize(512, 512, {
        //     scale_image: true
        // });

        // Start rendering.
        viewer.render();
// can't assign to property "name" on "No color map set for this volume. Cannot render slice
        // Load volumes.
        viewer.loadVolume({
            type: "nifti1",
            nii_url: '/DBCPOnline/Preparation/getNIIfile/example',
            template: {
                element_id: "volume-ui-template",
                viewer_insert_class: "volume-viewer-display"
            }
        }, function () {
            $('#visualizeProgress').removeClass('show').addClass('hidden');
            $(".slice-display").css("display", "inline");
            $(".volume-viewer-display").css("text-align", "center");
            // $(".slice-display").css("margin-left", "30px");
            $(".volume-controls").css("width", "auto");
        });
    });


});





