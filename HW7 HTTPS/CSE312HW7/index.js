var socket = new WebSocket('wss://' + window.location.host + '/socket');
socket.onmessage = renderMessages;
function sendMessage() {
    socket.send(JSON.stringify({ 'username': document.getElementById("UserName").value, 'message': document.getElementById("message").value }));
}

function renderMessages(message) {
    console.log(message.data);
    var text_message = JSON.parse(message.data)
    var table = document.getElementById("messageTable");

    row = table.insertRow(1);
    row.insertCell(0).innerHTML = text_message.username;
    row.insertCell(1).innerHTML = text_message.message;
}