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
        start: function(event, ui) {
            var start_pos = ui.item.index();
            ui.item.data('start_pos', start_pos);
        },
        change: function(event, ui) {
            var start_pos = ui.item.data('start_pos');
            var index = ui.placeholder.index();
            var portlet = ui.item;
            var pId = getPortletId(portlet);
            if (index > start_pos) {
                $.get('/portlet/movedown/' + pId + '/');
            }
            else if (index < start_pos) {
                $.get('/portlet/moveup/' + pId + '/');
            }
        }
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

    $('.slot a.add-portlet').click(function() {
        var overlay = $('#overlay');
        var slot = getSlot($(this));
        var slotId = getSlotId(slot);

        $.get('/portlet/add/', function(data, textStatus, xdr) {
            overlay.css({top: '100px', left: '100px'});
            overlay.html('');
            var html = '<ul class="portletcategories">'
            for (var i = 0; i < data.length; i++) {

                var item = data[i];
                html += '<li class="portletcategory">'+ item.category;
                html += '<ul>';
                for (var j = 0; j < item.portlets.length; j++) {
                    html += '<li class="portlet"><a href="/portlet/add/?slot=' + slotId + '&path=' + location.pathname + '&pk=' + item.portlets[j].pk + '">' + item.portlets[j].title + '</a>';
                }
                html += '</ul></li>';
            }
            html += '</ul>';
            $(html).appendTo(overlay);
            $(".portletcategory").click(function(){$(this).children().toggle()});
            overlay.fadeIn();
        }, 'json');
    });
});
