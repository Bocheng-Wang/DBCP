$(document).ready(function () {


     $('body').css('background-color', 'black');

    // Currently, BrainBrowser.SurfaceViewer and VolumeViewer cannot be put together in a single webpage.

    // Load BrainBrowser.SurfaceViewer
    BrainBrowser.config.set("worker_dir", "/static/brainbrowser-2.5.5/release/workers");
    var examples = {
        cortical_thickness: function (viewer) {
            // viewer.annotations.setMarkerRadius(1);
            viewer.loadModelFromURL("/static/brainbrowser-2.5.5/examples/models/realct.obj", {
                // viewer.loadModelFromURL("https://brainbrowser.cbrain.mcgill.ca/models/brain-surface.obj", {
                // viewer.loadModelFromURL("https://brainbrowser.cbrain.mcgill.ca/models/realct.obj", {
                // format: "mniobj",
                // parse: {split: true},
                complete: function () {
                     viewer.loadIntensityDataFromURL("/static/brainbrowser-2.5.5/examples/models/realct.txt", {
                        //     //     name: "Cortical Thickness",
                        //     //     complete: hideLoading,
                        //     //     // cancel: defaultCancelOptions(current_request)
                    });
                },
                // cancel: defaultCancelOptions(current_request)
            });
        },
    };
    BrainBrowser.SurfaceViewer.start('Brain_3D', function (viewer_3D) {

        // viewer_3D.addEffect("AnaglyphEffect");

        // Start rendering the scene.
        viewer_3D.render();
        viewer_3D.loadColorMapFromURL('/static/brainbrowser-2.5.5/examples/color-maps/spectral.txt');
        examples['cortical_thickness'](viewer_3D);
        // viewer_3D.autorotate.x = true;
        // viewer_3D.autorotate.y = true;
        viewer_3D.autorotate.z = true;
    });


//     // Load BrainBrowser.VolumeViewer
//     BrainBrowser.VolumeViewer.start("visualize_for_visit", function (viewer) {
//         viewer.clearVolumes();
//         $('#visualizeProgress').removeClass('hidden').addClass('show');
//         $('#visualizationTitle').text('Demo shown here. Click the corresponding Visit Operation for a detail visualization');
//         // Add an event listener.
//         // viewer.addEventListener("volumesloaded", function () {
//         //     // console.log("Viewer is ready!");
//         // });
//
//         // Load the default color map.
//         // (Second argument is the cursor color to use).
//         viewer.loadDefaultColorMapFromURL('/static/brainbrowser.colormap/spectral-brainview.txt', "#FF0000");
//         // var color_map_config = BrainBrowser.config.get("color_maps")[0];
//         // viewer.loadDefaultColorMapFromURL(color_map_config.url, color_map_config.cursor_color);
//         // BrainBrowser.set("color_maps.spectral.name", "Spectral");
//         // Set the size of slice display panels.
//         viewer.setPanelSize(256, 256);
//
//         // Start rendering.
//         viewer.render();
// // can't assign to property "name" on "No color map set for this volume. Cannot render slice
//         // Load volumes.
//         viewer.loadVolume({
//             type: "nifti1",
//             nii_url: '/DBCPOnline/Preparation/getNIIfile/82',
//             template: {
//                 element_id: "volume-ui-template",
//                 viewer_insert_class: "volume-viewer-display"
//             }
//         }, function () {
//             $('#visualizeProgress').removeClass('show').addClass('hidden');
//             $(".slice-display").css("display", "inline");
//             $(".volume-viewer-display").css("text-align", "center");
//             $(".slice-display").css("margin-left", "30px");
//             $(".volume-controls").css("width", "auto");
//         });
//     });


});