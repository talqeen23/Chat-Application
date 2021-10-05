 var socket;
 var seeMessage='';
            jQuery(document).ready(function(){
                socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
                socket.on('connect', function() {
                    socket.emit('joined', {});
                });
                socket.on('status', function(data) {
                    var num=data.dataid;
					if(!jQuery("#c"+data.userid).length > 0){
						jQuery('#chat').html(jQuery('#chat').html() + '<div class="div'+num+' useradded" id="c'+data.userid+'">'+data.msg+'</div>\n');
					}
                    jQuery('#chat').scrollTop(jQuery('#chat')[0].scrollHeight);
					if(jQuery('#user'+data.userid).length <=0 && typeof data.userid != "undefined"){
						jQuery("ul.user_list").append('<li class="online_users online" id="user'+data.userid+'"> <span>'+data.name+' </span></li>');
					}
                });
                socket.on('message', function(data) {
					var name = jQuery(".user-chat").data('id');
					var cls='you';
					if (name==data.name){
						cls='me'
					}
					//var message= data.msg;
					jQuery('#chat').html(jQuery('#chat').html() + data.msg );
					jQuery('#chat .chatlist').last().addClass(cls);
                    jQuery('#chat').scrollTop(jQuery('#chat')[0].scrollHeight);
					
				   if (cls=='you'){
					  seeMessage =  setInterval(function(){
							var title = document.title;
							document.title = (title == "New Message Recieved" ? "Realtime User Login" : "New Message Recieved");
						}, 1000);
					}
                });
                jQuery('#text').keypress(function(e) {
                    var code = e.keyCode || e.which;
					
					if(e.shiftKey==false){
						
						
					
					if (code == 13) {
                        text = jQuery('#text').val();
						if(text.trim()==""){
							return false;
						}
                        jQuery('#text').val('');
                        socket.emit('text', {msg: text});
						jQuery('#text').val('');
						jQuery('#text').focus();
						return false;
                    }
					}
                });
            });
            function leave_room() {
                socket.emit('left', {}, function() {
                    socket.disconnect();

                    // go back to the login page
                    window.location.href = "/";
                });
            }
jQuery(document).ready(function(){
	 getUsersLongPolling()
	var currentPoll;
	function getUsersLongPolling(){
		//alert(lasttime);
		if(currentPoll) {currentPoll.abort();}
		currentPoll = jQuery.ajax({
					type:'POST',
					dataType:'json',
					url:'//' + document.domain + ':' + location.port + '/onlineusers',
					beforeSend : function(){
						
					},
					success:function(data, textStatus, XMLHttpRequest){
						jQuery("li.online_users").each(function(){
							if(jQuery(this).find("span").html()==""){ jQuery(this).remove();}
							
						});
						jQuery("ul.user_list li.online_users").removeClass("online");
						jQuery("ul.user_list li.online_users").addClass("offline");
						if(data){
						jQuery.each( data, function( key, val ) {
							var idc=jQuery("ul.user_list li.online_users").is("#user"+key);
							if(idc){
								jQuery("#user"+key).removeClass("offline");
								jQuery("#user"+key).addClass("online");
							}else{
								jQuery("ul.user_list").append('<li class="online_users online" id="user'+key+'"> <span>'+val+' </span></li>');
							}
							});
						}
						setTimeout(function(){ getUsersLongPolling() },4000);
					},
					error:function(data, textStatus, XMLHttpRequest){
						setTimeout(function(){ getUsersLongPolling() },4000);
					}
					
		});		
		
	}

jQuery(document).on('mouseover','html,body',function(){
	if(seeMessage){ clearInterval(seeMessage); document.title ='Realtime User Login';}
		});
	jQuery(document).on('click','html,body',function(){	
		if(seeMessage){ clearInterval(seeMessage); document.title ='Realtime User Login';}
	});
	jQuery(document).on('click','.send_chat',function(){	
		text = jQuery('#text').val();
						if(text.trim()==""){
							return false;
						}
                        jQuery('#text').val('');
                        socket.emit('text', {msg: text});
						jQuery('#text').val('');
						jQuery('#text').focus();
						return false;
	});
});		


function setHeight(){
	/*if(jQuery(".message-area").length > 0){
	var height=jQuery(window).height()-220-(jQuery(".message-area").height());
	jQuery("div#chat").attr("style","max-height:"+height+"px;min-height:"+height+"px");
	alert(height);
	}*/
	
}
	
