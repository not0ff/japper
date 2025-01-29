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
    return fetch(
        "/post/fetch?" +
            new URLSearchParams({
                id: postId,
            }).toString(),
        {
            method: "GET",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
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

function showNotifications(notifications) {
    const notificationContainer = document.getElementById(
        "notificationContainer"
    );

    notificationContainer.innerHTML = "";
    notifications.forEach((notification) => {
        const content = notificationContainer.innerHTML;
        notificationContainer.innerHTML = content + notification;
    });

    let delay = 5000 + 500 * notifications.length;
    notificationContainer
        .querySelectorAll(".notification")
        .forEach((notification) => {
            const notificationToast = bootstrap.Toast.getOrCreateInstance(
                notification,
                { delay: delay }
            );
            notificationToast.show();
            delay -= 500;
        });
    flask_moment_render_all();
}

function getAllNotifications(unread_only = false, autoread = true) {
    fetch(
        "/notification/get?" +
            new URLSearchParams({
                unread_only: unread_only,
                autoread: autoread,
            }).toString(),
        {
            method: "GET",
            headers: {
                "Content-type": "application/json; charset=UTF-8",
            },
        }
    )
        .then((response) => response.json())
        .then((notificationList) => showNotifications(notificationList));
}

function get_timestamp() {
    return Math.floor(new Date().getTime() / 1000);
}

function notificationUpdates() {
    let timestamp = get_timestamp();

    setInterval(function () {
        fetch(
            "/notification/get?" +
                new URLSearchParams({
                    since: timestamp,
                    unread_only: true,
                    autoread: true,
                }).toString(),
            {
                method: "GET",
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                },
            }
        )
            .then((response) => response.json())
            .then((notificationList) => {
                if (Object.keys(notificationList).length !== 0) {
                    showNotifications(notificationList);
                }
                timestamp = get_timestamp();
            });
    }, 10000);
}

async function getNotificationsCount() {
    const response = await fetch("/notification/unread_count");
    const json_resp = await response.json();
    return json_resp.count;
}

document.addEventListener("DOMContentLoaded", notificationUpdates);
