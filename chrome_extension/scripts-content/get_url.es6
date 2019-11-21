chrome.runtime.sendMessage({
    code: Communication.CRAWL_REQUEST(),
}, function(response) {


    let links = document.links;
    let arr = [];


    for(let i=0; i < links.length; i++) {
        arr.push(links[i].href);
    }

    let path_names = [];
    let url;
    let ran_num;


    while(path_names.length < response.breadth && arr.length) {

        ran_num = getRandomInt(arr.length);
        try {
            url = new URL(arr[ran_num]);

            if (url.host == window.location.host && url.pathname != window.location.pathname) {
                path_names.push(
                    {
                        protocol: url.protocol,
                        pathname: url.pathname

                    }
                );
            }
            arr.splice(ran_num, 1);

        }
        catch (error) {
            arr.splice(ran_num, 1);
        }
    }


    let _data = {
        depth:response.depth,
        page: {
            protocol: window.location.protocol,
            host: window.location.host,
            pathname: window.location.pathname

        },
        urls: {
            host: window.location.host,
            pathname: path_names
        }
    };

    chrome.runtime.sendMessage({
        code: Communication.CRAWL_RESPONSE_URLS(),
        data: _data
    }, function(response) {

    });
});


function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}