$(document).ready(function(){
	$('#sidebar > .worker').on('click', function(){
		$(this).parent().find('.worker').removeClass('active');
		$(this).toggleClass('active');
	});

	$('#add_project').on('click', function(){
		window.location.href = 'dashboard.php';
	});

	$('.c-project').on('click', function(){
		window.location.href = 'dashboard.php';
	});
});