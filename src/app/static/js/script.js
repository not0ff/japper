document.querySelectorAll("ul.navbar-nav a.nav-link").forEach(function (link) {
    if (link.href === window.location.href) {
        link.classList.add("active");
    }
});

document.getElementById("postButton").addEventListener("click", function () {
    let post_form = document.getElementById("newPostForm");
    post_form.submit();
});

document.getElementById("savePostButton").addEventListener("click", function () {
    const editPostForm = document.getElementById("editPostForm");
    editPostForm.submit();
});