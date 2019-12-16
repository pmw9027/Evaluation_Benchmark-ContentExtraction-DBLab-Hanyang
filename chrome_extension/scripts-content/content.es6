
let _DEBUG_MODE = true;


window.onload = function() {
    _DEBUG_MODE ? console.log(0, "Started function named 'window.onload'") : false;

    let port = chrome.runtime.connect({name: Communication.CURATION_PORT_CONTENT()});
    port.onMessage.addListener(function(msg) {

        switch(msg.command) {
            case Communication.CURATION_FLASH():


                break;

        }

    });

    // chrome.runtime.sendMessage({
    //
    //     code: Communication.JOB_QUERY(),
    //
    // }, response => {
    //
    //
    //
    //     let job_type = null;
    //     if(response == 'undefined')
    //         job_type = response.job_type;
    //
    //     switch (job_type) {
    //         case null:
    //
    //
    //             break;
    //         case Job.CURATION():
    //             chrome.runtime.sendMessage({
    //                 code: Communication.CURATION_QUERY(),
    //             }, response => {
    //
    //
    //               console.log(response)
    //
    //             });
    //
    //             break;
    //         case Job.EXTRACTION():
    //             chrome.runtime.sendMessage({
    //                 code: Communication.EXTRACTION_QUERY(),
    //             }, response => {
    //
    //                 let _data = {};
    //
    //                 switch(response.extractor) {
    //                     case Communication.SAFARI_READER_MODE():
    //                         let finderJS = new ReaderArticleFinder(document);
    //                         let readable = finderJS.isReaderModeAvailable();
    //                         _data['readable'] = readable;
    //
    //                         if (readable) {
    //
    //                             _data['content'] =finderJS.articleNode().getAttribute('hyu');
    //
    //                         }
    //
    //
    //                         break;
    //                     case Communication.READABILITY():
    //                         let article = new Readability(document).parse();
    //
    //
    //                         if (article == null) {
    //                             _data['readable'] = false
    //
    //                         }
    //                         else {
    //                             console.log(article);
    //
    //                             _data['readable'] = true;
    //                             let dom = createElementFromHTML(article.content);
    //                             _data['content'] = dom;
    //
    //                         }
    //
    //                         break;
    //                     default:
    //
    //                         break;
    //                 }
    //
    //                 chrome.runtime.sendMessage({
    //                     code: Communication.EXTRACTION_RESPONSE(),
    //                     data: _data
    //                 });
    //             });
    //
    //             break;
    //         case Job.EVALUATION():
    //
    //             chrome.runtime.sendMessage({
    //                 code: Communication.EVALUATION_QUERY(),
    //             }, response => {
    //
    //                 let _result = [];
    //
    //                 let answer = $("[hyu='"+523+"'");
    //                 let predict = $("[hyu='"+523+"'");
    //
    //
    //                 console.log(answer, predict);
    //
    //                 let pm = new PerformanceMetric([answer], [predict]);
    //                 chrome.runtime.sendMessage({
    //                     code:Communication.EVALUATION_RESPONSE(),
    //                     data:{
    //                         // predict_id:value['_id'],
    //                         performances: [pm.words(), pm.textLCS(), pm.basedbyarea()]
    //                     }
    //                 });
    //             });
    //
    //             break;
    //     }
    // });

    _DEBUG_MODE ? console.log(0, "Initialed valuables") : false;

};

function createElementFromHTML(htmlString) {
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    // Change this to div.childNodes to support multiple top-level nodes

    let elem = div.firstChild.firstChild;

    if (elem) {
        return elem.getAttribute('hyu');

    }
    else {
        return null;

    }
}

