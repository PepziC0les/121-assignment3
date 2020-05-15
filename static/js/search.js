function populateTable(response) {
	console.log("test 3");
	let thead = $("#table-head");
	thead.append("<tr><td>Results</td></tr>");
	let tbody = $("#table-body");
	tbody.append("<tr><td>line 0</td></tr>")
}

$('button').on("click", function(){
	console.log("test 2");
	let query = $("#query-text").val();
	populateTable(query);
});

console.log("test 1");