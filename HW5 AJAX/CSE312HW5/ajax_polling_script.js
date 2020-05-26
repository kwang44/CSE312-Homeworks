setInterval(recieveMessage, 500);

function sendMessage() {
    const chatBox = document.getElementById("chatInput");
    const message = chatBox.value;
    const user = document.getElementById("userName");
    const userName = user.value;
    const request = new XMLHttpRequest();

    const messageObject = {"userName": userName, "message": message};

    request.open("POST", "message");
    request.send(JSON.stringify(messageObject));
}

function recieveMessage() {
    rows = document.getElementById("messageTable").rows.length - 1;
    console.log(rows);
    const request = new XMLHttpRequest();
    
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200)
        {
            console.log(this.response);
            const messageJSON = JSON.parse(this.response);

            const userName = messageJSON["userName"]
            const message = messageJSON["message"]
            const time = messageJSON["time"]

            var table = document.getElementById("messageTable");

            for (var i = 0; i <userName.length; i++)
            {
                row = table.insertRow(1);
                row.insertCell(0).innerHTML = userName[i];
                row.insertCell(1).innerHTML = message[i];
                row.insertCell(2).innerHTML = time[i];
            }
        }
    };

    request.open("GET", "messages" + rows);
    request.send();
}