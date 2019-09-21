$(document).ready(function(){
	$('#back').on('click', function(){
		window.history.go(-1);	
	});
	$('.worker').click(function(){
		$(this).parent().find('.worker').removeClass('active');
		$(this).toggleClass('active');
		$('.collapse').hide();
		$($(this).attr('target')).show();
	});
});