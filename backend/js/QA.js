$(document).ready(function(){
	$('#sidebar > .worker').on('click', function(){
		// $(this).parent().find('.worker').removeClass('active');
		// $(this).toggleClass('active');
		window.location.href = $(this).attr('id') + '.html';
	});


	$('#add_project').on('click', function(){
		window.location.href = 'dashboard.html';
	});

	$('.c-project').on('click', function(){
		window.location.href = 'dashboard.html';
	});

	
});