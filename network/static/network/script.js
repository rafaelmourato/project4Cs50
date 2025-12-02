document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.onclick = () => editPost(button.dataset.id);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".like-btn").forEach(button => {
        button.onclick = () => toggleLike(button.dataset.id);
    });
});

function toggleLike(id) {
    fetch(`/like/${id}`, {
        method: "PUT",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.log(data.error);
            return;
        }
        const btn = document.querySelector(`button[data-id='${id}']`);
        btn.innerText = data.liked ? "Unlike" : "Like";
        document.getElementById(`likes-${id}`).innerText = data.like_count;
    });
}

function editPost(id) {
    const contentNew = document.getElementById(`content-${id}`);
    const oldContent = contentNew.innerText;
    contentNew.innerHTML = `
        <textarea id="textarea-${id}" class="edit-area">${oldContent}</textarea>
    `;
    const button = document.querySelector(`button[data-id='${id}']`);
    button.innerText = "Save";
    button.onclick = () => saveEdit(id);
}

function saveEdit(id) {
    const newContent = document.getElementById(`textarea-${id}`).value;
    fetch(`/edit/${id}`, {
        method: "PUT",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify({ content: newContent })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        document.getElementById(`content-${id}`).innerHTML = newContent;
        const button = document.querySelector(`button[data-id='${id}']`);
        button.innerText = "Edit";
        button.onclick = () => editPost(id);
    });
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}