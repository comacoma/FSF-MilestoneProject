$(document).ready(function() {
    $('#message').delay(3500).show().slideUp();

    $('.comment-edit').on('click', function(e) {
        var comment_id = "#comment_" + e.target.id;

        $('#edit-comment-modal').modal('toggle');
        $('#edit-comment').val($(comment_id).text());
    });

    $('#comment-edit-form').on('submit', function(event) {
        event.preventDefault();
    });
});
