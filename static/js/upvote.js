var user_id = document.getElementById("user_id").value;
var post_id = document.getElementById("post_id").value; 
var upvote_button = document.getElementById("upvote");

upvote_button.addEventListener(
    "click", 
    function(){
        $.ajax({
            url: '/upvote_post',
            type:'POST',
            data: {
                user_id: user_id,
                post_id: post_id,
            },
            beforeSend: function () {
                document.getElementById("target").innerText = "Please wait...";
            },
            success: function(msg) {
                document.getElementById("target").innerText = '';
                var upvote_count = document.getElementById("upvote_count");
                upvote_count.textContent = "upvotes: " + (parseInt(upvote_count.textContent.slice(-2)) + 1);
                alert('upvoted');
            },               
        });
    }
);

console.log("go");