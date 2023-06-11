function htmlspecialchars(str) {
    if (typeof (str) == "string") {
        str = str.replace(/&/g, "&amp;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
    }

    return str;
}

function q_e(s) {
    // Work out if using a ' or " to wrap the string
    // is more efficient by counting the occurences

    var a = s.split("'").length;
    var b = s.split('"').length;

    if (a < b) {
        // Escape using '
        return "'" + s.replace(/'/g, "\\'") + "'";
    }

    // Escape using "
    return '"' + s.replace(/"/g, '\\"') + '"';
}

const createReview = function (title, description, profileImage, productImage, productLink, accountId, userName, category, productName, id) {
    title = htmlspecialchars(title);
    description = htmlspecialchars(description);
    userName = htmlspecialchars(userName);
    category = htmlspecialchars(category);
    productName = htmlspecialchars(productName);

    profileImage = q_e(profileImage);
    productImage = q_e(productImage);
    productLink = q_e(productLink);
    id = q_e("/review/" + id);
    accountId = q_e("/account/" + accountId);

    let html = `<article class="review outer"
    href=${id} onclick=""
    <div class="review inner">
        <div class="image" style="
background-image: url(${profileImage});
"></div>
        <div class="itemInfo">
            <h3>
                ${title}
            </h3>
            <div class="innerInfo">
                <a href=${productLink}
                    target="_blank" class="meta productName">${productName}
                </a>
                <span class="meta category">${category}</span>
                <a class="username" href=${accountId}
                    target="_blank">by <span class="innerUser">${userName}</span></a>
            </div>
            <p class="meta overview">
                ${description}
            </p>
            <div class="buttons">
                <form onsubmit=""></form>
            </div>
        </div>
    </div>
</article>`
    document.querySelector("div.reviewList.inner .reviews").insertAdjacentHTML("beforeend", html);
}