function getPortletId(node) {
    return node.attr('id').substring(8);
};
function getSlot(node) {
    var i = 0;
    while (! node.hasClass('slot')) {
        node = node.parent();
        if ( i++ > 5) break; // zu tiefe recusion verhindern
    }
    return node;
}
function getSlotId(node) {
    return node.attr('id').substring(5);
};
$(function() {
    $(".staffview").sortable({
        handle: ".handle",
        items: ".portlet",
        connectWith: ".slot",
        start: function(event, ui) {
            var start_pos = ui.item.index();
            ui.item.data('start_pos', start_pos);
        },
        update: function(event, ui) {
            if (this === ui.item.parent()[0]) {
                var start_pos = ui.item.data('start_pos');
                var index = ui.item.index();
                var portlet = ui.item;
                var pId = getPortletId(portlet);
                var slot = $(this).closest('.slot').attr("id").replace("slot-", "");
                $.get('/portlet/move/' + pId + '/' + (index-start_pos) + '/' + slot + '/');
            }
        },
    });
	$('.portlet .inherit').click(function() {
		var portlet = $(this).parents(".portlet");
		var link = $(this);
		var pId = getPortletId(portlet);
		$.get('/portlet/inherit/' + pId + '/', function(data) {
			if (data == '') {
				document.location.reload(true);
			}
			else {
				alert(data);
			}
		});
		return false;
	});
	$('.portlet .delete').click(function() {
		var portlet = $(this).parents(".portlet");
		var pId = getPortletId(portlet);
		$.get('/portlet/delete/' + pId + '/', function(data) {
			if (data == '') {
				portlet.slideUp().remove();    
			}
			else {
				alert(data);
			}
		});
		return false;
	});
	$('.portlet .delete-here').click(function() {
		var portlet = $(this).parents(".portlet");
		var pId = getPortletId(portlet);
		$.get('/portlet/delete/' + pId + '/', {'where': 'here', path: document.location.pathname}, function(data) {
			if (data == '') {
				portlet.addClass("prohibited");
			}
			else {
				alert(data);
			};
		});
		return false;
	});
	$('.portlet .delete-here-inherit').click(function() {
		var portlet = $(this).parents(".portlet");
		var pId = getPortletId(portlet);
		$.get('/portlet/delete/' + pId + '/', {'where': 'here-inherit', path: document.location.pathname}, function(data) {
			if (data == '') {
				portlet.addClass("prohibited");
			}
			else {
				alert(data);
			}
		});
		return false;
	});
    $(".popuplink").click(function () {
        href = this.href;
        var win = window.open(href, "popupwindow", 'height=500,width=800,resizable=yes,scrollbars=yes');
        win.focus();
        return false;
    });
    var overlay = $('<div id="portletStaffToggleOverlay"><a href="#" id="portletStaffViewToggle">Editieren</a></div>');
    $('body').append(overlay);
    $("#portletStaffToggleOverlay").show();
    if(localStorage && localStorage.getItem('portletStaffToggleOverlay') == 1) {
    	$(".staff").show();
    };
    $('#portletStaffViewToggle').click(function() {
    	$(".staff").slideToggle(200);
    	if(localStorage && localStorage.getItem('portletStaffToggleOverlay') == 1) {
    		localStorage.setItem('portletStaffToggleOverlay', 0);
    	} else {
    		localStorage.setItem('portletStaffToggleOverlay', 1);
    	};
    	return false;
    });
    var portletStaffOverlay = false;
    $('.slot a.add-portlet').click(function() {
    	if(!portletStaffOverlay) {
    		portletStaffOverlay = true;
	        var overlay = $('<div id="portletStaffOverlay"></div>');
	        $('body').append(overlay);
	        var slot = getSlot($(this));
	        var slotId = getSlotId(slot);
	
	        $.get('/portlet/add/', function(data, textStatus, xdr) {
	            overlay.html('');
	            var html = '<ul class="portletcategories" id="portletcategories">'
	            for (var i = 0; i < data.length; i++) {
	                var item = data[i];
	                html += '<li class="portletcategory"><a href="#">'+ item.category;
	                html += '</a><ul>';
	                for (var j = 0; j < item.portlets.length; j++) {
	                    html += '<li class="portlet"><a href="/portlet/add/?slot=' + slotId + '&path=' + location.pathname + '&pk=' + item.portlets[j].pk + '">' + item.portlets[j].title + '</a>';
	                }
	                html += '</ul></li>';
	            }
	            html += '</ul><a href="#" id="closePortletStaffOverlay">Schließen</a>';
	            $(html).appendTo(overlay);
	            $("#closePortletStaffOverlay").click(function() {
	            	$(this).parent().fadeOut().delay(400).remove();
	            	portletStaffOverlay = false;
	            	return false;
	            })
	            $(".portletcategory > a").click(function(e){
	            	var el = $('#portletcategories');
	            	el.children("li").removeClass("active");
	            	el.find("ul").hide();
	            	$(this).parent().addClass("active").find("ul").fadeIn(100);
	            	e.preventDefault();
	            });
	            overlay.fadeIn();
	        }, 'json');
    	};
        return false;
    });
});
