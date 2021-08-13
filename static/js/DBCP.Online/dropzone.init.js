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

$("#template").ready(function () {
// Get the template HTML and remove it from the doumenthe template HTML and remove it from the doument
        document.querySelector(".cancel").onclick = function () {
            myDropzone.removeAllFiles(true);
        };

        // document.querySelector(".start").onclick = function () {
        //     myDropzone.enqueueFiles(myDropzone.getFilesWithStatus(Dropzone.ADDED));
        // };

        var previewNode = document.querySelector("#template");
        previewNode.id = "";
        var previewTemplate = previewNode.parentNode.innerHTML;
        previewNode.parentNode.removeChild(previewNode);


        var csrftoken = getCookie('csrftoken');

        var myDropzone = new Dropzone(document.body, { // Make the whole body a dropzone
                url: "/DBCPOnline/Preparation/FileUpload", // Set the url
                thumbnailWidth: 80,
                thumbnailHeight: 80,
                parallelUploads: 5,
                maxFilesize: null,
                acceptedFiles: ".zip",
                timeout: 120000,
                previewTemplate: previewTemplate,
                autoQueue: false, // Make sure the files aren't queued until manually added
                previewsContainer: "#previews", // Define the container to display the previews
                clickable: ".fileinput-button", // Define the element that should be used as click trigger to select files.
                headers: {
                    'X-CSRFToken': csrftoken
                }
            })
        ;

        myDropzone.on("sending", function (file, xhr, data) {
            var selector = file.previewElement.querySelector('.GroupSelector');
            var group = selector.value;
            data.append("group", group);

            selector = file.previewElement.querySelector('.AgeInput');
            age = selector.value;
            data.append('age', age);

            selector = file.previewElement.querySelector('.VisitSelector');
            visit = selector.value;
            data.append('visit', visit);
        });

        myDropzone.on("addedfile", function (file) {
            // Hookup the start button
            var fileList = myDropzone.files;
            var newfileName = fileList[fileList.length - 1].name;
            for (var i = 0; i < fileList.length - 1; i++) {
                if (fileList[i].name === newfileName) {
                    myDropzone.removeFile(file);
                    return;
                }
            }

            file.previewElement.querySelector(".delete").onclick = function () {

            };

            file.previewElement.querySelector(".start").onclick = function () {
                var UserOnline = $('#UserOnline');
                if (UserOnline.length === 0) {
                    file.previewElement.querySelector('.uploaderror').textContent = 'Please Login in first';
                    file.previewElement.querySelector('.uploaderror').hidden = false;
                    return;
                }
                var fileName = file.previewElement.querySelector('.name').textContent;
                var pattern = /^ADNI\d_\d{3}_S_\d{4}.zip/i;
                if (!pattern.test(fileName)) {
                    file.previewElement.querySelector('.uploaderror').textContent = 'Check the file name, Example: ADNI2_010_S_0001.zip';
                    file.previewElement.querySelector('.uploaderror').hidden = false;
                    return;
                }
                var VisitInfo = file.previewElement.querySelector('.VisitSelector').value;
                if (VisitInfo === 'null') {
                    file.previewElement.querySelector('.uploaderror').textContent = 'Select the Visit';
                    file.previewElement.querySelector('.uploaderror').hidden = false;
                    return;
                }
                var AgeInfo = file.previewElement.querySelector('.AgeInput').value;
                if (AgeInfo == '') {
                    file.previewElement.querySelector('.uploaderror').textContent = 'Fill the Age';
                    file.previewElement.querySelector('.uploaderror').hidden = false;
                    return;
                }
                if (Number(AgeInfo) <= 0 || Number(AgeInfo) > 150) {
                    file.previewElement.querySelector('.uploaderror').textContent = 'Check the Age';
                    file.previewElement.querySelector('.uploaderror').hidden = false;
                    return;
                }
                file.previewElement.querySelector('.uploaderror').textContent = '';
                file.previewElement.querySelector('.uploaderror').hidden = true;
                myDropzone.enqueueFile(file);
            };
        });

        myDropzone.on("success", function (file, data, fn) {
            result = data
            if (result === '200') {
                file.previewElement.querySelector('.uploadStatus').textContent = 'Upload Succeeded';
                file.previewElement.querySelector('.uploadStatus').hidden = false;
            } else if (result === '500') {
                file.previewElement.querySelector('.uploaderror').textContent = 'Zip file checking failed';
                file.previewElement.querySelector('.uploaderror').hidden = false;
            } else {
                file.previewElement.querySelector('.uploaderror').textContent = 'Error in upload';
                file.previewElement.querySelector('.uploaderror').hidden = false;
            }

            $('#myUploadedTable').bootstrapTable('refresh');
            $('#AllUploadedTable').bootstrapTable('refresh');


        });

// // Update the total progress bar
//         myDropzone.on("totaluploadprogress", function (progress) {
//             document.querySelector("#total-progress .progress-bar").style.width = progress + "%";
//         });
//
//         myDropzone.on("sending", function (file) {
//             // Show the total progress bar when upload starts
//             document.querySelector("#total-progress").style.opacity = "1";
//             // And disable the start button
//             file.previewElement.querySelector(".start").setAttribute("disabled", "disabled");
//         });

// Hide the total progress bar when nothing's uploading anymore
//         myDropzone.on("queuecomplete", function (progress) {
//             document.querySelector("#total-progress").style.opacity = "0";
//         });


    }
);

