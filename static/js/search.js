$(function(){
	$('button').click(function(){
		var user = $('#query-text').val();
		$.ajax({
			url: '/search',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});