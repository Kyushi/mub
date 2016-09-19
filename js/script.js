// All my ajax is based on
// abhishek gosh's (modified) code here from
// https://discussions.udacity.com/t/how-to-update-the-counter-for-likes/179740/4
// because I started this project with no knowledge of Ajax. After writing this
// project, I'm starting to get the hang of it :)


// Like button for posts
$('.like').on('click', function(e){
  e.preventDefault();
  var instance = $(this);
  var key = $(this).data('key');
  var errormsg = $(this).parent().find('span.error');
  var youlike = instance.parent().find('span.you-like');
  $.ajax({
    type: "post",
    url: "/like", // Route which will handle the request
    dataType: 'json',
    data: {"postID": key},
    success: function(data){
      // if there is a problem, display error (with fade out)
      if (data['error']) {
        errormsg.html(data['error']);
        errormsg.fadeToggle(1500, 'swing', function(){
          errormsg.html('');
          errormsg.toggle(0);
        });
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


// Submit comments

// show form to enter comment and remove placeholder when clicked
$('.comment-placeholder').on('click', function(e) {
    var commentForm = $(this).parent().find('.comment-input-form')
    commentForm.css('display', 'block');
    commentForm.find('.comment-input').focus();
    console.log(commentForm.html())
    $(this).css('display', 'none');
});

// Submit comments, write to datastore and dynamically update on front end
$('.submit-button').on('click', function(e){
  e.preventDefault();
  var comment = $(this).parent().find('.comment-input').val();
  var parent = $(this).data('parentid');
  var commentForm = $(this).parent().parent()
  console.log(comment)
  $.ajax({
    type: "post",
    url: "/comment",
    dataType: 'json',
    data: {"parent": parent, "comment": comment},
    success: function(data){
      commentForm.css('display', 'none');
      commentForm.prev('.comment-placeholder').css('display', 'block');
      commentForm.find('textarea').val('');
      commentForm.parent().find('div.comment-list').prepend(data['comment']);
    },
    error: function(err){
      console.log(err);
      console.log('there was no comment');
    }
  });
});

// Reverse display of placeholder and comment form when user clicks outside of comment
$('.cancel-comment').on('click', function(e) {
  e.preventDefault();
  $('.comment-input-form').css('display', 'none');
  $('.comment-placeholder').css('display', 'block');
});

// Edit comments

// Toggle display of editing form and comment div
$('.comment-list').on('click', '.edit', function(e){
  e.preventDefault();
  $(this).parent().prev('div.comment-edit-form').toggle('display');
  $(this).parent().toggle('display');
});

// Post data to backend via ajax and update comment in situ
$('.comment-list').on('click', '.save-button', function(e){
  e.preventDefault();
  var commentText = $(this).prev('textarea.comment-input').val();
  if($.trim(commentText).length > 0){
    var commentDiv = $(this).parent().parent().next('div.single-comment');
    var commentEditForm = $(this).parent().parent();
    var commentID = $(this).data('commentid');
    $.ajax({
      type: "post",
      url: "/editcomment",
      dataType: 'json',
      data: {"commentid": commentID, "newcomment": commentText},
      success: function(data){
        commentDiv.find('p.comment-content').html(data['comment']);
        commentDiv.toggle('display');
        commentEditForm.toggle('display');
      },
      error: function(err) {
        console.log(err);
        console.log('There was a problem with this comment')
      }
    });
  }
  else {
    $(this).parent().next().text("If you want to remove your comment, please use the delete button");
    $(this).parent().next().toggle(1500, function(){
      $(this).parent().next('.error').text("");
      $(this).parent().next('.error').toggle(0);
  });
  }
});

// Cancel editing a comment
$('.comment-list').on('click', '.cancel-button', function(e){
  e.preventDefault();
  $(this).parent().parent().next('div.single-comment').toggle('display');
  $(this).parent().parent().toggle('display');
});

  // Delete comments
$('.blog-article').on('click', '.delete', function(e){
  e.preventDefault();
  var instance = $(this);
  var ids = $(this).data('ids');
  $.ajax({
    type: "post",
    url: "/delete",
    dataType: 'json',
    data: {"ids": ids},
    success: function(data){
      instance.closest('.single').remove();
    },
    error: function(err) {
      console.log(err);
      console.log('There was a problem');
    }
  });
});
