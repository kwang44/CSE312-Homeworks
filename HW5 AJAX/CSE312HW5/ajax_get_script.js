var request = new XMLHttpRequest();
request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200)
    {
        console.log(this.response);
        document.getElementById('ajax_stuff').innerText = this.response;
    }
};
request.open('GET', '/get_time');
request.send();