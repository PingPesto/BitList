+function ($) { "use strict";

	// sortable
	if ($.fn.sortable) {
	  $('.sortable').sortable();
	}

	// slim-scroll
	$('.no-touch .slim-scroll').each(function(){
		var $self = $(this), $data = $self.data(), $slimResize;
		$self.slimScroll($data);
		$(window).resize(function(e) {
			clearTimeout($slimResize);
			$slimResize = setTimeout(function(){$self.slimScroll($data);}, 500);
		});
    $(document).on('updateNav', function(){
      $self.slimScroll($data);
    });
	});	

	// portlet
	$('.portlet').each(function(){
		$(".portlet").sortable({
	        connectWith: '.portlet',
            iframeFix: false,
            items: '.portlet-item',
            opacity: 0.8,
            helper: 'original',
            revert: true,
            forceHelperSize: true,
            placeholder: 'sortable-box-placeholder round-all',
            forcePlaceholderSize: true,
            tolerance: 'pointer'
	    });
    });

}(window.jQuery);
