document.querySelectorAll("ul.navbar-nav a.nav-link").forEach(function (link) {
    if (link.href === window.location.href) {
        link.classList.add("active");
    }
});

document.getElementById("postButton").addEventListener("click", function () {
    let post_form = document.getElementById("newPostForm");
    post_form.submit();
});

document
    .getElementById("savePostButton")
    .addEventListener("click", function () {
        const editPostForm = document.getElementById("editPostForm");
        editPostForm.submit();
    });

document
    .getElementById("deletePostButton")
    .addEventListener("click", function () {
        const editPostForm = document.getElementById("deletePostForm");
        editPostForm.submit();
    });

function fetchPost(postId) {
    const csrfToken = document.getElementById("csrf_token").value;

    return fetch(
        "/post/fetch?" +
            new URLSearchParams({
                id: postId,
            }).toString(),
        {
            method: "GET",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "X-CSRFToken": csrfToken,
            },
        }
    ).then((response) => {
        return response.text();
    });
}

function refreshPost(postId) {
    fetchPost(postId).then((newPost) => {
        document.getElementById(postId).outerHTML = newPost;
        flask_moment_render_all();
    });
}

function likeButtonClicked(button) {
    const postId = button.getAttribute("data-bs-id");
    const csrfToken = document.getElementById("csrf_token").value;

    let actionEndpoint = "/post/add_like";
    if (!button.classList.contains("active")) {
        actionEndpoint = "/post/remove_like";
    }

    fetch(actionEndpoint, {
        method: "POST",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            id: postId,
        }),
    }).then((response) => refreshPost(postId));
}

function editPostButtonClicked(button) {
    const postId = button.getAttribute("data-bs-id");
    const content = document
        .getElementById(postId)
        .querySelector(".post-content").textContent;

    document.getElementById("editPostIdField").value = postId;
    document.getElementById("postContentField").value = content;
}

function deletePostButtonClicked(button) {
    const postId = button.getAttribute("data-bs-id");
    document.getElementById("deletePostIdField").value = postId;
}

function showUserList(element) {
    const userId = element.getAttribute("data-bs-id");
    const listType = element.getAttribute("data-bs-list-type");
    const csrfToken = document.getElementById("csrf_token").value;

    let actionEndpoint = "/null";
    let listTitle = "User list";
    switch (listType) {
        case "followers":
            actionEndpoint = "/profile/get_followers?";
            listTitle = "User's followers";
            break;
        case "following":
            actionEndpoint = "/profile/get_following?";
            listTitle = "Following user";
            break;
        case "likes":
            actionEndpoint = "/post/get_likes?";
            listTitle = "Users leaving ✨aura✨";
            break;
    }

    fetch(
        actionEndpoint +
            new URLSearchParams({
                id: userId,
            }).toString(),
        {
            method: "GET",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "X-CSRFToken": csrfToken,
            },
        }
    )
        .then((response) => response.text())
        .then((userList) => {
            const modal = document.getElementById("showUsers");
            modal.querySelector(".modal-title").textContent = listTitle;
            modal.querySelector(".modal-body").innerHTML = userList;

            new bootstrap.Modal(modal).show();
        });
}
