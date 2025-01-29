async function fetchPost(postId) {
    const response = await fetch(`/post/fetch?id=${postId}`);
    const data = await response.text();

    return data;
}

async function refreshPost(postId) {
    postHtml = await fetchPost(postId);
    document.getElementById(postId).outerHTML = postHtml;
    flask_moment_render_all();
}

async function likeButtonClicked(button) {
    const postId = button.getAttribute("data-post-id");
    const csrfToken = document.getElementById("csrf_token").value;

    const actionEndpoint = button.classList.contains("active")
        ? "/post/add_like"
        : "/post/remove_like";

    const response = await fetch(actionEndpoint, {
        method: "POST",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
            id: postId,
        }),
    });

    await refreshPost(postId);
}

function editPostButtonClicked(button) {
    const postId = button.getAttribute("data-post-id");
    const content = document
        .getElementById(postId)
        .querySelector(".post-content").textContent;

    document.getElementById("editPostIdField").value = postId;
    document.getElementById("postContentField").value = content;
}

function deletePostButtonClicked(button) {
    const postId = button.getAttribute("data-post-id");
    document.getElementById("deletePostIdField").value = postId;
}

async function showUserList(element) {
    const elementId = element.getAttribute("data-element-id");
    const listType = element.getAttribute("data-list");

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

    const response = await fetch(actionEndpoint + `id=${elementId}`);
    const userList = await response.text();

    const modal = document.getElementById("showUsers");

    modal.querySelector(".modal-title").textContent = listTitle;
    modal.querySelector(".modal-body").innerHTML = userList;

    new bootstrap.Modal(modal).show();
}

function showNotifications(notifications) {
    const notificationContainer = document.getElementById(
        "notificationContainer"
    );

    notificationContainer.innerHTML = "";
    notifications.forEach((notification) => {
        notificationContainer.innerHTML += notification;
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

async function getAllNotifications(unread_only = false, autoread = true) {
    const response = await fetch(
        `/notification/get?unread_only=${unread_only}&autoread=${autoread}`
    );
    const notifications = await response.json();

    showNotifications(notifications);
    await showUnreadCount();
}

function get_timestamp() {
    return Math.floor(new Date().getTime() / 1000);
}

function notificationUpdates() {
    let timestamp = get_timestamp();

    setInterval(async function () {
        const response = await fetch(
            `/notification/get?unread_only=true&autoread=true&since=${timestamp}`
        );
        const notifications = await response.json();

        if (Object.keys(notifications).length !== 0) {
            showNotifications(notifications);
        }
        timestamp = get_timestamp();
    }, 10000);
}

async function getNotificationsCount() {
    const response = await fetch("/notification/unread_count");
    const json_resp = await response.json();

    return json_resp.count;
}

async function showUnreadCount() {
    let count = await getNotificationsCount();

    const userMenu = document.getElementById("userMenu");
    const notificationsBtn = document.getElementById("notificationsBtn");

    if (count > 0) {
        count = count > 99 ? "99+" : String(count);
        const badge = `<span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger notification-badge">${count}</span>`;

        userMenu.innerHTML += badge;
        notificationsBtn.innerHTML += badge;
    } else {
        document.querySelectorAll(".notification-badge").forEach((badge) => {
            badge.remove();
        });
    }
}

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

document.addEventListener("DOMContentLoaded", notificationUpdates);
document.addEventListener("DOMContentLoaded", showUnreadCount);
