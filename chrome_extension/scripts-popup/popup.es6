let _DEBUG_MODE = false;
let tab;
_DEBUG_MODE ? _debug(0, "Popup script started") : false;


let communication = new Communication();


chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    tab = tabs[0].id;


});


function display(data) {

    if (data.login) {
        $(".username").text("DBLAB");

        $("#container-sign").addClass("d-none")
        $("#container-nav").removeClass("d-none")
        $("#containver-user").removeClass("d-none")

        let selector = $(".test-set-selector");
        selector.empty();
        let option = $('<option disabled selected value>Choose One...</option>');
        selector.append(option);
        data.answer_set.forEach(data => {
            option = $('<option value='+data._pk+'>'+data._name+'</option>');
            selector.append(option);

        });

        // if(!data.page) {

        //     $("#main_content_show_button").css('color','red');
        //     $("#main_content_show_button").attr("disabled", true);

        // }
        // else {
        //     if (data.page.fields.answer === "") {

        //         $("#main_content_show_button").css('color','red');
        //         $("#main_content_show_button").attr("disabled", true);

        //     }
        // }

    } else {
        $(".container-login").show();

    }

}
function update() {

    communication.sendToBackground(Communication.STATUS(),null, display);


}

window.onload = function() {

    update();

    $("#login-button").on("click", function() {

        let _username = $("input[name='username']").val();
        let _password = $("input[name='password']").val();



        if (_username === "" || _password == "") {
            chrome.notifications.create("alert",{ type: "basic", iconUrl: "icons/icon.png", title: "Login", message: "Password or Username is empty"});
        }
        else {

            let _data = {
                "username": _username,
                "password": _password,
            };
            communication.sendToBackground(Communication.LOGIN(),_data, update);

        }
    });

    $("#logout-button").on("click", function() {

        communication.sendToBackground(Communication.LOGOUT(),{}, update);

    });

    $("#join-button").on("click", function() {

        // let _data = {
        //     "username":$("input[name='username']").val(),
        //     "password":$("input[name='password']").val(),
        // };

        communication.sendToBackground(Communication.JOIN(),{}, update);

    });
    $(".save-page").on("click", function() {

        communication.sendToBackground(Communication.SAVE_PAGE(),null, update);

    });

    $(".test-set-selector").change(event => {

        let val = $(event.target).find(":selected").val();
        let _data = {
            "test_set_id": val
        };

        communication.sendToBackground(Communication.TEST_SET_SITE(),_data, data => {
            $(".test-set-site-toltal-count").text(data.length);
        });

        communication.sendToBackground(Communication.TEST_SET_PAGE(),_data, data => {

            $(".test-set-page-total-count").text(data.length);
        });

    });

    $("#button_left, #button_right").on("click", function(event) {

        let result = parseInt($(".test-set-page-cnt-count").text()) + parseInt(event.target.getAttribute('value'));
        if (0 < result && result < parseInt($(".test-set-page-total-count").text()) + 1) {
            $(".test-set-page-cnt-count").text(result);

            communication.sendToBackground(Communication.LOAD_PAGE(),{
                'test_set_id': $(".test-set-selector > option:selected").last().val(),
                'index': result
            }, update);

        }
    });


    $('#nav-crawl, #nav-curation, #nav-evaluation, #nav-extraction').click(function(){
        $('.navbar-collapse').collapse('hide');
        $('#container-content').removeClass("d-none")

        switch(this.id) {
            case 'nav-crawl':
                $('#container-button').removeClass("d-none");
                $('#container-moving-page').addClass("d-none");
                $('.navbar-brand').text('Crawling');
                break;
            case 'nav-curation':
                $('#container-button').addClass("d-none");
                $('#container-moving-page').removeClass("d-none");

                $('.navbar-brand').text('Curation');
                break;
            case 'nav-extraction':
                $('#container-extraction').removeClass("d-none");
                $('.navbar-brand').text('Extraction');
                break;
            case 'nav-evaluation':
                $('#container-evaluation').removeClass("d-none");
                $('.navbar-brand').text('Evaluation');
                break;

        }
    });
    $('#button-start-crawling').click((event) => {
        let selector = $("#test-set-selector > option:selected");
        $(event.target).text('stop');
        communication.sendToBackground(Communication.TEST_SET_SITE(),{test_set_id: selector.val()}, data => {
            $(".progress-total-count").text(data.length);

            let sites = data;

            communication.sendToBackground(Communication.JOB_CREATION(), null, data => {
                communication.sendToBackground(Communication.CRAWL_SITE(), {
                    job_id: data.job_id,
                    test_set_id: selector.val()
                }, data => {

                    // resolve(data);

                });
            });
        });
    });
};


function _debug(_code, _message) {

    let _date = new Date();

    console.log(_code, _date.getHours()+':'+_date.getMinutes()+':'+_date.getSeconds(), _message);
    // console.log(_code, _date.format('hh:mm:ss'), _message);

}


const POPUPCOMMAND = {

    a:1,
    b:2


};
