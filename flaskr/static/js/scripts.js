$(document).ready(function() {
	$('.grid').masonry({
		// options
		itemSelector: '.grid-item',
		columnWidth: 100,
		gutter: 5
	});

	$('#file').on('change',function(){
		//get the file name
		var fileName = $(this).val();
		var cleanedName = fileName.split('\\').slice(-1)[0] 
		//replace the "Choose a file" label
		$(this).next('.custom-file-label').html(cleanedName);
	})
});
