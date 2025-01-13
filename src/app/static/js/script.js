document.querySelectorAll("ul.navbar-nav a.nav-link").forEach(function (link) {
    if (link.href === window.location.href) {
        link.classList.add("active");
    }
});

document.getElementById("postButton").addEventListener("click", function () {
    let post_form = document.getElementById("newPostForm");
    post_form.submit();
});

document.getElementById("saveButton").addEventListener("click", function () {
    let profile_form = document.getElementById("editProfileForm");
    profile_form.submit();
});

function likeButtonClicked(button) {
    let postId = button.getAttribute("data-bs-id");
    let csrfToken = document.getElementById('csrf_token').value;

    if (button.classList.contains('active')) {
        fetch('/add_like', {
            method: "POST",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                post_id: postId
              }),
            credentials: 'include',
        })
        .then((response) => response.json())
        .then((json) => console.log(json));
    } else {
        console.log("...");
    }
}
