function fetchPost(postId) {
    const csrfToken = document.getElementById("csrf_token").value;

    return fetch("/api/fetch_post", {
        method: "POST",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            post_id: postId,
        }),
        credentials: "include",
    }).then((response) => {
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

    let actionEndpoint = "/api/add_like";
    if (!button.classList.contains("active")) {
        actionEndpoint = "/api/remove_like";
    }

    fetch(actionEndpoint, {
        method: "POST",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            post_id: postId,
        }),
        credentials: "include",
    })
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
            refreshPost(postId);
        });
}

function editPostButtonClicked(button) {
    const postId = button.getAttribute("data-bs-id");
    const content = document.getElementById(postId).getElementsByClassName('post-content').item(0).textContent

    document.getElementById('editPostIdField').value = postId;
    document.getElementById('postContentField').value = content;
}

function deletePostButtonClicked(button) {
    const postId = button.getAttribute("data-bs-id");
    document.getElementById('deletePostIdField').value = postId;
}