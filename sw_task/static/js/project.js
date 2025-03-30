function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute("content");
}

$(document).on("change", ".category-checkbox", function () {
    let checkbox = $(this);
    let categoryId = checkbox.data("category-id");
    let parentContainer = checkbox.closest("div");
    let subcategoryContainer = parentContainer.children(".subcategories");

    if (checkbox.is(":checked")) {
        $.ajax({
            url: "/api/v2/categories/",
            data: { parent_id: categoryId },
            dataType: "json",
            success: function (data) {
                if (data.count > 0) {
                    let html = `<div class="subcategory-group">`;
                    $.each(data.results, function (index, subcategory) {
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
                        url: "/api/v2/categories/",
                        method: "POST",
                        contentType: "application/json",
                        headers: { "X-CSRFToken": getCSRFToken() },
                        data: JSON.stringify({
                            parent_id: categoryId
                        }),
                        xhrFields: { withCredentials: true }, // Include credentials
                        success: function (newData) {
                            let html = `<div class="subcategory-group">`;
                            $.each(newData, function (index, subcategory) {
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
