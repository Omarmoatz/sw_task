function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split("; ");
    for (let i = 0; i < cookies.length; i++) {
        let parts = cookies[i].split("=");
        if (parts[0] === "csrftoken") {
            cookieValue = decodeURIComponent(parts[1]);
            break;
        }
    }
    return cookieValue;
}

$(document).on("change", ".category-checkbox", function () {
    let checkbox = $(this);
    let categoryId = checkbox.data("category-id");
    let parentContainer = checkbox.closest("div");
    let subcategoryContainer = parentContainer.children(".subcategories");

    if (checkbox.is(":checked")) {
        $.ajax({
            url: "/api/categories/",
            data: { parent_id: categoryId },
            dataType: "json",
            success: function (data) {
                if (data.categories.length > 0) {
                    let html = `<div class="subcategory-group">`;
                    $.each(data.categories, function (index, subcategory) {
                        html += `
                            <div class="ms-4">
                                <input type="checkbox" class="category-checkbox" data-category-id="${subcategory.id}">
                                <label>${subcategory.name}</label>
                                <div class="subcategories"></div>
                            </div>
                        `;
                    });
                    html += `</div>`;
                    subcategoryContainer.html(html);
                } else {
                    // No subcategories found, create two new ones
                    $.ajax({
                        url: "/api/categories/",
                        method: "POST",
                        contentType: "application/json",
                        headers: { "X-CSRFToken": getCSRFToken() },
                        data: JSON.stringify({
                            parent_id: categoryId
                        }),
                        success: function (newData) {
                            let html = `<div class="subcategory-group">`;
                            $.each(newData.categories, function (index, subcategory) {
                                html += `
                                    <div class="ms-5">
                                        <input type="checkbox" class="category-checkbox" data-category-id="${subcategory.id}">
                                        <label>${subcategory.name}</label>
                                        <div class="subcategories"></div>
                                    </div>
                                `;
                            });
                            html += `</div>`;
                            subcategoryContainer.html(html);
                        },
                        error: function () {
                            console.error("Failed to create subcategories.");
                        }
                    });
                }
            },
            error: function () {
                console.error("Failed to fetch subcategories.");
            }
        });
    } else {
        subcategoryContainer.empty();
    }
});
