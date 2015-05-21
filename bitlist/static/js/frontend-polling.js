/* Most everything in here will be replaced with pub/sub after sockets are impl */

/* pollute global space - cuz yanno */


(function poll() {
    setTimeout(function () {
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
    }, 5000);
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
