var socket = new WebSocket('ws://' + window.location.host + '/socket');
socket.onmessage = renderMessages;

const str1 = "KFsnSLtfo7fPdZF5VyY4vwLwhS6iOuxuEHc7D8J3xnZGZiOz3jQCyKTuyDiDx24C2gbGWIx9Oyr2lXQMf8LrptJKDUhYI64kpjOCSlqa0UmLZhQJmdh9aMfSsMUY1u3I3dURLp0qFXD8caNJfUTalnxq5PTkB8cyICy7NE5q4s1yVqzNvUPCYj5lhnDp4LbWZKNZDcRdiAQvZNzNWkdSO6BL5YF22DG6cfsdxswuafl9nftQqZvg1ObNklDR0dSRZQFYpXQCS3DTmIGUS233iDxMejBwYxm1QlruZIl3Qp0LFzcvWR2QghTxbuwaqiVwPYJonX3v5cfkpLxDQcvhKsTUwgEEpiyyKWD1xudSyU4jTzl4ZHHdeOFlXXQskRl6k9wmoS3JTNR9Q0ogrAMAleU0IrwMqTZ7WoSYvWtP7mUVr6JvwMMpV9FPicPpWvJZLmSzwaaWtGC8TRS0ntY6iQBY3QYEsV1t9XVY7A08r362h9XFIDpY"
const str2 = "epy7Dyh3LhwXhMSsHwaB6vuP9D3By7kXxCD2jCAj93hd8QQRBxDPXtJ5Z3whIuOSD8LglmRs4eOajmZUWUUQo6j5vP9V3T1juS2bwYBMjbg2gpmqorbANdTPLydGKN7LqOaE8nO46eyju22KRbHixGsHDXblV3l9qEcpOcxCjt2ObdcQHa1Ik25L091vw0IYCQPqMyjFQcRWlBADI2DuhMOV5WnWjmTYSR4Z8lejIsQoC3i44gljoysRya1iOJbRfxOpcubiJkF8MvjfeWrmGvpSxweGeNfczbhYjeevXkvriKfuV5zMNh1nBl8pOAOxtxrO7MtSwbgMfl3hdrGtedODcKfim9RJxbmUZqy9Cgejy7xl2PWqtiZ6QE1qUn8kZjjapBf5QU13GIpERCIto1Jm38a0lQcrhv1hqQ7b0ng9jfyPdRObGUiVLKQm4REAK3txIrraci3eXRjnvNIvStgUATNkMeBFGjoA7vLX7KBvEhQGTWZT"

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

function randoText() {
    document.getElementById("UserName").value = str1;
    document.getElementById("message").value = str2;
}