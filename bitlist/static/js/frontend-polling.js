/* Most everything in here will be replaced with pub/sub after sockets are impl */

/* pollute global space - cuz yanno */


(function poll() {
    setTimeout(function () {
        console.log('tick')
        $.ajax({
            type: 'GET',
            dataType: 'json',
            url: '/player/playlist',
            success: function(data) {
                if(localStorage.getItem('debug') == "true"){
                    console.log(data)
                }
                update_playlist(data)
            },
            complete: poll
        });
    }, 10000);
})();


function update_playlist(data){
    $('#playing-list').children().remove();
    $(data).each(function(item) {
       var source = $("#playlist-item-template").html();
       var template = Handlebars.compile(source);
       var html = template(data[item]);
       $('#playing-list').append(html);
    })

}

function array_compare(a, b){
    // Make hashtable of ids in B
    var bIds = {}
    b.forEach(function(obj){
        bIds[obj.id] = obj;
    });
    console.log(bIds)
    // Return all elements in A, unless in B
    return a.filter(function(obj){
        return !(obj.id in bIds);
    });
}

/* Library Javascript */
// Add Library Enqueue method
$('.library-play').on('click', function(e){
   console.log($(this).parent().data('value'))
   $.ajax({
       url: "/player/playlist/queue/" + $(this).parent().data('value'),
   })
  $(this).parent().fadeOut(1000)
});

$('.library-info').on('click', function(e){
   console.log($(this).parent().data('value'))
   $.ajax({
       url: "/songs/" + $(this).parent().data('value'),
   }).done(function(data){
       console.log(data)
       var modal = $('#song-info-modal')
       modal.find('.modal-title').text(data['title'])
       var source = $("#song-info-data").html();
       var template = Handlebars.compile(source);
       var html = template(data);
       var body = modal.find('.modal-body')
       body.children().remove()
       body.append(html)
   })
   $('#song-info-modal').modal({'backdrop': true, 'keyboard': true})
});


