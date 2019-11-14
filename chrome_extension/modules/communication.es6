class Communication {


    constructor() {  }

    static ISLOGIN()            {   return 100; }
    static LOGIN()              {   return 101; }
    static JOIN()               {   return 103; }
    static LOGOUT()             {   return 102; }
    static MENU_CONTENT_CHECK() {   return 5;   }
    static MAIN_CONTENT_SHOW()  {   return 15;  }
    static MAIN_CONTENT_CHECK() {   return 6;   }
    static NEXTPAGE()           {   return 4;   }
    static PREVIOUSPAGE()       {   return 3;   }
    static GETLIST()            {   return 2;   }
    static MENU_INITIAL()       {   return 1;   }
    static SENDING()            {   return 0;   }
    static STATUS()             {   return 10;  }
    static SAVE_PAGE()          {   return 200; }

    static CONTENT_CHECK_MODE()  {   return 300; }
    static CONTENT_ANSWER()  {   return 301; }

    static ANSWER_CHECK()       {   return 401; }

    static REQUEST_RESOURCE()       {   return 501; }

    static JOB_CREATION()          {   return 801; }

    static CRAWL_SITE()          {   return 601; }

    static TEST_SET_SITE() {return 701;}


    sendToBackground(_code,_data, callback) {
        _DEBUG_MODE ? _debug(0, "Message is sent to BackgroundScript (code:"+_code+")") : false;
        chrome.runtime.sendMessage({code:_code, data:_data}, function(response) {
            _DEBUG_MODE ? _debug(0, "Message is received from BackgroundScript\n"+JSON.stringify(response)) : false;
            if(response !== undefined) {
                callback(response.data);
            }
            else {
                _DEBUG_MODE ? _debug(0, "Error") : false;
            }
        });
    }

    sendToContent (_code,_data, callback) {

        chrome.tabs.sendMessage(tab, { code: _code, data:_data }, function(response) {
            // 응답 처리


            switch (response.code) {

                case Communication.code.MAIN_CONTENT_CHECK:




                    break;
                default:



                    break;

            }
        });
    }

}

function _debug(_code, _message) {

    let _date = new Date();

    console.log(_code, _date.getHours()+':'+_date.getMinutes()+':'+_date.getSeconds(), _message);
    // console.log(_code, _date.format('hh:mm:ss'), _message);

}
