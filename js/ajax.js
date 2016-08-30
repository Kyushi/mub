// using abhishek gosh's (modified) code here from
// https://discussions.udacity.com/t/how-to-update-the-counter-for-likes/179740/4
// because I don't know Ajax yet but want the like counter to update without reload

// Update: I'm getting the hang of this Ajax thingy :)

$('.like').on('click', function(e){
  console.log('clicked!')
   e.preventDefault();
   var instance = $(this);
   var key = $(this).data('key');
   var errormsg = instance.parent().parent().next().next().find('p.error');
   var youlike = instance.parent().parent().next().find('p.you-like');
    $.ajax({
      type: "post",
      url: "/like", // Route which will handle the request
      dataType: 'json',
      data: {"entryID": key},
      success: function(data){
          // if there is a problem, display error (with fade out)
          if (data['error']) {
              errormsg.html(data['error']);
              errormsg.css("opacity", "0");
            }
          // if there is no problem, update like counter and let user know
          // that they like it
          else {
            instance.find('span').html(data['likes']);
            youlike.html(data['you-like']);
          }
        },
      error: function(err){
          console.log(err);
          console.log('something went wrong');
       }
    });
  });

// when user mouseenters the like link, the opacity gets restored and the error
// removed, so that it can be displayed again upon clicking
$('.like').mouseenter(function(){
    var instance = $(this);
    var errormsg = instance.parent().parent().next().next().find('p.error');
    errormsg.html('');
    //errormsg.css("transition", "0s")
    errormsg.css("opacity", "1");
});


// submit comments
// $('.comment-input').keydown(function(e){
//   if(e.which==13) {
//     e.preventDefault();
//     e.stopPropagation();
//     var comment = $(this,'.comment').val();
//     var parent = $(this).data('parentid');
//     $.ajax({
//       type: "post",
//       url: "/comment", // Route which will handle the request
//       dataType: 'json',
//       data: {"parent": parent, "comment": comment},
//       success: function(data){
//             // $(this).parent().html(data['comments']);
//           },
//       error: function(err){
//           console.log(err);
//           console.log('something went wrong');
//        }
//      });
//   }
// });
