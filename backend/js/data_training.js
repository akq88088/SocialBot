$(document).ready(function(){
	$('#sidebar > .worker').on('click', function(){
		$(this).parent().find('.worker').removeClass('active');
		$(this).toggleClass('active');
	});

	$('#frontend').on('click', function(){
		window.location.href = '../frontend/project.php';
	});
	
	$('#add_project').on('click', function(){
		// history.replaceState(null, "report page", window.location.href);
		window.location.href = 'train.php';
	});

	$('.c-project').on('click', function(){
		// history.replaceState(null, "report page", window.location.href);
		window.location.href = 'train.php';
	});
});