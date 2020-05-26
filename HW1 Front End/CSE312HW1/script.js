function addRow() {
    var myTable = document.getElementById('myTable');
    var lastEvenNum = myTable.lastElementChild.lastElementChild.firstElementChild.innerHTML;
    var even = parseInt(lastEvenNum) + 2;

    console.log(myTable.innerHTML);

    myTable.innerHTML = myTable.innerHTML + "<tr><th>" + even + "</th><th>" + (even + 1) + "</th></tr>";
}