/**
 * Created by Bocheng Wang on 2020/7/2.
 */
$(function () {
    $('.captcha').css({
        'cursor': 'pointer'
    });
    $('.captcha').click(function () {
        $('#captcha_status').remove();
        $.getJSON("/UserManagement/captcha/refresh/",
            function (result) {
                $('#id_captcha_1').val("");
                $('.captcha').attr('src', result['image_url']);
                $('#id_captcha_0').val(result['key'])
            });
    });
    $('#id_captcha_1').blur(function () {
        $('#captcha_status').remove();
        var inputValue = $('#id_captcha_1').val();
        if (inputValue == "") {
            return;
        }
        json_data = {
            'response': inputValue,
            'hashkey': $('#id_captcha_0').val()
        };
        $.getJSON('/UserManagement/captcha_ajax_val', json_data, function (data) {
            if (data['status']) {
                $('#id_captcha_1').after('<ui id="captcha_status" style="color:red;"><p>*验证码错误</p></ui>')
            }
        });
    });
})
