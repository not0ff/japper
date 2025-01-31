function showAlert(message, category) {
    const alertContainer = document.getElementById('flashList');
    const alert = `
    <li class="alert alert-dismissible alert-${category} fade show mt-2">
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        <span>${message}</span>
    </li> `;

    alertContainer.innerHTML += alert;
}

async function fetchPost(postId) {
    try {
        const response = await fetch(`/post/fetch?id=${postId}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(`Couldn\'t fetch post ${postId}, ${data.message}`);
        }
        return data.result.post;
    } catch (error) {
        console.error(error);
        showAlert(error, 'danger');
    }
}

async function fetchNotifications(
    autoread = true,
    unread_only = true,
    since = 0
) {
    try {
        const response = await fetch(
            '/notification/get?' +
                new URLSearchParams({
                    autoread: autoread,
                    unread_only: unread_only,
                    since: since,
                }).toString()
        );
        const data = await response.json();
        if (!response.ok) {
            throw new Error(`Couldn\'t fetch notifications, ${data.message}`);
        }
        return data.result.notifications;
    } catch (error) {
        console.error(error);
        showAlert(error, 'danger');
    }
}

async function fetchNotificationsCount() {
    try {
        const response = await fetch('/notification/unread_count');
        const data = await response.json();
        if (!response.ok) {
            throw new Error(
                `Couldn\'t fetch notifications count, ${data.message}`
            );
        }
        return data.result.count;
    } catch (error) {
        console.error(error);
        showAlert(error, 'danger');
    }
}

async function refreshPost(postId) {
    postHtml = await fetchPost(postId);
    document.getElementById(postId).outerHTML = postHtml;
    flask_moment_render_all();
}

async function likeButtonClicked(button) {
    const postId = button.getAttribute('data-post-id');
    const csrfToken = document.getElementById('csrf_token').value;

    const actionEndpoint = button.classList.contains('active')
        ? '/post/add_like'
        : '/post/remove_like';

    try {
        const response = await fetch(actionEndpoint, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                id: postId,
            }),
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(
                `Couldn\'t do like action on post ${postId}, ${data.message}`
            );
        }

        await refreshPost(postId);
    } catch (error) {
        console.error(error);
        showAlert(error, 'danger');
    }
}

function editPostButtonClicked(button) {
    const postId = button.getAttribute('data-post-id');
    const content = document
        .getElementById(postId)
        .querySelector('.post-content').textContent;

    document.getElementById('editPostIdField').value = postId;
    document.getElementById('postContentField').value = content;
}

function deletePostButtonClicked(button) {
    const postId = button.getAttribute('data-post-id');
    document.getElementById('deletePostIdField').value = postId;
}

async function showUserList(element) {
    const elementId = element.getAttribute('data-element-id');
    const listType = element.getAttribute('data-list');

    let actionEndpoint = '/null';
    let listTitle = 'User list';
    switch (listType) {
        case 'followers':
            actionEndpoint = '/profile/get_followers?';
            listTitle = "User's followers";
            break;
        case 'following':
            actionEndpoint = '/profile/get_following?';
            listTitle = 'Following user';
            break;
        case 'likes':
            actionEndpoint = '/post/get_likes?';
            listTitle = 'Users leaving ✨aura✨';
            break;
    }

    try {
        const response = await fetch(actionEndpoint + `id=${elementId}`);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(`Couldn\'t fetch user list, ${data.message}`);
        }

        const modal = document.getElementById('showUsers');
        modal.querySelector('#showUsersLabel').textContent = listTitle;
        modal.querySelector('.modal-body').innerHTML = data.result.userList;

        new bootstrap.Modal(modal).show();
    } catch (error) {
        console.error(error);
        showAlert(error, 'danger');
    }
}

function showNotifications(notifications) {
    const notificationContainer = document.getElementById(
        'notificationContainer'
    );

    notificationContainer.innerHTML = '';
    notifications.forEach((notification) => {
        notificationContainer.innerHTML += notification;
    });

    let delay = 5000 + 500 * notifications.length;
    notificationContainer
        .querySelectorAll('.notification')
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

async function getAllNotifications() {
    const notifications = await fetchNotifications();

    if (Object.keys(notifications).length !== 0) {
        showNotifications(notifications);
    } else {
        const notificationsBtn = document.getElementById('notificationsBtn');
        const infoPopover = bootstrap.Popover.getOrCreateInstance(
            notificationsBtn,
            {
                container: 'body',
                trigger: 'focus',
                content: 'You have no unread notifications',
            }
        );
        infoPopover.show();
    }
    await showUnreadCount();
}

function get_timestamp() {
    return Math.floor(new Date().getTime() / 1000);
}

function notificationUpdates() {
    let timestamp = get_timestamp();

    setInterval(async function () {
        const notifications = await fetchNotifications(true, true, timestamp);

        if (Object.keys(notifications).length !== 0) {
            showNotifications(notifications);
        }
        timestamp = get_timestamp();
    }, 10000);
}

async function showUnreadCount() {
    let count = await fetchNotificationsCount();

    const userMenu = document.getElementById('userMenu');
    const notificationsBtnLink = document
        .getElementById('notificationsBtn')
        .querySelector('span');

    if (count > 0) {
        count = count > 99 ? '99+' : String(count);
        const badge = `
        <span class='position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger notification-badge'>
            ${count}
            <span class="visually-hidden">unread notifications</span>
        </span>`;

        userMenu.innerHTML += badge;
        notificationsBtnLink.innerHTML += badge;
    } else {
        document.querySelectorAll('.notification-badge').forEach((badge) => {
            badge.remove();
        });
    }
}

document.getElementById('postButton').addEventListener('click', function () {
    let post_form = document.getElementById('newPostForm');
    post_form.submit();
});

document
    .getElementById('savePostButton')
    .addEventListener('click', function () {
        const editPostForm = document.getElementById('editPostForm');
        editPostForm.submit();
    });

document
    .getElementById('deletePostButton')
    .addEventListener('click', function () {
        const editPostForm = document.getElementById('deletePostForm');
        editPostForm.submit();
    });

document.addEventListener('DOMContentLoaded', notificationUpdates);
document.addEventListener('DOMContentLoaded', showUnreadCount);
